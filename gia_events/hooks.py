from . import __version__ as app_version

app_name = "gia_events"
app_title = "Gia Events"
app_publisher = "Bantoo Accounting"
app_description = "Event Management"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "technical@thebantoo.com"
app_license = "MIT"

# Includes in <head>
# ------------------


# include js, css files in header of desk.html
# app_include_css = "/assets/gia_events/css/gia_events.css"
# app_include_js = "/assets/gia_events/js/gia_events.js"

# include js, css files in header of web template
# web_include_css = "/assets/gia_events/css/gia_events.css"
# web_include_js = "/assets/gia_events/js/gia_events.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "gia_events/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "gia_events.install.before_install"
# after_install = "gia_events.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gia_events.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
    "Request": {
        "after_insert": "gia_events.api.check",
        "validate": "gia_events.api.verify"
	},
    "Lead": {
        "validate": "gia_events.api.insert_attendee",
	},
    "Speaker": {
        "after_insert": "gia_events.api.speaker_row",
	},
    "Event Sponsor": {
        "after_insert": "gia_events.api.sponsor_row",
	},
    "Media Partner": {
        "after_insert": "gia_events.api.media_row",
	},
    "Communication": {
        "after_insert": "gia_events.api.update_link",
	},
    "Newsletter": {
        "after_insert": "gia_events.api.update_link_newsletter",
    },
    "Email Queue": {
        "after_insert": "gia_events.api.add_pixel_tracker",
    },
    "Test Email Campaign": {
        "after_insert": "gia_events.api.add_links",
	},
 }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"gia_events.tasks.all"
# 	],
# 	"daily": [
# 		"gia_events.tasks.daily"
# 	],
# 	"hourly": [
# 		"gia_events.tasks.hourly"
# 	],
# 	"weekly": [
# 		"gia_events.tasks.weekly"
# 	]
# 	"monthly": [
# 		"gia_events.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "gia_events.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "gia_events.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "gia_events.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"gia_events.auth.validate"
# ]

fixtures = [
    {
        "dt": "DocType",
        "filters": [
            [
                "module", "in", [
                    "Gia Events",
                ]
            ]
        ]
    },
    {
        "dt": "Workflow State",
        "filters": [
            [
                "name", "in", [
                    "Already Exists",
                    "Updated",
                    "Verify Attendance",
                    "Clarification",
                    "Email/Call",
                    "Send Form",
                    "Sign Form",
                    "Confirmed",
                    "Contact Lead",
                    "Cancelled",
                    "Pending Verification",
                    "Spam",
                    "Rejected",
                    "Approved",
                    "Pending"
                ]
            ],
        ]

    },
    {
        "dt": "Workflow",
        "filters": [
            [
                "name", "in", [
                    "Verify Lead",
                    "Request Verification"
                ]
            ],
        ]

    },
    {
        "dt": "Custom Field",
        "filters": [
            [
                "name", "in", [
                    "Lead-company_size",
                    "Lead-linkedin_profile_link",
                    "Lead-t",
                    "Lead-whatsapp_phone_number",
                    "Lead-number_of_linkedin_followers",
                    "Lead-company_details",
                    "Sales Order-deal_details",
                    "Sales Order-deal_value",
                    "Sales Order-deal_detail",
                    "Sales Order-starting_date",
                    "Lead-project",
                    "Lead-first_name",
                    "Lead-last_name",
                    "Lead-region",
                    "Lead-segmentation",
                    "Lead-segmentation_no_1",
                    "Lead-column_break_22",
                    "Lead-segmentation_details",
                    "Lead-segmentation_2",
                    "Lead-segmentation_status",
                    "Lead-deal_value",
                    "Lead-event",
                    "Sales Invoice-event",
                    "Email Group-event",
                    "Email Group-hidden",
                    "Email Group-recipient_type",
                    "Email Group Member-event",
                    "Email Group-purpose",
                    "Lead-workflow_state",
                    "Lead-mobile_number",
                    "ToDo-subject",
                    "Communication-gia",
                    "Communication-newsletter",
                    "Communication-communication_status",
                    "Communication-email_links",
                    "Request-workflow_state",
                    "Lead-lead_requests",
                    "Lead-requests"
                ]
            ],
        ]

    },
    {
        "dt": "Notification",
        "filters": [
            [
                "name", "in", [
                    "Welcome Email",
                    "New Lead"
                ]
            ],
        ]

    },
    {
        "dt": "Report",
        "filters": [
            [
                "name", "in", [
                    "Event Attendance",
                    "Speaker Attendance",
                    "Media Partner Attendance",
                    "Event Sponsors",
                    "Email Analytics"
                ]
            ],
        ]

    },
    {
        "dt": "Dashboard Chart",
        "filters": [
            [
                "name", "in", [
                    "Request Forms"
                ]
            ],
        ]

    },
    {
        "dt": "Workspace",
        "filters": [
            [
                "name", "in", [
                    "GIA Events"
                ]
            ],
        ]

    },
    {
        "dt": "Client Script",
        "filters": [
            [
                "name", "in", [
                    "Lead-Form",
                    "Contact-Form",
                    "Call Log GIA-Form",
                ]
            ],
        ]

    },
]