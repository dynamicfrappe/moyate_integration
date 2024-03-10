import frappe 
from frappe import _ 
from frappe.utils import nowdate, now_datetime

from moyate_integration.moyate_integration.utils.repzo import repzo_document_create ,repzo_document_update
from datetime import datetime, timedelta

def create_custom_field(doctype) :

   """
   create custom field after save Repzo Integration
   
   """
   doc = frappe.get_doc("DocType" ,doctype)
   # insert after last two fields in the doctype 

   insert_after =  doc.fields[-2].fieldname
   field = frappe.new_doc("Custom Field")
   field.dt = doctype 
   field.label = "Repzo Id"
   field.fieldname = "repzo_id"
   field.insert_after = insert_after 
   field.fieldtype = "Data"
   field.read_only = 1
   field.save()
   frappe.db.commit()
   frappe.msgprint(f"""Depzo Id Created for {doctype} """)

def create_repzo_id(doctype=False):


   """
   param doctype 
      if doctype create repzo id for single doctype else create all 
   create custom field with name repzo_id if not found 
   repzo = get_repzo_setting()

   """

   if doctype :
      if not frappe.db.exists("Custom Field" ,{"dt" :doctype , "fieldname" :'repzo_id'}) :
         create_custom_field(doctype)

   else :
      """
      create Custom field for all docs
      """
      repzo = frappe.get_single("Repzo Integration")
      for i in repzo.items :
         if not frappe.db.exists("Custom Field" ,{"dt" :i.document , "fieldname" :'repzo_id'}) :
            create_custom_field(i.document)
   return True
      

@frappe.whitelist()
def make_sync():
   """
   create all synced doctype without repzo id 
   """
   repzo = frappe.get_single("Repzo Integration")
   added_minutes = repzo.minutes
   for i in repzo.items :
      if not i.last_update  :
            repzo_document_create(i.document)
            last_update = now_datetime()
            frappe.db.sql(f""" UPDATE `tabRepzo Integration Doctypes` SET last_update = '{last_update}'
            WHERE name ='{i.name}' """)
            frappe.db.commit()
      if i.last_update :
         current_date = now_datetime()
         # add hour to last update date 
         update_on = i.last_update + timedelta(minutes=int(added_minutes))
         if current_date > update_on :
            print("current_date greater than update on ")
            filters ={"creation":[">=", update_on ]}
            repzo_document_create(i.document ,filters)
            frappe.db.sql(f""" UPDATE `tabRepzo Integration Doctypes` SET last_update = '{current_date}'
                          WHERE name ='{i.name}' """)
            frappe.db.commit()
         if current_date < update_on :
            print("current_date less than update on ")
   return True
@frappe.whitelist()
def make_sync_updated_data():
   repzo = frappe.get_single("Repzo Integration")
   added_minutes = repzo.minutes
   for i in repzo.items :
      if i.last_update :
         current_date = now_datetime()
         update_on = i.last_update + timedelta(minutes=int(added_minutes))
         if current_date > update_on :
            filters ={"modified":[">=", update_on ]}
            repzo_document_update(i.document ,filters)
            frappe.db.sql(f""" UPDATE `tabRepzo Integration Doctypes` SET last_update = '{current_date}'
                           WHERE name ='{i.name}' """)
            frappe.db.commit()


   # validate time 
@frappe.whitelist()   
def sync_now(*ars ,**kwargs) :
   make_sync()
   make_sync_updated_data()
   # if frappe.flags.in_test:
   #    make_sync()
   #    make_sync_updated_data()
   # else:
   #    frappe.enqueue( make_sync ,queue="long")
   #    frappe.enqueue( make_sync_updated_data ,queue="long")


from moyate_integration.moyate_integration.controlers import create_error_log

#from moyate_integration.moyate_integration.utils.integration import create_payment


@frappe.whitelist()
def create_payment(repzo_id , amount = False):
      
      """
      repzo_id = string  sales invoice .repzo id
      
      amount  = float if amout paid_amount will set else paid_amount will = invoice total 
      """
      repzo_setting = frappe.get_single("Repzo Integration")
      document_name = frappe.get_value("Sales Invoice" ,{"repzo_id" :repzo_id} ,"name")
      if not document_name:
         create_error_log(create_payment , "Sales Invoice" , f"their are no Repzo ID like {repzo_id} found" )
         return False
      try:
         doc = frappe.get_doc("Sales Invoice", document_name)
      except Exception as e :
         create_error_log(create_payment , "Sales Invoice" , e )
         return False

      # sales_team = doc.sales_team
      sales_team = frappe.get_all(
         "Sales Team",
         filters={"parent": doc.name},
         fields=["sales_person"]
      )      
      sales_person = sales_team[0]['sales_person']

      doc_mode_of_payment = frappe.get_doc("Mode of Payment" , frappe.db.get_value("Sales Person" , sales_person , 'mode_of_payment'))
      accounts = frappe.get_all(
         "Mode of Payment Account",
         filters={"parent": doc_mode_of_payment.name},
         fields=["company", "default_account"]
      )
      matching_data = next((d for d in accounts if d['company'] == repzo_setting.company), None)
      if not matching_data:
        return f"No Mode of Payment Account found for company '{repzo_setting.company}'"
      account = matching_data.default_account
      # doc_account = frappe.get_doc("Account" , account)
      # currency = doc_account.account_currency
      currency = frappe.db.get_value("Account" , account , 'account_currency')

      log = frappe.new_doc("Payment Entry")
      log.payment_type = "Receive"
      log.company = repzo_setting.company
      log.mode_of_payment = doc_mode_of_payment.mode_of_payment
      log.party_type = "Customer"
      log.party = doc.customer
      log.paid_to = account
      log.paid_to_account_currency = currency

      log.paid_amount = amount if amount else doc.grand_total
      log.received_amount = amount if amount else doc.grand_total

      temp = 0 
      if not amount or amount == 0:
         temp = doc.grand_total
      elif amount >= doc.grand_total:
         temp = doc.grand_total
      elif amount < doc.grand_total:
         temp = amount

      reference = {
         "reference_doctype": "Sales Invoice",
         "reference_name": document_name,
         "due_date": doc.posting_date,
         "total_amount": doc.grand_total,
         "allocated_amount":temp
      }
      log.append("references", reference)
      log.total_allocated_amount = doc.grand_total
      log.status = "Submitted"
      
      try:
         log.save(ignore_permissions = True)
         log.submit()
         frappe.db.commit()
         return log.name
      except Exception as e :
         create_error_log(create_payment , "Sales Invoice" , e )
         return False