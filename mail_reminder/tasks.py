from datetime import timedelta

import frappe
from frappe import get_email_from_template
from frappe.utils import date_diff, nowdate


def all():
    pass


def daily():
    pass


def hourly():
    pass


def weekly():
    pass


def monthly():
    pass


def cron():
    related_documents = dict()
    set_documents = frappe.get_all(
        "Mail Reminder Item",
        fields=[
            "document",
            "mail_model",
            "time_between_reminders",
            "mail_account_sender",
        ],
    )

    for item in set_documents:
        related_documents[item.document] = frappe.get_all(
            item.document,
            fields=[
                "name",
                "docstatus",
                "automatic_mail_dunning",
                "last_automatic_mail_dunning_date",
                "contact_person",
                "contact_email",
            ],
            # fields=["*"],
            filters={"automatic_mail_dunning": True},
        )  # TODO : Add filter on docstatus where it's equal to 2
    for key in related_documents:
        current_doc = related_documents[key][0]
        for item in set_documents:
            if item.document == key:
                days_between_reminders = timedelta(
                    seconds=item.time_between_reminders
                ).days
                mail_model = item.mail_model
                mail_account_sender = item.mail_account_sender

        print(
            date_diff(nowdate(), current_doc.last_automatic_mail_dunning_date),
            days_between_reminders,
        )
        if (
            current_doc.last_automatic_mail_dunning_date is not None
            and date_diff(nowdate(), current_doc.last_automatic_mail_dunning_date)
            < days_between_reminders
        ):
            print("skipped\n")
            # continue

        print("changed\n")
        # frappe.db.set_value(key, current_doc.name, 'last_automatic_mail_dunning_date', nowdate())
        # frappe.db.set_value(key, current_doc.name, 'last_automatic_mail_dunning_date', '2024-11-13')
        # frappe.db.commit()

        args = {
            "contact_person": current_doc.contact_person,
            "contact_email": current_doc.contact_email,
            "name": current_doc.name,
        }
        html = get_email_from_template(mail_model, args)
        print("test", html)

        frappe.sendmail(
            recipients=["yannis.hoareau@scopen.fr"],
            template=mail_model,
            args=args,
            sender=mail_account_sender,
        )

    # print(json.dumps(related_documents, default=str, indent=4))
