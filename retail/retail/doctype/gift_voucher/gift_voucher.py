import frappe
from frappe.model.document import Document
from frappe.utils import today, add_days, get_link_to_form
from frappe.model.docstatus import DocStatus

class GiftVoucher(Document):
    def validate(self):
        """Validate bulk quantity before saving."""
        if self.is_bulk and (not self.bulk_qty or self.bulk_qty <= 1):
            frappe.throw("Bulk quantity must be greater than 1 when bulk creation is enabled.")

    def before_insert(self):
        """If bulk creation is enabled, create multiple draft vouchers."""
        if self.is_bulk:
            self.create_bulk_vouchers()

        # Set initial status to 'Created'
        self.status = "Created"
        self.current_balance = self.opening_balance
        self.gift_voucher_code = self.name

    def before_save(self):
        if self.status == "Created":
            self.current_balance = self.opening_balance


    def create_bulk_vouchers(self):
        """Create multiple draft gift voucher documents before inserting the first one."""
        for _ in range(self.bulk_qty - 1):
            new_voucher = frappe.get_doc({
                "doctype": "Gift Voucher",
                "opening_balance": self.opening_balance,
                "current_balance": self.opening_balance,
                "is_bulk": 0,
                "docstatus": 0,
                "status": "Created"
            })
            new_voucher.insert(ignore_permissions=True)
       
        frappe.msgprint(
            f"<b>Total {self.bulk_qty} Draft Gift Vouchers Created!</b><br>"
            f"Submit them to generate the Gift Vouchers.<br>",
            title="Success",
            indicator="blue"
        )
