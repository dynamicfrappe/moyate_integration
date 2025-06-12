from . import __version__ as app_version

app_name = "moyate_integration"
app_title = "moyate_integration"
app_publisher = "Dynamic Business Solutions"
app_description = "moyate_integration integrate with repzo "
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "dynmaic@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/moyate_integration/css/moyate_integration.css"
# app_include_js = "/assets/moyate_integration/js/moyate_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/moyate_integration/css/moyate_integration.css"
# web_include_js = "/assets/moyate_integration/js/moyate_integration.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "moyate_integration/public/scss/website"

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

# before_install = "moyate_integration.install.before_install"
# after_install = "moyate_integration.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "moyate_integration.uninstall.before_uninstall"
# after_uninstall = "moyate_integration.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "moyate_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }
after_migrate = [
    "moyate_integration.install.after_install"
]
after_install = [	
    "moyate_integration.install.after_install"
	]



doc_events = {
    "Sales Invoice" : {
        "on_submit" :"moyate_integration.controllers.sales_invoice.submit_sales_invoice" ,
        "validate" :"moyate_integration.controllers.sales_invoice.validate_sales_invoice",
        "on_update_after_submit" : "moyate_integration.controllers.sales_invoice.change_sales_person_commission_log"
	 } ,
     "Delivery Note": {
        "on_submit" :"moyate_integration.controllers.sales_invoice.submit_delivery_note"
	 } ,
     "Purchase Receipt" :{
         "on_submit" : "moyate_integration.controllers.purchase_invoice.submit_purchase_receipt"
	 } ,
      "Purchase Invoice" :{
         "on_submit" : "moyate_integration.controllers.purchase_invoice.submit_purchase_invoice"
	 } , 
     "Stock Entry" : {
         "on_submit" : "moyate_integration.controllers.stock_entry.submit_stock_entry"
	 }
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"moyate_integration.tasks.all"
#	],
#	"daily": [
#		"moyate_integration.tasks.daily"
#	],
#	"hourly": [
#		"moyate_integration.tasks.hourly"
#	],
#	"weekly": [
#		"moyate_integration.tasks.weekly"
#	]
#	"monthly": [
#		"moyate_integration.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "moyate_integration.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "moyate_integration.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "moyate_integration.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["moyate_integration.utils.before_request"]
# after_request = ["moyate_integration.utils.after_request"]

# Job Events
# ----------
# before_job = ["moyate_integration.utils.before_job"]
# after_job = ["moyate_integration.utils.after_job"]

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
#	"moyate_integration.auth.validate"
# ]

domains = {
    "Repzo": "moyate_integration.domains.moyate_integration",
}
#

scheduler_events = {
    "cron": {
		"0/5 * * * *": ["moyate_integration.moyate_integration.utils.integration.sync_now",
					]
        }
}

#from moyate_integration.moyate_integration.utils.integration  import sync_now
