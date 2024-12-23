// Copyright (c) 2024, Scopen and contributors
// For license information, please see license.txt

let available_status = [];

frappe.ui.form.on("Mail Reminder Settings", {
  setup() {
    frappe.call({
      method:
        "mail_reminder.mail_reminder.doctype.mail_reminder_settings.mail_reminder_settings.get_available_status_per_doctype",
      async: false,
      callback(r) {
        if (r.message) {
          available_status = r.message;
        }
      },
    });
  },

  refresh(frm) {
    for (let row of frm.fields_dict["mail_reminder"].grid.grid_rows) {
      let statusField = row?.docfields?.find((d) => d.fieldname === "status");
      if (statusField) {
        statusField["options"] = available_status[row.doc.document];
      }
    }
  },
});

frappe.ui.form.on("Mail Reminder Item", "document", function (frm, cdt, cdn) {
  let row_dt = frappe.get_doc(cdt, cdn);
  frm.set_df_property(
    "mail_reminder",
    "options",
    available_status[row_dt.document],
    frm.docname,
    "status",
    row_dt.name
  );
});
