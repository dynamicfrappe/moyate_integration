# Copyright (c) 2025, Dynamic Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.accounts.report.customer_ledger_summary.customer_ledger_summary import execute as execute_customer
from erpnext.accounts.report.supplier_ledger_summary.supplier_ledger_summary import execute as execute_supplier

class MonthlyAccountStatement(Document):
	pass

@frappe.whitelist()
def get_balance(party_type , party ):
	res = 0
	if party_type == "Customer":
		res = get_closing_balance_for_customer(party_type , party )
	elif party_type == "Supplier":
		res = get_closing_balance_for_supplier(party_type , party)

	return res


@frappe.whitelist()
def get_closing_balance_for_supplier(party_type , party):
	company = frappe.defaults.get_user_default("Company")
	from_date = frappe.defaults.get_user_default("fiscal_year_start_date")
	to_date = frappe.utils.today()
	supplier_name = frappe.get_value( party_type, party , "supplier_name")
	filters = {
		"from_date": from_date,
		"to_date": to_date,
		"company": company,
		"party_type": party_type,
		"party": party,
		"party_name": supplier_name
	}
	data = execute_supplier(filters)
	if data and data[1] and data[1][0]:
		return data[1][0].get("closing_balance")
	else:
		return 0

@frappe.whitelist()
def get_closing_balance_for_customer(party_type , party):
	company = frappe.defaults.get_user_default("Company")
	from_date = frappe.defaults.get_user_default("fiscal_year_start_date")
	to_date = frappe.utils.today()
	customer_name = frappe.get_value( party_type , party , "customer_name")
	filters = {
		"from_date": from_date,
		"to_date": to_date,
		"company": company,
		"party_type": party_type,
		"party": party,
		"party_name": customer_name
	}
	data = execute_customer(filters)
	if data and data[1] and data[1][0]:
		return data[1][0].get("closing_balance")
	else:
		return 0