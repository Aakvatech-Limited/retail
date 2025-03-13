// Copyright (c) 2025, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Gift Voucher", {
  refresh: function (frm) {
    if (!frm.doc.__islocal) {
      // Only change title for saved documents
      frm.set_title(frm.doc.status || "Gift Voucher");
    }
  },
});
