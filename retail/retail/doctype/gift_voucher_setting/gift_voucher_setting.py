# Copyright (c) 2025, Talib Sheikh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GiftVoucherSetting(Document):
    def on_update(self):
        if self.enable_gift_voucher_system:
            create_or_enable_gift_voucher_redeemed_account()
            create_or_enable_gift_voucher_liability_account()
            create_or_enable_gift_voucher_revenue_account()
            enable_gift_voucher_item()
        else:
            disable_gift_voucher_item()
            disable_gift_voucher_redeemed_account()
            disable_gift_voucher_liability_account()
            disable_gift_voucher_revenue_account()


def get_company_details():
    """Returns default company and abbreviation"""
    default_company = frappe.defaults.get_defaults().get("company")
    if not default_company:
        frappe.throw("Default company not found. Please set it in Company settings.")
    
    company_abbr = frappe.get_value("Company", default_company, "abbr")
    return default_company, company_abbr


def enable_gift_voucher_item():
    """Create or enable the Gift Voucher item and set default income account."""
    item_code = "Gift Voucher"
    default_company, company_abbr = get_company_details()

    income_account = f"Gift Voucher Liability - {company_abbr}"

    if frappe.db.exists("Item", item_code):
        frappe.db.set_value("Item", item_code, "disabled", 0)
        frappe.msgprint(f"Gift Voucher item '{item_code}' enabled.")
    else:
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": "Gift Voucher",
            "item_group": "Services",  
            "is_stock_item": 0,  
            "stock_uom": "Nos",
            "disabled": 0,  
            "item_defaults": [
                {
                    "company": default_company,
                    "income_account": income_account
                }
            ]
        })
        item.insert(ignore_permissions=True)
        frappe.msgprint(f"Gift Voucher item '{item_code}' created and enabled.")


def disable_gift_voucher_item():
    """Disable the Gift Voucher item if it exists."""
    item_code = "Gift Voucher"

    if frappe.db.exists("Item", item_code):
        frappe.db.set_value("Item", item_code, "disabled", 1)
        frappe.msgprint(f"Gift Voucher item '{item_code}' has been disabled.")


def create_or_enable_gift_voucher_redeemed_account():
    """Create or enable 'Gift Voucher Redeemed' account."""
    default_company, company_abbr = get_company_details()
    account_name = f"Gift Voucher Redeemed - {company_abbr}"

    if frappe.db.exists("Account", account_name):
        frappe.db.set_value("Account", account_name, "disabled", 0)
        frappe.msgprint(f"Account '{account_name}' enabled.")
    else:
        account = frappe.get_doc({
            "doctype": "Account",
            "account_name": "Gift Voucher Redeemed",
            "parent_account": f"Indirect Income - {company_abbr}",
            "account_type": "Income Account",
            "company": default_company,
            "is_group": 0,
            "disabled": 0
        })
        account.insert(ignore_permissions=True)
        frappe.msgprint(f"Account '{account_name}' created and enabled under 'Indirect Income'.")


def disable_gift_voucher_redeemed_account():
    """Disable the 'Gift Voucher Redeemed' account if it exists."""
    default_company, company_abbr = get_company_details()
    account_name = f"Gift Voucher Redeemed - {company_abbr}"

    if frappe.db.exists("Account", account_name):
        frappe.db.set_value("Account", account_name, "disabled", 1)
        frappe.msgprint(f"Account '{account_name}' has been disabled.")


def create_or_enable_gift_voucher_liability_account():
    """Create or enable 'Gift Voucher Liability' account."""
    default_company, company_abbr = get_company_details()
    account_name = f"Gift Voucher Liability - {company_abbr}"

    if frappe.db.exists("Account", account_name):
        frappe.db.set_value("Account", account_name, "disabled", 0)
        frappe.msgprint(f"Account '{account_name}' enabled.")
    else:
        account = frappe.get_doc({
            "doctype": "Account",
            "account_name": "Gift Voucher Liability",
            "parent_account": f"Current Liabilities - {company_abbr}",
            "account_type": "Liability",
            "company": default_company,
            "is_group": 0,
            "disabled": 0
        })
        account.insert(ignore_permissions=True)
        frappe.msgprint(f"Account '{account_name}' created and enabled under 'Current Liabilities'.")


def disable_gift_voucher_liability_account():
    """Disable the 'Gift Voucher Liability' account if it exists."""
    default_company, company_abbr = get_company_details()
    account_name = f"Gift Voucher Liability - {company_abbr}"

    if frappe.db.exists("Account", account_name):
        frappe.db.set_value("Account", account_name, "disabled", 1)
        frappe.msgprint(f"Account '{account_name}' has been disabled.")


def create_or_enable_gift_voucher_revenue_account():
    """Create or enable 'Gift Voucher Revenue' account."""
    default_company, company_abbr = get_company_details()
    account_name = f"Gift Voucher Revenue - {company_abbr}"

    if frappe.db.exists("Account", account_name):
        frappe.db.set_value("Account", account_name, "disabled", 0)
        frappe.msgprint(f"Account '{account_name}' enabled.")
    else:
        account = frappe.get_doc({
            "doctype": "Account",
            "account_name": "Gift Voucher Revenue",
            "parent_account": f"Indirect Income - {company_abbr}",
            "account_type": "Income Account",
            "company": default_company,
            "is_group": 0,
            "disabled": 0
        })
        account.insert(ignore_permissions=True)
        frappe.msgprint(f"Account '{account_name}' created and enabled under 'Indirect Income'.")


def disable_gift_voucher_revenue_account():
    """Disable the 'Gift Voucher Revenue' account if it exists."""
    default_company, company_abbr = get_company_details()
    account_name = f"Gift Voucher Revenue - {company_abbr}"

    if frappe.db.exists("Account", account_name):
        frappe.db.set_value("Account", account_name, "disabled", 1)
        frappe.msgprint(f"Account '{account_name}' has been disabled.")
