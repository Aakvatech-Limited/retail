import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    fields = {
        "Sales Invoice Item": [
            {
                "fieldname": "custom_gift_voucher_details",
                "fieldtype": "Section Break",
                "insert_after": "brand",
                "label": "Gift Voucher Details",
                "depends_on": "eval:doc.item_code == \"Gift Voucher\"",
               
            },
            {
                "fieldname": "custom_gift_voucher_code",
                "fieldtype": "Link",
                "insert_after": "custom_gift_voucher_details",
                "label": "Gift Voucher Code",
                "options": "Gift Voucher",
                "mandatory_depends_on": "eval:doc.item_code == \"Gift Voucher\"",
                "no_copy": 1
            },
             {
                "fieldname": "custom_gift_voucher_amount",
                "fieldtype": "Currency",
                "fetch_from": "custom_gift_voucher_code.opening_balance",
                "insert_after": "custom_gift_voucher_code",
                "label": "Gift Voucher Amount",
                "no_copy": 1,
                "read_only": 1,
                "depends_on": "eval:doc.custom_gift_voucher_code",
            },
            
            
        ],
         "Sales Invoice Payment": [
            {
                "fieldname": "custom_gift_voucher_details",
                "fieldtype": "Section Break",
                "insert_after": "clearance_date",
                "label": "Gift Voucher Details",
                "depends_on": "eval:doc.mode_of_payment == \"Gift Voucher\"",
               
            },
            {
                "fieldname": "custom_gift_voucher_code",
                "fieldtype": "Link",
                "insert_after": "custom_gift_voucher_details",
                "label": "Gift Voucher Code",
                "options": "Gift Voucher",
                "mandatory_depends_on": "eval:doc.mode_of_payment == \"Gift Voucher\"",
                "no_copy": 1
            },
             {
                "fieldname": "custom_gift_voucher_current_balance",
                "fieldtype": "Currency",
                "fetch_from": "custom_gift_voucher_code.current_balance",
                "insert_after": "custom_gift_voucher_code",
                "label": "Gift Voucher Current Balance",
                "no_copy": 1,
                "read_only": 1,
                "depends_on": "eval:doc.custom_gift_voucher_code",
                
            },
            
            
        ],
        
       
        
    }

    create_custom_fields(fields, update=True)