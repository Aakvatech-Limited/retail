frappe.ui.form.on("Sales Invoice", {
  setup(frm) {
    // filter - `Created` Gift Vouchers
    frm.set_query(
      "custom_gift_voucher_code",
      "items",
      function (doc, cdt, cdn) {
        return {
          filters: {
            status: "Created",
            docstatus: 1,
          },
        };
      }
    );
    // filter - `Active` Gift Vouchers
    frm.set_query(
      "custom_gift_voucher_code",
      "payments",
      function (doc, cdt, cdn) {
        return {
          filters: {
            status: "Active",
          },
        };
      }
    );
  },
});

frappe.ui.form.on("Sales Invoice Item", {
  custom_gift_voucher_code: function (frm, cdt, cdn) {
    let row = locals[cdt][cdn]; // Get the selected row from child table

    if (row.custom_gift_voucher_code) {
      frappe.db
        .get_value(
          "Gift Voucher",
          row.custom_gift_voucher_code,
          "opening_balance"
        )
        .then((r) => {
          if (r.message.opening_balance) {
            frappe.model.set_value(cdt, cdn, "rate", r.message.opening_balance);
          }
        });
    }
  },
});

frappe.ui.form.on("Sales Invoice Payment", {});
