# Copyright (c) 2024, Scopen and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MailReminderSettings(Document):
    def before_save(self):
        list_of_items = []

        for item in self.mail_reminder:
            if item.document not in list_of_items:
                list_of_items.append(item.document)
            else:
                frappe.throw("Unable to have two rows for the same document")


@frappe.whitelist()
def get_available_status_per_doctype():
    status_available = {}
    # for doctype in frappe.get_meta("Mail Reminder Item").get_field("document").link_filters.split("\n"):
    for doctype in [
        "Supplier Quotation",
        "Purchase Order",
        "Sales Order",
        "Sales Invoice",
    ]:
        if frappe.get_meta(doctype).has_field("status"):
            status_available[doctype] = (
                frappe.get_meta(doctype).get_field("status").options.split("\n")
            )

    if status_available:
        return status_available
    else:
        return []
