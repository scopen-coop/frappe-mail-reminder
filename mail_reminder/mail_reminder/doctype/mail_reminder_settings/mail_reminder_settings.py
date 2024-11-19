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
