import frappe
from frappe.utils import add_days

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

            # If Gift Voucher is in Draft, submit it
            if gift_voucher.docstatus == 0:
                gift_voucher.docstatus = 1  # Submit the document

            gift_voucher.save()

            frappe.msgprint(f"Gift Voucher {gift_voucher.name} activated. Issue Date: {gift_voucher.issue_date}, Expiration Date: {gift_voucher.expiration_date}")
