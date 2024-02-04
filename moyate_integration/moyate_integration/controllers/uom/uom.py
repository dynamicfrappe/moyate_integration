

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



def get_all_uom():
	url = "https://sv.api.repzo.me/measureunits?parent=BASE_UNIT_ID&disabled=false"
	response = requests.request("GET", url, headers=headers, data=payload)
	if response.status_code == 200:
		response = response.json()
		prepare_enque_method(response)
	else:
		frappe.response["http_status_code"] = response.status_code 
		frappe.response["message"] = response.text
		

def get_one_uom():
	try:
		data = json.loads(frappe.request.data)
		url = f"https://sv.api.repzo.me/measureunits/{data.get('UNIT_ID')}"
		response = requests.request("GET", url, headers=headers, data=payload)
		response = response.json()
		_create_uom(response.data)
	except Exception as e:
			frappe.local.response['message'] = f"Error Accourd  {e}"
			frappe.local.response['http_status_code'] = 400


def post_uom():
	try:
		url = "https://sv.api.repzo.me/measureunits"
		data = frappe.db.get_list('UOM',
		fields=['uom_name'],
		)
		payload = json.dumps(data)
		response = requests.request("POST", url, headers=headers, data=payload)
	except Exception as e:
			frappe.local.response['message'] = f"Error Accourd  {e}"
			frappe.local.response['http_status_code'] = 400

def update_uom():
	try:
		data = json.loads(frappe.request.data)
		payload = json.dumps({
			"parent": data.get('parent') or '',
			"name": data.get('uom_name'),
			"factor":  data.get('factor') or 1 ,
			})
		headers = {
			'Content-Type': 'application/json',
			'api-key': 'YOUR_API_KEY'
			}
		url = f"https://sv.api.repzo.me/measureunits/{data.get('uom_name')}"
		response = requests.request("PUT", url, headers=headers, data=payload)
	except Exception as e:
		frappe.local.response['message'] = f"Error Accourd  {e}"
		frappe.local.response['http_status_code'] = 400

def delete_uom():
	try:
		data = json.loads(frappe.request.data)
		url  = f"https://sv.api.repzo.me/measureunits/{data.get('remote_id')}"
		response = requests.request("DELETE", url, headers=headers, data=payload)
	except Exception as e:
		frappe.local.response['message'] = f"Error Accourd  {e}"
		frappe.local.response['http_status_code'] = 400


def prepare_enque_method(response):
	kwargs={
		"data":response.get('data'),
	}
	frappe.enqueue( 
	method=create_uom_if_not_exist,
	job_name="get_all_item",
	queue="default", 
	timeout=500, 
	is_async=True, # if this is True, method is run in worker
	now=False, # if this is True, method is run directly (not in a worker) 
	at_front=False, # put the job at the front of the queue
	**kwargs,
)
	
def create_uom_if_not_exist(**kwargs):
	for obj in kwargs.get("data"):
		_create_uom(obj)

def _create_uom(obj):
	if not frappe.db.exists("UOM",{'remote_id':obj.get('name')}):
		new_uom = frappe.new_doc("UOM")
		new_uom.remote_id = obj.get("name")
		new_uom.uom_name = obj.get("name")
		new_uom.insert(ignore_permissions=1)