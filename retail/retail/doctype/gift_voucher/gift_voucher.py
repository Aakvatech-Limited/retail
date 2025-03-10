import frappe
from frappe.model.document import Document

class GiftVoucher(Document):
    def validate(self):
        """Validate bulk quantity before saving."""
        if self.is_bulk and (not self.bulk_qty or self.bulk_qty <= 1):
            frappe.throw("Bulk quantity must be greater than 1 when bulk creation is enabled.")

    def before_insert(self):
        """If bulk creation is enabled, create multiple draft vouchers."""
        if self.is_bulk:
            self.create_bulk_vouchers()

    def on_submit(self):
        """Assign serial number when a voucher is submitted."""
        if not self.gift_voucher_code:
            self.assign_serial_number()

    def assign_serial_number(self):
        """Assign a serial number upon submission."""
        if frappe.db.exists("Serial No", self.name):
            return

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

        

    def create_bulk_vouchers(self):
        """Create multiple draft gift voucher documents before inserting the first one."""
        for _ in range(self.bulk_qty - 1): 
            new_voucher = frappe.get_doc({
                "doctype": "Gift Voucher",
                "initial_balance": self.initial_balance,
                "is_bulk": 0,
                "docstatus": 0
            })
            new_voucher.insert(ignore_permissions=True)

        frappe.msgprint(
            f"<b>Total {self.bulk_qty} Draft Gift Vouchers Created!</b><br>"
            f"Submit them to generate serial numbers.",
            title="Success",
            indicator="blue"
        )
