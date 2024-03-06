# Copyright (c) 2024, moyate_integration and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from moyate_integration.moyate_integration.utils.integration import create_repzo_id
class RepzoIntegration(Document):
	def validate(self) :
		create_repzo_id()
