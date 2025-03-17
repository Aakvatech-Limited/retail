import frappe
from frappe.utils import today

def check_gift_voucher_status():
    """Checks and updates the status of Gift Vouchers based on balance and expiry"""
    
    try:
        
        # Check for expired vouchers and create journal entries
        expired_vouchers = frappe.get_all("Gift Voucher", filters={"status": "Active", "expiration_date": ("<=", today())}, fields=["name", "current_balance"])
        for voucher in expired_vouchers:
            try:
                if voucher.current_balance > 0:
                    create_expiry_journal_entry(voucher.name, voucher.current_balance)

                frappe.db.set_value("Gift Voucher", voucher.name, "status", "Expired")
            except Exception as e:
                frappe.log_error(f"Error updating status to Expired for {voucher.name}: {str(e)}")

    except Exception as e:
        frappe.log_error(f"Unexpected error in Gift Voucher expiry job: {str(e)}")

def create_expiry_journal_entry(voucher_name, amount):
    """Creates a journal entry to move liability to revenue on expiry"""
    
    try:
        settings = frappe.get_single("Gift Voucher Setting")
        liability_account = settings.liability_account
        revenue_account = settings.revenue_account

        je = frappe.get_doc({
            "doctype": "Journal Entry",
            "posting_date": today(),
            "accounts": [
                {
                    "account": liability_account,
                    "debit_in_account_currency": amount
                },
                {
                    "account": revenue_account,
                    "credit_in_account_currency": amount
                }
            ],
            "voucher_type": "Journal Entry",
            "remark": f"Gift Voucher {voucher_name} expired, moving {amount} from liability to revenue"
        })
        je.insert()
        je.submit()
    except Exception as e:
        frappe.log_error(f"Error creating journal entry for expired Gift Voucher {voucher_name}: {str(e)}")
