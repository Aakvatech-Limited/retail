import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form

class GiftVoucher(Document):
    def on_submit(self):
        """Set voucher name as serial number if not already set."""
        if self.gift_voucher_code:
            return
        if not frappe.db.exists("Serial No", self.name):
            frappe.get_doc({
                "doctype": "Serial No",
                "serial_no": self.name,
                "item_code": "Gift Voucher"
            }).insert(ignore_permissions=True)
        self.db_set("gift_voucher_code", self.name)
        frappe.msgprint(
            f"<b>Gift Voucher Created Successfully!</b><br>"
            f"Serial Number: {get_link_to_form('Serial No', self.name)}",
            title="Success",
            indicator="green"
        )