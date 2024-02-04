


import frappe 
import requests
import json




def get_all_price_list():
	payload={}
	headers = {
	'api-key': 'YOUR_API_KEY'
	}
	url = "https://sv.api.repzo.me/pricelists?disabled=false"
	response = requests.request("GET", url, headers=headers, data=payload)
	if response.status_code == 200:
		response = response.json()
		prepare_enque_method(response)
	else:
		frappe.response["http_status_code"] = response.status_code 
		frappe.response["message"] = response.text


def post_price_list():
	try:
		url = "https://sv.api.repzo.me/pricelists"
		headers = {
		'api-key': 'YOUR_API_KEY'
		}
		data = frappe.db.get_list('Price List',
		fields=['name', 'currency'],
		)
		payload = json.dumps(data)
		response = requests.request("POST", url, headers=headers, data=payload)
		frappe.local.response['message'] = response.txt
		frappe.local.response['http_status_code'] = response.status_code
	except Exception as e:
			frappe.local.response['message'] = f"Error Accourd  {e}"
			frappe.local.response['http_status_code'] = 400

def prepare_enque_method(response):
	kwargs={
		"data":response.get('data'),
	}
	frappe.enqueue( 
	method=create_price_list_if_not_exist,
	job_name="get_all_item",
	queue="default", 
	timeout=500, 
	is_async=True, # if this is True, method is run in worker
	now=False, # if this is True, method is run directly (not in a worker) 
	at_front=False, # put the job at the front of the queue
	**kwargs,
)
	
def create_price_list_if_not_exist(**kwargs):
	for obj in kwargs.get("data"):
		_create_price_list(obj)

def _create_price_list(obj):
	if not frappe.db.exists("Price List",{'remote_id':obj.get('name')}):
		new_price_list = frappe.new_doc("Price List")
		new_price_list.remote_id = obj.get("name")
		new_price_list.uom_name = obj.get("name")
		new_price_list.insert(ignore_permissions=1)