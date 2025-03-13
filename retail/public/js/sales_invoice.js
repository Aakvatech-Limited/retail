frappe.ui.form.on("Sales Invoice", {
  refresh: function (frm) {
    console.log("Sales Invoice refresh");
  },
  setup(frm) {
    frm.set_query(
      "custom_gift_voucher_code",
      "items",
      function (doc, cdt, cdn) {
        return {
          filters: {
            status: "Created",
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
          "initial_balance"
        )
        .then((r) => {
          if (r.message.initial_balance) {
            frappe.model.set_value(cdt, cdn, "rate", r.message.initial_balance);
          }
        });
    }
  },
});
