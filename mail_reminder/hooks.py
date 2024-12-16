app_name = "mail_reminder"
app_title = "Mail Reminder"
app_publisher = "Scopen"
app_description = "Mail reminder application"
app_email = "contact@scopen.fr"
app_license = "gpl-3.0"

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                (
                    "Customer-automatic_mail_reminder",
                    "Purchase Order-section_break_vxxkz",
                    "Purchase Order-automatic_mail_dunning",
                    "Purchase Order-last_automatic_mail_dunning_date",
                    "Sales Invoice-section_break_11c8n",
                    "Sales Invoice-automatic_mail_dunning",
                    "Sales Invoice-last_automatic_mail_dunning_date",
                    "Sales Order-section_break_rkngy",
                    "Sales Order-automatic_mail_dunning",
                    "Sales Order-last_automatic_mail_dunning_date",
                    "Supplier-automatic_mail_reminder",
                    "Supplier Quotation-automatic_mail_dunning",
                    "Supplier Quotation-last_automatic_mail_dunning_date",
                    "Supplier Quotation-section_break_rzuok",
                ),
            ],
        ],
    }
]

# include js in doctype views

doctype_js = {
    "Purchase Order": ["public/js/purchase_order.js"],
    "Sales Invoice": ["public/js/sales_invoice.js"],
    "Sales Order": ["public/js/sales_order.js"],
    "Supplier Quotation": ["public/js/supplier_quotation.js"],
}


# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": ["mail_reminder.tasks.mail_reminder"],
}
