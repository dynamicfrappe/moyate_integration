
import frappe 
import requests
import json

base_item_group = frappe.db.get_single_value("Stock Settings","item_group")
base_uom = frappe.db.get_single_value("Stock Settings","stock_uom")


base_url = "https://sv.api.repzo.me/product?active=true"
api_key = ""
payload={}
headers = {
	'api-key': api_key
}


def get_all_items():
	url = "https://sv.api.repzo.me/product?active=true"
	response = requests.request("GET", url, headers=headers, data=payload)
	if response.status_code == 200:
		response = response.json()
		prepare_enque_method(response)
	else:
		frappe.response["http_status_code"] = response.status_code 
		frappe.response["message"] = response.text


def post_item():
	try:
		url = "https://sv.api.repzo.me/product"
		data_no_variants = frappe.db.get_list('Item',
		filters={"has_variants":0},
		fields=['name'],
		)
		data_wiz_variants = frappe.db.get_list('Item',
		filters={"has_variants":0},
		fields=['name'],
		)
		if len(data_wiz_variants):
			for item_wiz_variant in data_wiz_variants:
				item_childs = frappe.db.get_list('Item',
				filters={"variant_of":item_wiz_variant},
				fields=['name'],
				)
				item_wiz_variant['variants'] = item_childs or []
		all_data = data_no_variants + data_wiz_variants
		payload = json.dumps(all_data)
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
	method=create_item_if_not_exist,
	job_name="get_all_item",
	queue="default", 
	timeout=500, 
	is_async=True, # if this is True, method is run in worker
	now=False, # if this is True, method is run directly (not in a worker) 
	at_front=False, # put the job at the front of the queue
	**kwargs,
)
	
def create_item_if_not_exist(**kwargs):
	for obj in kwargs.get("data"):
		_create_item(obj)

def _create_item(obj):
	if not frappe.db.exists("Item",{'remote_id':obj.get('_id')}):
		new_item = frappe.new_doc("Item")
		new_item.item_code = obj.get("name")
		new_item.remote_id = obj.get("_id")
		new_item.stock_uom = obj.get("sv_measureUnit")  or base_uom
		new_item.disabled = obj.get("disabled")  or 0
		new_item.insert(ignore_permissions=1)
