import frappe
from frappe.utils import add_days
from frappe.utils import formatdate

def activate_gift_voucher(doc, method):
    """ Update Gift Voucher Status, Expiration Date, Issue Date & Docstatus on SI Submission """
    for item in doc.items:
        if item.item_code == "Gift Voucher" and item.custom_gift_voucher_code:
            # Fetch Gift Voucher
            gift_voucher = frappe.get_doc("Gift Voucher", item.custom_gift_voucher_code)

            # Update Status, Issue Date, Expiration Date, and Docstatus
            gift_voucher.status = "Active"
            gift_voucher.issue_date = doc.posting_date
            gift_voucher.expiration_date = add_days(doc.posting_date, gift_voucher.expiry_days or 0)
            gift_voucher.docstatus = 1
            gift_voucher.save()
            frappe.msgprint(f"""
                <p><b>Gift Voucher <span style="color:green;">{gift_voucher.name}</span> Activated.</b></p>
                <p><b>Issue Date:</b> {formatdate(gift_voucher.issue_date, "dd/mm/yyyy")}</p>
                <p><b>Expiration Date:</b> {formatdate(gift_voucher.expiration_date, "dd/mm/yyyy")}</p>
            """, title="Gift Voucher Activated", indicator="green")

def validate_gift_voucher_for_redeemed(doc, method):
    for item in doc.payments:
        if item.mode_of_payment == "Gift Voucher" and item.custom_gift_voucher_code:
            gift_voucher = frappe.get_doc("Gift Voucher", item.custom_gift_voucher_code)

            # Check if the Gift Voucher has enough balance
            if gift_voucher.current_balance >= item.amount:
                # Deduct the used amount from the voucher balance
                gift_voucher.current_balance -= item.amount

                # Increment the redemption count
                gift_voucher.redemption_count += 1

                # Update status based on remaining balance
                if gift_voucher.current_balance == 0:
                    gift_voucher.status = "Redeemed"
                    frappe.msgprint(f"Gift Voucher {gift_voucher.name} fully redeemed.")

                else:
                    gift_voucher.status = "Active"  # Keep it Active for further use
                    frappe.msgprint(f"Gift Voucher {gift_voucher.name} partially redeemed. Remaining balance: {gift_voucher.current_balance}")

                # Save the updated voucher details
                gift_voucher.save()

            else:
                frappe.throw(f"Insufficient balance in Gift Voucher {gift_voucher.name}. Available: {gift_voucher.current_balance}, Required: {item.amount}")



def create_gift_voucher_journal_entry(doc, method):
    """Create a Journal Entry for Gift Voucher Redemption when SI is Submitted"""

    # Get total amount paid via Gift Vouchers
    gift_voucher_amount = sum(p.amount for p in doc.payments if p.mode_of_payment == "Gift Voucher")

    if not gift_voucher_amount:
        return  # No Gift Voucher payments, so exit

    # Get accounts from Gift Voucher Settings
    gift_voucher_settings = frappe.get_single("Gift Voucher Setting")
    liability_account = gift_voucher_settings.liability_account
    redeemed_account = gift_voucher_settings.redeemed_account

    # Create Journal Entry
    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "posting_date": doc.posting_date,
        "company": doc.company,
        "voucher_type": "Journal Entry",
        "user_remark": f"Gift Voucher Redemption for {doc.name}",
        "accounts": [
            {
                "account": liability_account,
                "debit_in_account_currency": gift_voucher_amount,
                "credit_in_account_currency": 0,
                                    
            },
            {
                "account": redeemed_account,
                "debit_in_account_currency": 0,
                "credit_in_account_currency": gift_voucher_amount,

            }
        ]
    })

    # Submit Journal Entry
    je.insert()
    je.submit()

    # Show success message
    frappe.msgprint(f"""
        <p><b>Journal Entry <span style="color:green;">{je.name}</span> Created for Gift Voucher Redemption.</b></p>
        <p><b>Amount:</b> ₹{gift_voucher_amount}</p>
    """, title="Gift Voucher Journal Entry", indicator="green")