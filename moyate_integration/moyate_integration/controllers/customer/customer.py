



import frappe 
import requests
import json

base_territory = frappe.db.get_single_value("Selling Settings","territory")
base_customer_group = frappe.db.get_single_value("Selling Settings","customer_group")

response = {
	"total_result": 117,
	"current_count": 10,
	"total_pages": 12,
	"current_page": 1,
	"per_page": 10,
	"first_page_url": "https://staging.sv.api.repzo.me/client?populatedKeys=%5B%22tags%22,%20%22reps%22,%20%22status,%20%22msl%22,%20%22job_category%22%20%5D&per_page=10&page=1&disabled=false",
	"last_page_url": "https://staging.sv.api.repzo.me/client?populatedKeys=%5B%22tags%22,%20%22reps%22,%20%22status,%20%22msl%22,%20%22job_category%22%20%5D&per_page=10&page=12&disabled=false",
	"next_page_url": "https://staging.sv.api.repzo.me/client?populatedKeys=%5B%22tags%22,%20%22reps%22,%20%22status,%20%22msl%22,%20%22job_category%22%20%5D&per_page=10&page=2&disabled=false",
	"prev_page_url": null,
	"path": "https://staging.sv.api.repzo.me/client",
	"data": [
		{
			"_id": "5fea2dc63aa4b3548d9c8126",
			"tags": [],
			"disabled": false,
			"formatted_address": "No location",
			"lat": 0,
			"lng": 0,
			"location_verified": false,
			"assigned_to": [],
			"profile_pic": null,
			"logo": null,
			"website": "",
			"email": "clientemail@repzoetest.com",
			"comment": "",
			"parent_client_id": null,
			"target_visit": 0,
			"geofencing_radius": null,
			"price_tag": null,
			"status": null,
			"job_category": [],
			"availability_msl": [],
			"territory": null,
			"assigned_media": [],
			"assigned_products": [],
			"company_namespace": [
				"demosv"
			],
			"teams": [],
			"name": "client name",
			"phone": "+962798355222",
			"chain": null,
			"isChain": null,
			"rep_targets": [],
			"shelf_share_targets": [],
			"jobs": [],
			"createdAt": "2020-12-28T19:11:02.740Z",
			"updatedAt": "2020-12-28T19:14:31.307Z",
			"__v": 0
		},
		{
			"_id": "5fe0b52804fb6a472076cc45",
			"tags": [
				"5fe0b52604fb6a472076cc42",
				"5fe0b52604fb6a472076cc43",
				"5fe0b52604fb6a472076cc44",
				"5fe0b52604fb6a472076cc40",
				"5fe0b52604fb6a472076cc41"
			],
			"disabled": false,
			"formatted_address": "No location",
			"lat": 31.9898748,
			"lng": 35.8515535,
			"location_verified": true,
			"assigned_to": [
				"5fc79c24b96133219dc5153b",
				"5ec509dfa361912790bef397"
			],
			"profile_pic": "18191268_1853238241594601_1506225271_n",
			"logo": "https://www.citymall.jo/sites/all/themes/citymall/images/logoen.png",
			"website": "www.citymall.jo",
			"email": "info@citymall.jo",
			"comment": "Comment 1",
			"parent_client_id": null,
			"target_visit": 0,
			"geofencing_radius": 250,
			"price_tag": null,
			"status": null,
			"job_category": [],
			"availability_msl": [
				"5fc8e1e0acc4597d8af2b217"
			],
			"territory": null,
			"assigned_media": [],
			"assigned_products": [
				"5f3243575b836958372de0f3",
				"5fce17fb30cb72155eafd6f7"
			],
			"company_namespace": [
				"demosv"
			],
			"teams": [
				"5fbb8ff8b377543d35251ca2"
			],
			"name": "City Mall",
			"client_code": "c-01",
			"phone": "00962777777777",
			"city": "Khalda",
			"state": "Amman",
			"country": "Jordan",
			"contact_name": "Mohammad Ali",
			"contact_title": "Branch Manager",
			"zip": "12356",
			"credit_limit": 500,
			"isChain": false,
			"channel": "5fe0b52604fb6a472076cc3f",
			"sv_priceList": "5fad5a419aedf7391b6ccde9",
			"paymentTerm": "5ec31fb72074755762130473",
			"rep_targets": [],
			"shelf_share_targets": [],
			"jobs": [],
			"__v": 0,
			"createdAt": "2020-12-21T14:46:00.330Z",
			"updatedAt": "2020-12-21T14:46:00.330Z"
		},
		{
			"_id": "5fe0b0472885d39aaf2f4868",
			"tags": [
				"5fe0566ac6506b81f1ba56bb"
			],
			"disabled": false,
			"formatted_address": "Formatted Address",
			"lat": 31,
			"lng": 31,
			"location_verified": false,
			"assigned_to": [
				"5e844d0c91a9c51a1a5d973d"
			],
			"profile_pic": null,
			"logo": null,
			"website": "Makkah mall",
			"email": "Makkah mall",
			"comment": "false",
			"parent_client_id": null,
			"target_visit": 0,
			"geofencing_radius": null,
			"price_tag": null,
			"status": null,
			"job_category": [],
			"availability_msl": [
				"5f155dcd878df1132c0b5b0d"
			],
			"territory": null,
			"assigned_media": [],
			"assigned_products": [],
			"company_namespace": [
				"demosv"
			],
			"teams": [
				"5fbb8ff8b377543d35251ca2"
			],
			"name": "Makkah mall",
			"sv_priceList": "5fad5a419aedf7391b6ccde9",
			"contact_name": "Makkah mall",
			"contact_title": "false",
			"phone": "false",
			"cell_phone": "Makkah mall",
			"city": "Amman Governorate, Jordan",
			"country": "Jordan",
			"zip": "code",
			"state": "KHBP",
			"channel": "5fdf659d31c0bc6db5dbe5fe",
			"client_code": "aasc",
			"paymentTerm": "5ec31fac5d5a89574611928e",
			"rep_targets": [],
			"shelf_share_targets": [],
			"jobs": [],
			"__v": 0,
			"createdAt": "2020-12-21T14:25:11.435Z",
			"updatedAt": "2020-12-21T14:25:11.435Z"
		},
		{
			"_id": "5fe0b0472885d39aaf2f4867",
			"tags": [
				"5fcf5e71db8fd470cff45328"
			],
			"disabled": false,
			"formatted_address": "Formatted Address",
			"lat": 31,
			"lng": 31,
			"location_verified": false,
			"assigned_to": [
				"5e8871d691a9c51a1a5d9767"
			],
			"profile_pic": null,
			"logo": null,
			"website": "Makkah mall",
			"email": "Makkah mall",
			"comment": "false",
			"parent_client_id": null,
			"target_visit": 0,
			"geofencing_radius": null,
			"price_tag": null,
			"status": null,
			"job_category": [],
			"availability_msl": [
				"5f154ae6878df1132c0b5b05"
			],
			"territory": null,
			"assigned_media": [],
			"assigned_products": [],
			"company_namespace": [
				"demosv"
			],
			"teams": [
				"5fbb8feeb377543d35251ca1"
			],
			"name": "Makkah mall",
			"sv_priceList": "5fad5a419aedf7391b6ccde9",
			"contact_name": "Makkah mall",
			"contact_title": "false",
			"phone": "false",
			"cell_phone": "Makkah mall",
			"city": "Amman Governorate, Jordan",
			"country": "Jordan",
			"zip": "code",
			"state": "KHBP",
			"channel": "5f573be41000882a89542f70",
			"client_code": "aassdc",
			"paymentTerm": "5ec31fbc2074755762130474",
			"rep_targets": [],
			"shelf_share_targets": [],
			"jobs": [],
			"__v": 0,
			"createdAt": "2020-12-21T14:25:11.435Z",
			"updatedAt": "2020-12-21T14:25:11.435Z"
		},
		{
			"_id": "5fe0b0472885d39aaf2f4866",
			"tags": [
				"5fe0648c057eb387bdeb3d27"
			],
			"disabled": false,
			"formatted_address": "Formatted Address",
			"lat": 31,
			"lng": 31,
			"location_verified": false,
			"assigned_to": [
				"5eb3eece2e35471b0fe246fa"
			],
			"profile_pic": null,
			"logo": null,
			"website": "Makkah mall",
			"email": "Makkah mall",
			"comment": "false",
			"parent_client_id": null,
			"target_visit": 0,
			"geofencing_radius": null,
			"price_tag": null,
			"status": null,
			"job_category": [],
			"availability_msl": [
				"5f155858878df1132c0b5b0a"
			],
			"territory": null,
			"assigned_media": [],
			"assigned_products": [],
			"company_namespace": [
				"demosv"
			],
			"teams": [
				"5fb4f18baa7523209e38e6c2"
			],
			"name": "Makkah mall",
			"sv_priceList": "5e91ef7a40472e42303b0c97",
			"contact_name": "Makkah mall",
			"contact_title": "false",
			"phone": "false",
			"cell_phone": "Makkah mall",
			"city": "Amman Governorate, Jordan",
			"country": "Jordan",
			"zip": "code",
			"state": "KHBP",
			"channel": "5f568a0c4ba5140ae47fcfb2",
			"client_code": "dx",
			"paymentTerm": "5ec31fb72074755762130473",
			"rep_targets": [],
			"shelf_share_targets": [],
			"jobs": [],
			"__v": 0,
			"createdAt": "2020-12-21T14:25:11.434Z",
			"updatedAt": "2020-12-21T14:25:11.434Z"
		},
		{
			"_id": "5fe0b0472885d39aaf2f4865",
			"tags": [
				"5fcf5e72db8fd470cff45329"
			],
			"disabled": false,
			"formatted_address": "Formatted Address",
			"lat": 35,
			"lng": 31,
			"location_verified": false,
			"assigned_to": [
				"5e85f215542d211a07ea01ca"
			],
			"profile_pic": null,
			"logo": null,
			"website": "Safeway",
			"email": "Safeway",
			"comment": "false",
			"parent_client_id": null,
			"target_visit": 0,
			"geofencing_radius": null,
			"price_tag": null,
			"status": null,
			"job_category": [],
			"availability_msl": [
				"5f1553ee6bf1f2133f1c7f35"
			],
			"territory": null,
			"assigned_media": [],
			"assigned_products": [],
			"company_namespace": [
				"demosv"
			],
			"teams": [
				"5fa940c39a07fe2e0e7d4bfb"
			],
			"name": "Safeway",
			"sv_priceList": "5f84183ea03e1a6c451c0a62",
			"contact_name": "Safeway",
			"contact_title": "false",
			"phone": "false",
			"cell_phone": "Safeway",
			"city": "Amman Governorate, Jordan",
			"country": "Jordan",
			"zip": "code",
			"state": "City Mall",
			"channel": "5f56899c4ba5140ae47fcfb1",
			"client_code": "A55d",
			"paymentTerm": "5ec31fb25d5a89574611928f",
			"rep_targets": [],
			"shelf_share_targets": [],
			"jobs": [],
			"__v": 0,
			"createdAt": "2020-12-21T14:25:11.434Z",
			"updatedAt": "2020-12-21T14:25:11.434Z"
		},
		{
			"_id": "5fe0af4e2885d39aaf2f4864",
			"tags": [
				"5fe0566ac6506b81f1ba56bb"
			],
			"disabled": false,
			"formatted_address": "Formatted Address",
			"lat": 31,
			"lng": 31,
			"location_verified": false,
			"assigned_to": [
				"5e844d0c91a9c51a1a5d973d"
			],
			"profile_pic": null,
			"logo": null,
			"website": "Makkah mall",
			"email": "Makkah mall",
			"comment": "false",
			"parent_client_id": null,
			"target_visit": 0,
			"geofencing_radius": null,
			"price_tag": null,
			"status": null,
			"job_category": [],
			"availability_msl": [
				"5f155dcd878df1132c0b5b0d"
			],
			"territory": null,
			"assigned_media": [],
			"assigned_products": [],
			"company_namespace": [
				"demosv"
			],
			"teams": [
				"5fbb8ff8b377543d35251ca2"
			],
			"name": "Makkah mall",
			"sv_priceList": "5fad5a419aedf7391b6ccde9",
			"contact_name": "Makkah mall",
			"contact_title": "false",
			"phone": "false",
			"cell_phone": "Makkah mall",
			"city": "Amman Governorate, Jordan",
			"country": "Jordan",
			"zip": "code",
			"state": "KHBP",
			"channel": "5fdf659d31c0bc6db5dbe5fe",
			"client_code": "aasc",
			"paymentTerm": "5ec31fac5d5a89574611928e",
			"rep_targets": [],
			"shelf_share_targets": [],
			"jobs": [],
			"__v": 0,
			"createdAt": "2020-12-21T14:21:02.930Z",
			"updatedAt": "2020-12-21T14:21:02.930Z"
		},
		{
			"_id": "5fe0af4e2885d39aaf2f4863",
			"tags": [
				"5fcf5e71db8fd470cff45328"
			],
			"disabled": false,
			"formatted_address": "Formatted Address",
			"lat": 31,
			"lng": 31,
			"location_verified": false,
			"assigned_to": [
				"5e8871d691a9c51a1a5d9767"
			],
			"profile_pic": null,
			"logo": null,
			"website": "Makkah mall",
			"email": "Makkah mall",
			"comment": "false",
			"parent_client_id": null,
			"target_visit": 0,
			"geofencing_radius": null,
			"price_tag": null,
			"status": null,
			"job_category": [],
			"availability_msl": [
				"5f154ae6878df1132c0b5b05"
			],
			"territory": null,
			"assigned_media": [],
			"assigned_products": [],
			"company_namespace": [
				"demosv"
			],
			"teams": [
				"5fbb8feeb377543d35251ca1"
			],
			"name": "Makkah mall",
			"sv_priceList": "5fad5a419aedf7391b6ccde9",
			"contact_name": "Makkah mall",
			"contact_title": "false",
			"phone": "false",
			"cell_phone": "Makkah mall",
			"city": "Amman Governorate, Jordan",
			"country": "Jordan",
			"zip": "code",
			"state": "KHBP",
			"channel": "5f573be41000882a89542f70",
			"client_code": "aassdc",
			"paymentTerm": "5ec31fbc2074755762130474",
			"rep_targets": [],
			"shelf_share_targets": [],
			"jobs": [],
			"__v": 0,
			"createdAt": "2020-12-21T14:21:02.930Z",
			"updatedAt": "2020-12-21T14:21:02.930Z"
		},
		{
			"_id": "5fe0af4e2885d39aaf2f4862",
			"tags": [
				"5fe0648c057eb387bdeb3d27"
			],
			"disabled": false,
			"formatted_address": "Formatted Address",
			"lat": 31,
			"lng": 31,
			"location_verified": false,
			"assigned_to": [
				"5eb3eece2e35471b0fe246fa"
			],
			"profile_pic": null,
			"logo": null,
			"website": "Makkah mall",
			"email": "Makkah mall",
			"comment": "false",
			"parent_client_id": null,
			"target_visit": 0,
			"geofencing_radius": null,
			"price_tag": null,
			"status": null,
			"job_category": [],
			"availability_msl": [
				"5f155858878df1132c0b5b0a"
			],
			"territory": null,
			"assigned_media": [],
			"assigned_products": [],
			"company_namespace": [
				"demosv"
			],
			"teams": [
				"5fb4f18baa7523209e38e6c2"
			],
			"name": "Makkah mall",
			"sv_priceList": "5e91ef7a40472e42303b0c97",
			"contact_name": "Makkah mall",
			"contact_title": "false",
			"phone": "false",
			"cell_phone": "Makkah mall",
			"city": "Amman Governorate, Jordan",
			"country": "Jordan",
			"zip": "code",
			"state": "KHBP",
			"channel": "5f568a0c4ba5140ae47fcfb2",
			"client_code": "dx",
			"paymentTerm": "5ec31fb72074755762130473",
			"rep_targets": [],
			"shelf_share_targets": [],
			"jobs": [],
			"__v": 0,
			"createdAt": "2020-12-21T14:21:02.929Z",
			"updatedAt": "2020-12-21T14:21:02.929Z"
		},
		{
			"_id": "5fe0af4e2885d39aaf2f4861",
			"tags": [
				"5fcf5e72db8fd470cff45329"
			],
			"disabled": false,
			"formatted_address": "Formatted Address",
			"lat": 35,
			"lng": 31,
			"location_verified": false,
			"assigned_to": [
				"5e85f215542d211a07ea01ca"
			],
			"profile_pic": null,
			"logo": null,
			"website": "Safeway",
			"email": "Safeway",
			"comment": "false",
			"parent_client_id": null,
			"target_visit": 0,
			"geofencing_radius": null,
			"price_tag": null,
			"status": null,
			"job_category": [],
			"availability_msl": [
				"5f1553ee6bf1f2133f1c7f35"
			],
			"territory": null,
			"assigned_media": [],
			"assigned_products": [],
			"company_namespace": [
				"demosv"
			],
			"teams": [
				"5fa940c39a07fe2e0e7d4bfb"
			],
			"name": "Safeway",
			"sv_priceList": "5f84183ea03e1a6c451c0a62",
			"contact_name": "Safeway",
			"contact_title": "false",
			"phone": "false",
			"cell_phone": "Safeway",
			"city": "Amman Governorate, Jordan",
			"country": "Jordan",
			"zip": "code",
			"state": "City Mall",
			"channel": "5f56899c4ba5140ae47fcfb1",
			"client_code": "A55d",
			"paymentTerm": "5ec31fb25d5a89574611928f",
			"rep_targets": [],
			"shelf_share_targets": [],
			"jobs": [],
			"__v": 0,
			"createdAt": "2020-12-21T14:21:02.928Z",
			"updatedAt": "2020-12-21T14:21:02.928Z"
		}
	]
}



api_key = ""
payload={}
headers = {
	'api-key': api_key
}
url = "https://sv.api.repzo.me/client"

def get_all_customer():
	"""
	get all customer
	"""
	url = url + "?disabled=false"
	response = requests.request("GET", url, headers=headers, data=payload)
	if response.status_code == 200:
		response = response.json()
		prepare_enque_method(response)
	else:
		frappe.response["http_status_code"] = response.status_code 
		frappe.response["message"] = response.text

@frappe.whitelist()
def get_one_customer():
	"""get one customer """
	try:
		data = json.loads(frappe.request.data)
	except Exception as e:
		frappe.local.response['message'] = f"Error Accourd  {e}"
		frappe.local.response['http_status_code'] = 400
		
	url = url + f"/{data.get('CLIENT_ID')}"
	response = requests.request("GET", url, headers=headers, data=payload)
	response = response.json()
	if len(response):
		_create_customer(response.get("data"))

def post_customer():
	data = frappe.db.get_list('Customer',
    fields=['customer_name', 'email','phone'],
	)
	payload = json.dumps(data)
	response = requests.request("POST",url, headers=headers, data=payload)
	if response.status_code==200:
		return response_data("Customer Created",200)
	else:
		msg = f"Error Customer Created {response.text}"
		return response_data(msg,response.status_code)

def update_customer():
	try:
		data = json.loads(frappe.request.data)
		payload = {
		"name": data.get('customer_name'),   #required
		"email": data.get('email'),
		"phone": data.get('phone'),
		# "lat" : 31.2152 , #
		# "lng": 32.12531, #
		"location_verified":False,
		"payment_type": "credit" #// or cash
	}
		url = url + f'/{data.get("remote_id")}'
		response = requests.request("PUT",url, headers=headers, data=payload)
	except Exception as e:
		msg = f"Error Accourd  {e}"
		return response_data(msg,400)
		
def delete_customer():
	try:
		data = json.loads(frappe.request.data)
		url = url + f'/{data.get("remote_id")}'
		response = requests.request("DELETE", url, headers=headers, data=payload)
	except Exception as e:
		msg = f"Error Accourd  {e}"
		return response_data(msg,400)

def prepare_enque_method(response):
	kwargs={
		"data":response.get('data'),
	}
	frappe.enqueue( 
	method=create_customer_if_not_exist,
	job_name="get_all_customer",
	queue="default", 
	timeout=500, 
	is_async=True, # if this is True, method is run in worker
	now=False, # if this is True, method is run directly (not in a worker) 
	at_front=False, # put the job at the front of the queue
	**kwargs,
)
	
def create_customer_if_not_exist(**kwargs):
	for obj in kwargs.get("data"):
		_create_customer(obj)

def _create_customer(obj):
	if not frappe.db.exists("Customer",{'remote_id':obj.get('_id')}):
		new_customer = frappe.new_doc("Customer")
		new_customer.customer_name = obj.get("name")
		new_customer.remote_id = obj.get("_id")
		new_customer.customer_group = obj.get("customer_group") or base_customer_group
		new_customer.terriotry = obj.get("terriotry")  or base_territory
		new_customer.disabled = obj.get("disabled")  or 0
		new_customer.email_id = obj.get("email")  or 0
		new_customer.mobile_no = obj.get("phone")  or 0
		new_customer.insert(ignore_permissions=1)

def response_data(msg, status):
	frappe.local.response['message'] = msg
	frappe.local.response['http_status_code'] = status
	return