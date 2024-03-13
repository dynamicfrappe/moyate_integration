import frappe 
import json 
from moyate_integration.moyate_integration.controlers import ( create_error_log ,
                                                               create_success_log ,
                                                               get_repzo_setting ,
                                                               get_document_object_by_repzo_id ,
                                                               create_payment)
"""
Create invoice


Submit invoice 

"""




@frappe.whitelist()
def invoice(*args , **kwargs) :

   """
   accepted params :
      _id : repzo id 
      business_day : date object
      client_id : client_repzo id 
      origin_warehouse : str warehouse repzo id 
      "items : [{}] list of objects
   
   """
   
   try:
      try :
         data = json.loads(kwargs)
      except :
         data = kwargs
      #data = json.loads(kwargs)
      create_error_log("api invoice" ,"Sales Invoice" , "Data Created success")
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
      cur_invoice.posting_date = data.get("business_day")
      cur_invoice.due_date = data.get("business_day")
      cur_invoice.customer =  frappe.get_value("Customer" , {"repzo_id" : data.get("client_id")} ,'name')
      cur_invoice.set_warehouse = frappe.get_value("Warehouse" , {"repzo_id" : data.get("origin_warehouse")} ,'name')
      #invoice  items 
     
      cur_invoice.items =[]
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
                                          "rate":(float(item.get("total_before_tax") or 1 )/1000)/float(qty)
                                       }
                           )
      # add Sales Team
      cur_invoice.sales_team =[]
      customer = get_document_object_by_repzo_id("Customer" ,data.get("client_id"))
      for sales_person in customer.sales_team :
         cur_invoice.append("sales_team"  , {
               "sales_person" :sales_person.sales_person ,
               "allocated_percentage" :sales_person.allocated_percentage
         })

      create_error_log("api invoice" ,"Sales Invoice" , "item created success")
      try :
         cur_invoice.save(ignore_permissions = True)
         frappe.local.response['http_status_code'] = 200
         cur_invoice.docstatus =1 
         cur_invoice.save(ignore_permissions = True)
      except Exception as E :
          create_error_log("api invoice" ,"Sales Invoice Save Error " , E)
   except Exception as E :
     create_error_log("api invoice" ,"Sales Invoice" , E)
   



@frappe.whitelist(allow_guest=True)
def payment(*args , **kwrags) :
   repzo_id  = None   
   try :
      data = json.loads(kwargs)
   except :
      data = kwargs

   if data :
      repzo_id = data.get("payments")[0].get("fullinvoice_id")
   if repzo_id :
      create_payment(repzo_id)
      frappe.local.response['http_status_code'] = 200
      return True 
   return False