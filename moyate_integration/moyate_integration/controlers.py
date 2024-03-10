import frappe 
import json
import requests 
from datetime import datetime

from datetime import datetime

def execute_payload(payload ,filters = None , update =False):
   """
   param : payload --> Str -- > any Repzo Document Payload name 
           filters  -- > object EXM :->  {"creation":[">=", date time value  ]}
           update  true or false  if true will add repzo id to request  

   function objects {
   "string with variable like '{doc.name}'
   " list with many dict [{} , {'doc.name '}] 
   supported function ** 1 - frappe_repzo_id  return repzo id for any object
                         2 - frappe_item_price return price * 1000 as repzo documents 
   }
   """
   data = frappe.get_doc("Repzo Document Payload" , payload)
   if data.document == "Bin" :
      if filters :
         filters["actual_qty"]  = [">", 0 ]
   all = frappe.get_all(f"{data.document}" ,filters = filters ,fields=['*'])
   request_data = []
   obj = data.webhook_json
   json_data = json.loads(obj)
   for doc in all :
      document = {}
      for key,value in json_data.items() :
         if isinstance(value,str) :
            if len (str(value)) and str(value)[0] =='{' :
               doc_value = eval(value)
               #print(doc_value)
               document[key]  =  str(doc_value)[2:-2]
               #request_data.append(document)
            else :            
             document[key]  =  value
         elif isinstance(value,list) :
               updated_value = []
               for i in value :
                  obj = {}
                  for k , val in i .items():
                     if len (str(val)) and str(val)[0] =='{' :
                        obj_key  =  eval(val)
                       
                        li = list(obj_key)
                        obj[k]  = li[0]
                        #obj[k]  =  str(obj_key )[2:-2]
                     else :
                        obj[k] = val
                  updated_value.append(obj)
               document[key] = updated_value
         else :            
            document[key]  =  value
      document["erp_name"] = doc.name
      if update :
         document["repzo_id"] = doc.repzo_id
      request_data.append(document)

  
   return request_data

def get_repzo_setting():
   repzo = frappe.get_single("Repzo Integration")
   return repzo


def frappe_repzo_id(doctype ,name) :
   return  str(frappe.get_value(f"{doctype}" ,name ,"repzo_id"))


def frappe_repzo_variant(doctype ,name) :
   repzo_id = frappe_repzo_id(doctype ,name)
   variant_id = get_item_variant_id(repzo_id)
   return variant_id


def create_error_log(method , doctype , error):
   """
   Create Repzo log with status Failed 
   params : 
   method string repzo end point 
   doctype string frappe doctype name 
   error string error 
   
   """
   log = frappe.new_doc("Repzo Logs")
   log.status = "Failed"
   log.method = method
   log.document = doctype
   log.error = error
   log.save(ignore_permissions = True)
   frappe.db.commit()




def create_success_log(method , doctype , message) :
   log = frappe.new_doc("Repzo Logs")
   log.status = "Success"
   log.method = method
   log.document = doctype
   log.error = message
   log.save(ignore_permissions = True)
   frappe.db.commit()
   frappe.msgprint("Repzo log created")   
   frappe.msgprint("Repzo log created")



def default_item_sales_price(item) :
   price_list  =frappe.get_single('Selling Settings').selling_price_list
   item_price = frappe.get_value('Item Price' ,{"item_code" :item , "selling" :1 , "price_list" :price_list }  ,
                                   'price_list_rate' )
   return  int(float(item_price or 1) *1000)




def frappe_item_price(price) :
   return float(price) *1000



def get_document_object_by_repzo_id(doctype , repzo_id) :
   """
   params :
    doctype : frappe doctype name 
    repzo_id : object repzo id 
   return object
   """
   document_name = frappe.get_value(doctype ,{"repzo_id" :repzo_id} ,"name")
   if document_name :
       object = frappe.get_doc(doctype , document_name)
       return object
   else :
      return False

def get_item_variant_id(item) :
   """
   item str repzo id 
   """
   
   repzo = get_repzo_setting()
   url = f"{repzo.url}product/{item}?withVariants=true"
   headers= {"api-key" : repzo.api_key , "Content-Type" :"application/json"}
   request = requests.get(url , headers=headers)
   response = request.json()
   variants = response.get("variants")
   variant_id = variants[0].get("_id")
   return variant_id
