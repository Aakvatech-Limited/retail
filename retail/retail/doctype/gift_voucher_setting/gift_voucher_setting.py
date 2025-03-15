# Copyright (c) 2025, Talib Sheikh and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class GiftVoucherSetting(Document):
    def on_update(self):
        """Enable or disable Gift Voucher settings and link accounts & mode of payment."""
        if self.enable_gift_voucher_system:
            self.setup_gift_voucher(enabled=True)
        else:
            self.setup_gift_voucher(enabled=False)

    def setup_gift_voucher(self, enabled):
        """Handles enabling/disabling of the Gift Voucher system and links settings."""
        # Ensure accounts exist before setting them
        liability_account = self.manage_account("Gift Voucher Liability", "Current Liabilities", "Liability", enabled)
        redeemed_account = self.manage_account("Gift Voucher Redeemed", "Indirect Income", "Income Account", enabled)
        revenue_account = self.manage_account("Gift Voucher Revenue", "Indirect Income", "Income Account", enabled)

        # Set values only when enabling
        if enabled:
            frappe.db.set_value("Gift Voucher Setting", self.name, {
                "liability_account": liability_account,
                "redeemed_account": redeemed_account,
                "revenue_account": revenue_account
            })

        # Ensure Mode of Payment exists after accounts are set
        mode_of_payment = self.manage_mode_of_payment(enabled, redeemed_account)

        # Update Mode of Payment in settings only when enabling
        if enabled:
            frappe.db.set_value("Gift Voucher Setting", self.name, "mode_of_payment", mode_of_payment)

        # Manage Gift Voucher item
        self.manage_gift_voucher_item(enabled, revenue_account)

    def get_company_details(self):
        """Fetch default company and abbreviation."""
        default_company = frappe.defaults.get_defaults().get("company")
        if not default_company:
            frappe.throw("Default company not found. Please set it in Company settings.")
        company_abbr = frappe.get_value("Company", default_company, "abbr")
        return default_company, company_abbr

    def manage_account(self, account_name, parent_group, account_type, enabled):
        """Create or enable/disable an account and return its name."""
        default_company, company_abbr = self.get_company_details()
        full_account_name = f"{account_name} - {company_abbr}"

        # Check if the account exists
        if frappe.db.exists("Account", full_account_name):
            frappe.db.set_value("Account", full_account_name, "disabled", not enabled)
        elif enabled:
            # Create new account
            account = frappe.get_doc({
                "doctype": "Account",
                "account_name": account_name,
                "parent_account": f"{parent_group} - {company_abbr}",
                "account_type": account_type,
                "company": default_company,
                "is_group": 0,
                "disabled": 0
            })
            account.insert(ignore_permissions=True)

        status = "enabled" if enabled else "disabled"
        frappe.msgprint(f"Account '{full_account_name}' {status}.")
        return full_account_name  # Return account name for linking in settings

    def manage_gift_voucher_item(self, enabled, revenue_account):
        """Create or enable/disable the 'Gift Voucher' item."""
        item_code = "Gift Voucher"
        default_company, company_abbr = self.get_company_details()

        if not revenue_account:
            frappe.throw("Revenue account is missing. Please check Gift Voucher settings.")

        if frappe.db.exists("Item", item_code):
            frappe.db.set_value("Item", item_code, "disabled", not enabled)
        elif enabled:
            frappe.get_doc({
                "doctype": "Item",
                "item_code": item_code,
                "item_name": "Gift Voucher",
                "item_group": "Services",
                "is_stock_item": 0,
                "stock_uom": "Nos",
                "disabled": 0,
                "item_defaults": [{"company": default_company, "income_account": revenue_account}]
            }).insert(ignore_permissions=True)

        status = "enabled" if enabled else "disabled"
        frappe.msgprint(f"Item '{item_code}' {status}.")

    def manage_mode_of_payment(self, enabled, redeemed_account):
        """Create or enable/disable the 'Gift Voucher' mode of payment and return its name."""
        default_company, company_abbr = self.get_company_details()
        mode_of_payment = "Gift Voucher"

        if not redeemed_account:
            frappe.throw("Redeemed account is missing. Please check Gift Voucher settings.")

        if frappe.db.exists("Mode of Payment", mode_of_payment):
            frappe.db.set_value("Mode of Payment", mode_of_payment, "enabled", enabled)
        elif enabled:
            frappe.get_doc({
                "doctype": "Mode of Payment",
                "mode_of_payment": mode_of_payment,
                "type": "General",
                "enabled": 1,
                "accounts": [{"company": default_company, "default_account": redeemed_account}]
            }).insert(ignore_permissions=True)

        status = "enabled" if enabled else "disabled"
        frappe.msgprint(f"Mode of Payment '{mode_of_payment}' {status}.")
        return mode_of_payment  # Return the mode of payment name for linking in settings
