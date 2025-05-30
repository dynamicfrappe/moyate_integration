import frappe 
from frappe import _ 
from frappe.utils import nowdate, now_datetime

from moyate_integration.moyate_integration.utils.repzo import repzo_document_create ,repzo_document_update
from datetime import datetime, timedelta


def post_all_items_without_repzo_id():

   filters = {"repzo_id" : ["=" , ""]}

   doctyeps = ["Item" , "Customer" , "Warehouse" ,"Bin","Item Group"]
   for doc in doctyeps :
      repzo_document_create(doc ,filters , bin=1)
      last_update = now_datetime()
      frappe.db.sql(f""" UPDATE `tabRepzo Integration Doctypes` SET last_create = '{last_update}'
            WHERE name ='{doc}' """)
      frappe.db.commit()
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
   current_date = now_datetime()
   for i in repzo.items :
      if not i.last_create  :
            repzo_document_create(i.document)
            last_update = now_datetime()
            frappe.db.sql(f""" UPDATE `tabRepzo Integration Doctypes` SET last_create = '{last_update}'
            WHERE name ='{i.name}' """)
            frappe.db.sql(f""" UPDATE `tabRepzo Integration Doctypes` SET last_update = '{current_date}'
                           WHERE name ='{i.name}' """)
            frappe.db.commit()
      if i.last_create :
        
         # add hour to last update date 
         update_on = i.last_update + timedelta(minutes=int(added_minutes))
         if current_date > update_on :
            print("current_date greater than craete on ")
            filters ={"creation":[">=", update_on ] , "repzo_id" :["=" , ""]}
            repzo_document_create(i.document ,filters)
           
            frappe.db.sql(f""" UPDATE `tabRepzo Integration Doctypes` SET last_create = '{current_date}'
                        WHERE name ='{i.name}' """)
            # frappe.db.sql(f""" UPDATE `tabRepzo Integration Doctypes` SET last_update = '{current_date}'
            #             WHERE name ='{i.name}' """)
            frappe.db.commit()
         if current_date < update_on :
            print("current_date less than update on ")
   #return True
@frappe.whitelist()
def make_sync_updated_data():
   repzo = frappe.get_single("Repzo Integration")
   added_minutes = repzo.minutes
   for i in repzo.items :
      if i.last_update :
         current_date = now_datetime()
         update_on = i.last_update + timedelta(minutes=int(added_minutes))
         if current_date > update_on :
            filters ={"modified":[">=", update_on ] , "repzo_id" :[ "!=" , ""]}
            repzo_document_update(i.document ,filters)
            frappe.db.sql(f""" UPDATE `tabRepzo Integration Doctypes` SET last_update = '{current_date}'
                           WHERE name ='{i.name}' """)
            frappe.db.commit()


   # validate time 
@frappe.whitelist()   
def sync_now(*ars ,**kwargs) :
   post_all_items_without_repzo_id()
   make_sync()
   #make_sync_updated_data()
   # if frappe.flags.in_test:
   #    make_sync()
   #    make_sync_updated_data()
   # else:
   #    frappe.enqueue( make_sync ,queue="long")
   #    frappe.enqueue( make_sync_updated_data ,queue="long")





