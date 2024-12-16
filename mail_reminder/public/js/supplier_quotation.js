// Copyright (c) 2024, scopen.fr and contributors
// For license information, please see license.txt

frappe.ui.form.on("Supplier Quotation", {
  supplier: function (frm) {
    frappe.db.get_value(
      "Supplier",
      { name: frm.doc.supplier },
      ["automatic_mail_reminder"],
      function (value) {
        frm.set_value("automatic_mail_dunning", value.automatic_mail_reminder);
      }
    );
  },
});
