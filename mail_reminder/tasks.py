import frappe

from datetime import timedelta
from frappe import _
from frappe.email.doctype.email_template.email_template import get_email_template
from frappe.utils import date_diff, nowdate, now


def mail_reminder():
    related_documents = dict()
    # Get the document types set ine the mail reminder settings
    set_documents_settings = frappe.get_all(
        "Mail Reminder Item",
        fields=[
            "document",
            "mail_model",
            "time_between_reminders",
            "mail_account_sender",
        ],
    )

    # Get the documents concerned by the automatic reminder
    for item in set_documents_settings:
        related_documents[item.document] = frappe.get_all(
            item.document,
            fields=["*"],
            # filters={"automatic_mail_dunning": True, "docstatus": 2}, #TODO : replace filters with this line when test finished
            filters={"automatic_mail_dunning": True},
        )

    for key in related_documents:
        for item in set_documents_settings:
            if item.document == key:
                mail_model = item.mail_model
                mail_account_sender = item.mail_account_sender
                days_between_reminders = timedelta(
                    seconds=item.time_between_reminders
                ).days

        for i in range(len(related_documents[key])):
            current_doc = related_documents[key][i]

            # Testing if there is a contact on the current document and if it has an email set
            if current_doc.contact_person == "" or current_doc.contact_email == "":
                print(
                    _(
                        "Document '{0}' has no contact person or no email correctly set.\n"
                    ).format(current_doc.name)
                )
                continue

            # Testing if the document never or has been dunned in the period set in the mail reminder settings
            if (
                current_doc.last_automatic_mail_dunning_date is not None
                and date_diff(nowdate(), current_doc.last_automatic_mail_dunning_date)
                < days_between_reminders
            ):
                continue

            template = get_email_template(mail_model, current_doc)

            frappe.sendmail(
                recipients=["yannishoareau26@gmail.com"],
                sender=mail_account_sender,
                subject=template["subject"],
                message=template["message"],
            )

            frappe.get_doc(key, current_doc.name).add_comment(
                "Label",
                _("sent a reminder to {0} via {1}").format(
                    current_doc.contact_display, current_doc.contact_email
                ),
            )

            # TODO : determine which one is the best
            # doc.add_comment("Comment", "text comment", "comment@comment.fr", "by Comment")
            # doc.add_comment("Workflow", "text workflow", "workflow@workflow.fr", "by workflow")
            # doc.add_comment("Attachment", "text attachment", "attachment@attachment.fr", "by attachment")

            frappe.db.set_value(
                key, current_doc.name, "last_automatic_mail_dunning_date", now()
            )
            frappe.db.commit()
