import frappe 
import requests 
import json
from  datetime import datetime
from moyate_integration.moyate_integration.controlers import (get_repzo_setting, frappe_repzo_id ,frappe_repzo_variant,
                                           frappe_repzo_id ,
                                           create_success_log,
                                           create_error_log)
def create_adjustment(warehouse , qty , item_code , name):
   """
   doc is dict with keys 
   warehouse -- string warehouse name
   actual_qty -- float negative or positive 
   item_code -- string Item Code
   name -- string source document name
   """
   payload = {
               "to": 
                  f"{frappe_repzo_id('Warehouse' , warehouse )}" ,
               "variants":
                  [ 
                     {
                     "variant":f"{frappe_repzo_variant('Item' , item_code)}" ,
                     "qty": qty 
                     }
                  ],
               "time": f"{datetime.now().timestamp()}",
               "sync_id": f"{name}"
            }
   repzo = get_repzo_setting()
   url = f"{repzo.url}adjust-inventory" 
   headers= {"api-key" : repzo.api_key , 
             "Content-Type" :"application/json" }
   json_payload = json.dumps(payload)
   request = requests.post(url , headers=headers ,
                              data=json_payload)
   if request.status_code in [200 , 201 ]:
      create_success_log("Stock adjustment"  ,"Bin" ,
                         f"{name} Created success ")
   else :
      create_error_log("Stock Adjustment" ,"Bin" ,
                        request.text)