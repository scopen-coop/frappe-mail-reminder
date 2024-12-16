// Copyright (c) 2024, scopen.fr and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Order", {
  customer: function (frm) {
    frappe.db.get_value(
      "Customer",
      { name: frm.doc.customer },
      ["automatic_mail_reminder"],
      function (value) {
        frm.set_value("automatic_mail_dunning", value.automatic_mail_reminder);
      }
    );
  },
});
