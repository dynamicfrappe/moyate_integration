import requests 
from datetime import datetime

import json
"""


"""


"""

            "name": "Small", 
            "barcode": "",
        
            "local_name": "",
            "price": 3000, 
            "sku": "AC-small",
            "position": 0

"""
#65dc889241183848b0c17342
api_key = "yPXhX5VQESaeoVRi4mi7O7h_EN8nsqLQ6LNQJifVzjA"
headers=  {"api-key" : api_key ,"Content-Type" :"application/json"}
#url = "https://sv.api.repzo.me/product"
#url = "https://sv.api.repzo.me/product/65e5eec4d3d1d2b34b1ee216?withVariants=true"
url = "https://sv.api.repzo.me/adjust-inventory"
#url ="https://sv.api.repzo.me/pricelistsitems"
#url = "adjust-inventory"
# payload = {  "name" :"Test 1027" ,
#     "local_name" : "المنتجات الخارجية لمصنع مويتي2" ,
#     "category": "65dc7e1e49285770ccf95c59",
#     "sv_measureUnit": "65dc888e4dd362e0f037d32a",
#     "variants":[
#         {   "name": "main", 
#             "barcode": "",
#             "local_name": "",
#             "price": 3000 , 
#              "sku": "AC2-small"}
#     ]



# }
# payload = {   "name": "160",
#            "local_name": "كرتون فارغ 2 لتر ",
#            "category":"65db1a060d649eb987de3c77"
 
# }

# current_datetime = datetime.now()
# timestamp = current_datetime.timestamp()
# payload = {
# 	"to" :"65db5d572bd596243f6cae8a",
# 	"variants":[
# 		{
#             "qty":30 , 
#             "variant":"65e5eec4d3d1d2b34b1ee225"
#         }
# 	],
   
#  "time" :str( timestamp) ,
#  "sync_id":"STO-2025-001"
# }

# {
# 	"to" :"WAREHOUSE_ID",
# 	"variants":[
# 		{"variant":"VARIANT_ID","qty":30 },
# 		{"variant" : "VARIANT_ID" ,"qty" : 10}
# 	],

#     "time" : "TIME_MS",
#   "sync_id": "UUID()->Unique ID"
# }
# payload = {
#     "product_id": "65dc88c49eb0f6a749c6afcf", "pricelist_id": "65e4711854df4089e6aa061d", "price": 1000
    
#     }


# payload =    {'name': '1401', 
#               'local_name': 'جالون ابيض فارغ',
#              'sku': '1401', 
#              'category': '65dc7e1cc3023caf072b3c24', 
#              'sv_measureUnit': '65dc888e4dd362e0f037d32a',
#                'variants': 
#                [{'name': 'Small',
#                               'price': 1000.0
#                            }
#     
# json_payload = json.dumps(payload)
# a = requests.post(url , headers=headers ,data=json_payload )
# print(a.text)
# print(a.status_code)
# print(a.json())
# b = a.json()
# print(b.get("_id"))
# import requests
# from test_data import invoice
# print(invoice.get("items"))
# headers=  {"Content-Type" :"application/json"}
# url = "http://0.0.0.0:8002/api/method/moyate_integration.api.invoice"
# r = requests.post(url , data=json.dumps(invoice) ,headers=headers)



temp = {
    "to": "{frappe_repzo_id('Warehouse' , doc.warehouse)}" ,
    "variants":[ 
        {"variant":  "{frappe_repzo_variant('Item' , doc.item_code)}" ,
        "qty": "{doc.actual_qty}"}
    ],
    "datetime": "{datetime.now().timestamp()}",
    "sync_id": "{doc.name}"
}
