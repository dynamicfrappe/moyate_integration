from pydoc import cli
import frappe 
import json 
from moyate_integration.moyate_integration.utils.taxts import calculate_taxes_and_totals_update
from moyate_integration.moyate_integration.controlers import ( create_error_log ,
                                                               create_success_log ,
                                                               get_repzo_setting ,
                                                               get_document_object_by_repzo_id ,
                                                               create_payment,
                                                               create_payment_for_reconcilation)
from frappe.utils import today
import requests
"""
Create invoice


Submit invoice 

"""

def get_item_defaulte_tax_template(item )  : 
   template = frappe.db.sql(""" 
   SELECT item_tax_template FROM `tabItem Tax` WHERE parent = '{item}'
   
   """,as_dict=1)
 
   return template[0].get('item_tax_template') if template else None


def get_rep_with_repzo_name(name) :
   if frappe.db.exists("Sales Person" , {"repzo_name" : name}) :
      rep = frappe.db.get_value("Sales Person" ,  {"repzo_name" : name} , "name")
      return rep
   else :
      return False 
   

def get_rep_with_repzo_id(rep_id) :
   if frappe.db.exists("Sales Person" , {"repzo_id" : rep_id}) :
      rep = frappe.db.get_value("Sales Person" ,  {"repzo_id" : rep_id} , "name")
      return rep
   else :
      return False 
   
@frappe.whitelist()
def invoice(*args , **kwargs) :

      """
      rep = frappe.db.get_value("Sales Person" ,  {"repzo_name" : "Radwan"} , "name")
      accepted params :
         _id : repzo id 
         business_day : date object
         client_id : client_repzo id 
         origin_warehouse : str warehouse repzo id 
         "items : [{}] list of objects
      
      """
   
      # try:
      try :
         data = json.loads(kwargs)
      except :
         data = kwargs
      #data = json.loads(kwargs)

      create_success_log("Sales invocie"  ,"Sales Invoice" , "Data Created success")
      repzo_id =data.get("_id")
      cur_invoice = False
      inv =frappe.db.exists("Sales Invoice" , {"repzo_id":repzo_id} ) or None
      if inv  :
         cur_invoice  = frappe.get_doc("Sales Invoice" ,
                                          frappe.get_value("Sales Invoice" , {"repzo_id" : repzo_id} ,'name') )
      if not inv :
         cur_invoice = frappe.new_doc("Sales Invoice" )
         cur_invoice.repzo_id = repzo_id 

      create_error_log("api invoice" ,"Sales Invoice" , "cur_invoice created success")
    
      repzo =get_repzo_setting()
      # invoice main info  
      cur_invoice.company = repzo.company
      cur_invoice.posting_date = today() #data.get("business_day")
      cur_invoice.due_date = today() #data.get("business_day")
      cur_invoice.customer =  frappe.get_value("Customer" , {"repzo_id" : data.get("client_id")} ,'name')
      cur_invoice.set_warehouse = frappe.get_value("Warehouse" , {"repzo_id" : data.get("origin_warehouse")} ,'name')
      #invoice  items 
      #cur_invoice.taxes_and_charges = repzo.tax_template
     
      cur_invoice.items =[]
      if data.get("items") :
         for item in data.get("items")  :
            item_object = item.get("variant")
            object = get_document_object_by_repzo_id("Item" , item_object.get("product_id"))
            uom_obj = item.get("measureunit")
            uom = get_document_object_by_repzo_id("UOM" , uom_obj.get("_id"))
            factor= float(uom_obj.get("factor") or 1)
            qty = float(item.get("qty") ) * factor
            cur_invoice.append("items"  , { 
                                             "item_code"   : object.name ,
                                             "item_name"   : object.item_name , 
                                             "description" : object.description ,
                                             "uom"    : uom.name ,
                                             "qty" : qty ,
                                             "item_tax_template" : get_item_defaulte_tax_template(object.name) ,
                                             "rate":(float(item.get("total_before_tax") or 1 )/1000)/float(qty)
                                          }
                              )
      elif data.get("return_items") :
         cur_invoice.is_return = 1
         if data.get("returned_from") :
            if frappe.db.exists("Sales Invoice" , {"repzo_id" : data.get("returned_from")} ) :
               cur_invoice.return_against = frappe.get_value("Sales Invoice" , {"repzo_id" : data.get("returned_from")} ,'name')
         for item in data.get("return_items")  :
            item_object = item.get("variant")
            object = get_document_object_by_repzo_id("Item" , item_object.get("product_id"))
            uom_obj = item.get("measureunit")
            uom = get_document_object_by_repzo_id("UOM" , uom_obj.get("_id"))
            factor= float(uom_obj.get("factor") or 1)
            qty = float(item.get("qty") ) * factor
            cur_invoice.append("items"  , { 
                                             "item_code"   : object.name ,
                                             "item_name"   : object.item_name , 
                                             "description" : object.description ,
                                             "uom"    : uom.name ,
                                             "qty" :  qty ,
                                             "item_tax_template" : get_item_defaulte_tax_template(object.name) ,
                                             "rate":(float(item.get("total_before_tax") or 1 )/1000)/float(qty)
                                          }
                              )
      # add Sales Team
      cur_invoice.sales_team =[]
      customer = get_document_object_by_repzo_id("Customer" ,data.get("client_id"))
      rep_name = data.get("creator").get("name") 
      rep = get_rep_with_repzo_name(rep_name) 
      if rep :
            cur_invoice.append("sales_team"  , {
               "sales_person" :rep ,
               "allocated_percentage" :100
               })       
      else :
         for sales_person in customer.sales_team :
            cur_invoice.append("sales_team"  , {
                  "sales_person" :sales_person.sales_person ,
                  "allocated_percentage" :sales_person.allocated_percentage
            })
      calculate_taxes_and_totals_update(cur_invoice)
      create_error_log("api invoice" ,"Sales Invoice" , "item created success")
      #try :
        
      cur_invoice.save(ignore_permissions = True)
      #calculate_taxes_and_totals_update(cur_invoice)
      cur_invoice.calculate_taxes_and_totals()
      cur_invoice.save(ignore_permissions = True)
      frappe.local.response['http_status_code'] = 200
      cur_invoice.validate()
      cur_invoice.submit()
      # except Exception as E :
      #     create_error_log("api invoice" ,"Sales Invoice Save Error " , E)
   # except Exception as E :
   #   create_error_log("api invoice" ,"Sales Invoice" , E)
   


from moyate_integration.moyate_integration.controlers import get_invoice_id
@frappe.whitelist(allow_guest=True)
def payment(*args , **kwargs) :
   repzo_id  = None   
   try :
      data = json.loads(kwargs)
   except :
      data = kwargs


   if data :
      #("paymentsData").get("payments")[0].get("fullinvoice_id")
      # create_error_log("api payment" ,"Payment Entry" , f"{data.get('LinkedTxn').get('Txn_serial_number').get('formatted')}")
      client_id = data.get("client_id")
      creator = data.get("creator").get("name")
      reference_table = data.get("paymentsData").get("payments")
      amount = float(data.get("amount") or 0) / 1000
      payment_id = data.get("_id")
      
      if data.get("LinkedTxn") :
         doc =  data.get("LinkedTxn")
         repzo_id = get_invoice_id(doc.get("Txn_serial_number").get("formatted"))
      if repzo_id :
         create_payment(repzo_id ,amount,client_id,payment_id=payment_id,creator = creator)
         # create_error_log("api payment" ,"Payment Entry" , f"{repzo_id} - amount {amount}")
      else:
         create_payment_for_reconcilation(client_id=data.get("client_id"),amount = amount, creator = creator,payment_id=payment_id,reference_table = reference_table)
         create_success_log("api payment","Payment Entry", f"amount {amount}")
         create_error_log("api payment" ,"Payment Entry" , "No repzo if found - amount {amount}")
      # frappe.local.response['http_status_code'] = 200
      # frappe.local.response['message'] = "Payment Done Correctly"
      return  
   return False


# @frappe.whitelist(allow_guest=True)
# def payment_refund(*args , **kwargs):
#    repzo_id  = None   
#    try :
#       data = json.loads(kwargs)
#    except :
#       data = kwargs
      
#    if data :
#       if data.get("LinkedTxn") :
#          doc =  data.get("LinkedTxn")
#          repzo_id = get_invoice_id(doc.get("Txn_serial_number").get("formatted"))
#       if repzo_id :
#          if frappe.db.exists("Payment Entry",{'repzo_id':repzo_id,'docstatus':1}):
#             payment_doc = frappe.get_doc("Payment Entry",{'repzo_id':repzo_id})
#          try:
#             payment_doc.cancel()
#             frappe.local.response['http_status_code'] = 200
#             frappe.local.response['message'] = "Payment Refund Done Correctly"
#          except Exception as e:
#             create_error_log("api payment" ,"Payment Entry" , e)
#             create_error_log("api payment" ,"Payment Entry" , "No repzo if found")
#             frappe.local.response['http_status_code'] = 402
#             frappe.local.response['message'] = "Problem With Refund"
            

@frappe.whitelist(allow_guest=True)
def payment_refund(*args , **kwargs):
   try :
      data = json.loads(kwargs)
   except :
      data = kwargs
      
   if data :
      customer_id = data.get("client_id")
      amount = float(data.get("amount") or 0) / 1000
      if frappe.db.exists("Customer",{"repzo_id":customer_id}):
         customer_name = frappe.db.get_value("Customer",{"repzo_id":customer_id},"name")
         payments = frappe.get_all("Payment Entry",filters={"party":customer_name,'paid_amount':amount,"docstatus":1},fields=["name"])
         if payments :
            print(f" Customer : {customer_name} - Paid Amount : {amount}")
            print(f"Payments Found {len(payments)}")
            print(payments)
            if len(payments) > 1 :
               create_error_log("api payment" ,"Payment Entry" , "Multiple Payments Found")
               frappe.local.response['http_status_code'] = 500
               frappe.local.response['message'] = "Multiple Payments Found"
               return 
            elif len(payments) == 1 :
               payment_doc = frappe.get_doc("Payment Entry",payments[0].name)
               if payment_doc.docstatus == 1 :
                  try:
                     payment_doc.cancel()
                     frappe.local.response['http_status_code'] = 200
                     frappe.local.response['message'] = "Payment Refund Done Correctly"
                     create_success_log("api payment","Payment Entry", f"Refunded Payment {payment_doc.name}")
                     return
                  except Exception as e:
                     create_error_log("api payment" ,"Payment Entry" , e)
                     frappe.local.response['http_status_code'] = 500
                     frappe.local.response['message'] = "Problem With Refund"
                     return
               else :
                  create_error_log("api payment" ,"Payment Entry" , "Payment Already Cancelled")
                  frappe.local.response['http_status_code'] = 500
                  frappe.local.response['message'] = "Payment Already Cancelled"
                  return


      
                  

@frappe.whitelist(allow_guest=True)
def customer(*args , **kwargs) :
 
   try :
      data = json.loads(kwargs)
   except :
      data = kwargs

   repzo =get_repzo_setting()
   repzo_id =data.get("_id")
   assigned_to = data.get("assigned_to")
   print(assigned_to)
   if repzo_id :
      # check if customer exist pass 
      if not frappe.db.exists("Custome" , {"repzo_id" : repzo_id}) :
         customer = frappe.new_doc("Customer")
         customer.repzo_id = repzo_id 
         customer.customer_name = data.get("name")
         customer.customer_group = repzo.customer_group
         customer.tax_id = data.get("tax_number")
         customer.receiver_id = data.get("tax_number")
         customer.territory =repzo.territory
         if assigned_to :
            print(assigned_to)
            for i in assigned_to:
               print(f"Rep ID{i}")
               customer.append("sales_team" , {
                  "sales_person" : get_rep_with_repzo_id(i) ,
                  "allocated_percentage" : 100
               })

         try :
            customer.save(ignore_permissions = True)
            create_success_log("Cautomer"  ,"Customer" , "Customer Created success")
            frappe.local.response['http_status_code'] = 200
            return True
         except Exception as E :
            create_error_log("api Customer" ,"Customer Create  error " ,E)
            frappe.local.response['http_status_code'] = 500
   else :
      create_error_log("api Customer" ,"Customer Create  error " , "no repzo ")
      frappe.local.response['http_status_code'] = 500
      return True
   
   



@frappe.whitelist(allow_guest=False)
def post_sales_person(*args , **kwargs) :
   data = kwargs
   # check for rep name exists in sales persopn and if not , create new sales person
   rep_name = data.get("name")
   repzo_id = data.get("_id")
   if not frappe.db.exists("Sales Person", {"repzo_name" : rep_name}) :
      sales_person = frappe.new_doc("Sales Person")
      sales_person.repzo_name = rep_name
      sales_person.sales_person_name = rep_name
      sales_person.enabled = 1 
      sales_person.repzo_id = repzo_id
      sales_person.save(ignore_permissions = True)
   else :
      # check if there is an update in the date or not 
      sales_person = frappe.get_doc("Sales Person", {"repzo_name" : rep_name})
      if not sales_person.repzo_id :
         sales_person.repzo_id = repzo_id
         sales_person.save(ignore_permissions = True)

      if sales_person.repzo_id != repzo_id :
         sales_person.repzo_id = repzo_id
         sales_person.save(ignore_permissions = True)

   frappe.db.commit()
   create_success_log("Sales Person"  ,"Sales Person" , "Get New Sales Persons Or Update Them Done Correctly")
   frappe.local.response['http_status_code'] = 200
   frappe.response.message = "Get New Sales Persons Or Update Them Done Correctly"

   return 
   
   
   
