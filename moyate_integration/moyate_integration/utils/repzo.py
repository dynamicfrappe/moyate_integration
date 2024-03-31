import frappe 
from frappe import _ 
import json
import requests 
#Repzo Integration
import string
import random
from moyate_integration.moyate_integration.controlers import *






def repzo_put_request(data , doctype , method) :
   print("Doctype" , doctype)
   repzo = get_repzo_setting()
   url = f"{repzo.url}{method}" 
   headers= {"api-key" : repzo.api_key , "Content-Type" :"application/json" }
   try :
      for payload in data :
         # get object erp name and remove from payload 
         name =payload["erp_name"] 
         del payload["erp_name"]
        
         url = url +f"/{payload.get('repzo_id')}"
         json_payload = json.dumps(payload)
         if doctype == "Bin" :
            stri = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            payload["sync_id"] = f'{stri}'
            json_payload = json.dumps(payload)
            print("Sync ID" , payload["sync_id"])
            url = f"{repzo.url}{method}"
            put = requests.post(url , headers=headers ,data=json_payload)
         else :
            put = requests.put(url , headers=headers ,data=json_payload)
         print("Payload , " ,payload)
         if put.status_code in [200 , 201 ]:
            create_success_log(method , doctype ,f"{name} updated success ")
         else :
            print("Payload , " ,payload)
            print("error")
            create_error_log(method , doctype , f"Update {doctype}  with name {name} accourd error  code {put.status_code} \n with {put.text}")
   except Exception as e :
      #create error log 
      create_error_log(method , doctype , e)



def repzo_post_request(data , doctype , method) :
   """
   params  
   data list of objects  format -->  [{} ,{}] 
   doctype string doctype name 
   method string repzo end point method
   create record on repzo and get response 
 
   """
   repzo = get_repzo_setting()
   url = f"{repzo.url}{method}" 

   # headers=  {"api-key" : api_key , "Content-Type" :"application/json" }
   headers= {"api-key" : repzo.api_key , "Content-Type" :"application/json"}
   try :
      for payload in data :
         # get object erp name and remove from payload 
         name =payload["erp_name"] 
         del payload["erp_name"]
         json_payload = json.dumps(payload)
         post = requests.post(url , headers=headers ,data=json_payload)
         
         if post.status_code in [200 , 201 ]:
            #set repzo ID 
            response = post.json()
            repzo_id = response.get("_id")
            # update with sql 
            frappe.db.sql(f"UPDATE `tab{doctype}` set repzo_id ='{repzo_id}' WHERE name = '{name}'")
            # print("done")
            create_success_log(method , doctype ,f"{name} synced with id {repzo_id}")
         else :
            print("error")
            create_error_log(method , doctype , f"Post {doctype}  with name {name} accourd error  code {post.status_code} \n with {post.text}")
   except Exception as e :
      #create error log 
      create_error_log(method , doctype , e)
      











@frappe.whitelist()   
def repzo_document_update(doctype ,filters= None) :
   """
   params doctype string doctype name 
   filters  -- > object EXM :->  {"creation":[">=", date time value  ]}
   update documents
   
   """
   #print("Doctype" , doctype)
   repzo = get_repzo_setting()
   for i in repzo.items :
      if i.document == doctype :
         #print( f"{i.document} = {doctype}")
         data_list = execute_payload(doctype ,filters ,True)
         print(data_list)
         repzo_put_request(data_list ,doctype , i.method )


@frappe.whitelist()
def repzo_document_create(doctype ,filters= None) :
   """
    params doctype string doctype name 
    filters -- > object EXM :->  {"creation":[">=", date time value  ]}
    create documents 
   """
   repzo = get_repzo_setting()
   for i in repzo.items :
      if i.document == doctype :
         #print( f"{i.document} = {doctype}")
         data_list = execute_payload(doctype ,filters )
         repzo_post_request(data_list ,doctype , i.method)


   return True
def get_document_data(doctype) :
   payload = ""
   repzo = get_repzo_setting()
   for i in repzo.items :
      if i.document == doctype :
         # post repzo data 
         try :
            # clear payload data 
            data_list = execute_payload(doctype)
            #make repzo request to create 
            repzo_post_request(data_list ,doctype , i.method)
         except Exception as e :
            create_error_log(i.method , doctype , e)











