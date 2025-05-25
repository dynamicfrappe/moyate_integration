import frappe
import os
import json



def after_install():
	create_domain_list()

def create_domain_list():
	if not frappe.db.exists("Domain", "Repzo"):
		dm1 = frappe.new_doc("Domain")
		dm1.domain = 'Repzo'
		dm1.insert()
	
