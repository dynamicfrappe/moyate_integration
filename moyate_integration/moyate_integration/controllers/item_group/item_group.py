2
import frappe 
import requests
import json

response = {
	"name": "Category Name",
	"local_name":"اسم الفئة",
	"photo": None,
	"icon": None,
	"position": 1
}
api_key = ""
payload={}
headers = {
	'api-key': api_key
}

def get_all_item_group():
	url = "https://sv.api.repzo.me/product-category?disabled=false"
	response = requests.request("GET", url, headers=headers, data=payload)
	if response.status_code == 200:
		response = response.json()
		prepare_enque_method(response)
	else:
		frappe.response["http_status_code"] = response.status_code 
		frappe.response["message"] = response.text


def get_one_item_group():
	try:
		data = json.loads(frappe.request.data)
		url = f"https://sv.api.repzo.me/product-category/{data.get('CATEGORY_ID')}"
		response = requests.request("GET", url, headers=headers, data=payload)
		response = response.json()
		_create_item_group(response.data)
	except Exception as e:
			frappe.local.response['message'] = f"Error Accourd  {e}"
			frappe.local.response['http_status_code'] = 400
		
	
def post_one_item_group():
	try:
		url = "https://sv.api.repzo.me/product-category"
		data = json.loads(frappe.request.data)
		data = frappe.db.get_list('Item Group',
		fields=['item_group_name'],
		)
		payload = json.dumps(data)
		response = requests.request("POST", url, headers=headers, data=payload)
	except Exception as e:
			frappe.local.response['message'] = f"Error Accourd  {e}"
			frappe.local.response['http_status_code'] = 400

def update_item_group():
	try:
		data = json.loads(frappe.request.data)
		payload = {
				"name": data.get('remote_id'),
				# "position": 2
			}
		url = f"https://sv.api.repzo.me/product-category/{data.get('CATEGORY_ID')}"
		response = requests.request("POST", url, headers=headers, data=payload)
	except Exception as e:
		frappe.local.response['message'] = f"Error Accourd  {e}"
		frappe.local.response['http_status_code'] = 400

def delete_item_group():
	try:
		data = json.loads(frappe.request.data)
		url = f"https://sv.api.repzo.me/product-category/{data.get('CATEGORY_ID')}"
		response = requests.request("DELETE", url, headers=headers, data=payload)
	except Exception as e:
		frappe.local.response['message'] = f"Error Accourd  {e}"
		frappe.local.response['http_status_code'] = 400

def prepare_enque_method(response):
	kwargs={
		"data":response.get('data'),
	}
	frappe.enqueue( 
	method=create_item_group_if_not_exist,
	job_name="get_all_item",
	queue="default", 
	timeout=500, 
	is_async=True, # if this is True, method is run in worker
	now=False, # if this is True, method is run directly (not in a worker) 
	at_front=False, # put the job at the front of the queue
	**kwargs,
)
	
def create_item_group_if_not_exist(**kwargs):
	for obj in kwargs.get("data"):
		_create_item_group(obj)

def _create_item_group(obj):
	if not frappe.db.exists("Item Group",{'remote_id':obj.get('name')}):
		item_group = frappe.new_doc("Item Group")
		item_group.remote_id = obj.get("name")
		item_group.item_group_name = obj.get("local_name")
		item_group.insert(ignore_permissions=1)