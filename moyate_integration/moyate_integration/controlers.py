import frappe 
import json
import requests 
from datetime import datetime

import string
import random





def get_rep_with_repzo_name(name) :
   if frappe.db.exists("Sales Person" , {"repzo_name" : name}) :
      rep = frappe.db.get_value("Sales Person" ,  {"repzo_name" : name} , "name")
      return rep
   else :
      return False 
   



def get_uid(doc):
    stri = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f'{doc}-{stri}'

def execute_payload(payload ,filters = None , update =False,bin=False):
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
   all =[]
   data = frappe.get_doc("Repzo Document Payload" , payload)
   if data.document == "Bin" :
      if filters :
         filters["actual_qty"]  = [">", 0 ]
         all = frappe.get_all(f"{data.document}" ,filters = filters ,fields=['*'])
   request_data = []
   if data.document != "Bin" :

   # print(f"{data.document}  , {filters}")
      all = frappe.get_all(f"{data.document}" ,filters = filters ,fields=['*'])

   # print(all)
   
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
      # print("Docuemt" , document)
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






@frappe.whitelist(allow_guest=True)
def create_payment(repzo_id = None , amount = False,client_id = None,creator = None):
      
      """


      this fucntion will use throw create payment end point  
      repzo_id = string  sales invoice .repzo id
      
      amount  = float if amout paid_amount will set else paid_amount will = invoice total 
      """
      repzo_setting = frappe.get_single("Repzo Integration")
      document_name = frappe.get_value("Sales Invoice" ,{"repzo_id" :repzo_id} ,"name")
      if not document_name:
         create_error_log(create_payment , "Sales Invoice" , f"their are no Repzo ID like {repzo_id} found" )
         return False
      try:
         doc = frappe.get_doc("Sales Invoice", document_name)
      except Exception as e :
         create_error_log(create_payment , "Sales Invoice" , e )
         return False

      sales_person = get_rep_with_repzo_name(creator) 
      customer = frappe.get_value("Customer", {"repzo_id" : client_id},'name')
      
      doc_mode_of_payment = frappe.get_doc("Mode of Payment" , frappe.db.get_value("Sales Person" , sales_person , 'mode_of_payment'))
      accounts = frappe.get_all(
         "Mode of Payment Account",
         filters={"parent": doc_mode_of_payment.name},
         fields=["company", "default_account"]
      )
      matching_data = next((d for d in accounts if d['company'] == repzo_setting.company), None)
      if not matching_data:
        return f"No Mode of Payment Account found for company '{repzo_setting.company}'"
      account = matching_data.default_account
      # doc_account = frappe.get_doc("Account" , account)
      # currency = doc_account.account_currency
      currency = frappe.db.get_value("Account" , account , 'account_currency')

      log = frappe.new_doc("Payment Entry")
      log.payment_type = "Receive"
      log.company = repzo_setting.company
      log.mode_of_payment = doc_mode_of_payment.mode_of_payment
      log.party_type = "Customer"
      log.party = customer
      log.paid_to = account
      log.paid_to_account_currency = currency
      log.base_paid_amount =  amount if amount else doc.grand_total
      log.paid_amount = amount if amount else doc.grand_total
      log.received_amount = amount if amount else doc.grand_total

      temp = 0 



      if not amount or amount == 0:
         temp = doc.grand_total
      elif amount >= doc.outstanding_amount :
         temp = doc.outstanding_amount 
      elif amount < doc.outstanding_amount :
         temp = amount

      reference = {
         "reference_doctype": "Sales Invoice",
         "reference_name": document_name,
         "due_date": doc.posting_date,
         "total_amount": doc.grand_total,
         "outstanding_amount" : doc.outstanding_amount ,
         "allocated_amount":temp
      }
      log.append("references", reference)
      log.total_allocated_amount = doc.grand_total
      #log.status = "Submitted"
      
      try:
         log.save(ignore_permissions = True)
         #log.submit()
         #frappe.db.commit()
         log.docstatus = 1 
         log.save(ignore_permissions = True)
         frappe.db.commit()
         create_success_log("create_payment" , "Payment Entry" , f"{log.name} succefuly created")
         #return log.name
      except Exception as e :
         create_error_log("create_payment" , "Sales Invoice" , e )
         return False
      
      
# @frappe.whitelist()
# def create_payment_for_reconcilation(client_id, amount = False,creator = None, reference_table=None ):
   

#    repzo_setting = frappe.get_single("Repzo Integration")

      
#    customer = frappe.get_value("Customer" , {"repzo_id" : client_id} ,'name')
#    sales_person = get_rep_with_repzo_name(creator) 

#    doc_mode_of_payment = frappe.get_doc("Mode of Payment" , frappe.db.get_value("Sales Person" , sales_person , 'mode_of_payment'))
#    accounts = frappe.get_all(
#       "Mode of Payment Account",
#       filters={"parent": doc_mode_of_payment.name},
#       fields=["company", "default_account"]
#    )
#    matching_data = next((d for d in accounts if d['company'] == repzo_setting.company), None)
#    if not matching_data:
#       return f"No Mode of Payment Account found for company '{repzo_setting.company}'"
   
#    account = matching_data.default_account
#    currency = frappe.db.get_value("Account" , account , 'account_currency')

#    # get all outstanding invoices
#    try:   
#    # Create payment entry
#       payment_entry = frappe.new_doc("Payment Entry")
#       payment_entry.payment_type = "Receive"
#       payment_entry.company = repzo_setting.company
#       payment_entry.mode_of_payment = doc_mode_of_payment.mode_of_payment
#       payment_entry.party_type = "Customer"
#       payment_entry.party = customer
#       payment_entry.paid_to = account
#       payment_entry.paid_to_account_currency = currency

#       print(f"{reference_table}")
   
      
#       payment_entry.paid_amount = amount
#       payment_entry.base_paid_amount = amount
#       payment_entry.received_amount = amount
#       payment_entry.total_allocated_amount = amount
#       temp = amount
#       for row in reference_table: 
#          invoice_name = frappe.db.get_value("Sales Invoice", {"repzo_id": row["fullinvoice_id"]}, "name")
         
#          payment_entry.append("references", {
#             "reference_doctype": "Sales Invoice",
#             "reference_name": frappe.db.get_value("Sales Invoice", {"repzo_id": row["fullinvoice_id"]}, "name")
#          })
      
#       payment_entry.save()
#       frappe.db.commit()
#       if not payment_entry.references:
#          frappe.db.rollback()
#          frappe.local.response["message"] = "No outstanding invoices found for the customer"
#          frappe.local.response["http_status_code"] = 404
#          return
#       create_success_log("create_payement_based_on_outstanding", "Payment Entry", f"{payment_entry.name} succefuly created")
#    except Exception as e :
#       frappe.db.rollback()
#       create_error_log("create_payement_based_on_outstanding", "Sales Invoice", e )
#       return False


@frappe.whitelist()
def create_payment_for_reconcilation(client_id, amount = False, creator = None, reference_table=None):
   repzo_setting = frappe.get_single("Repzo Integration")
   customer = frappe.get_value("Customer", {"repzo_id": client_id}, 'name')
   sales_person = get_rep_with_repzo_name(creator)

   doc_mode_of_payment = frappe.get_doc("Mode of Payment", frappe.db.get_value("Sales Person", sales_person, 'mode_of_payment'))
   accounts = frappe.get_all(
      "Mode of Payment Account",
      filters={"parent": doc_mode_of_payment.name},
      fields=["company", "default_account"]
   )
   matching_data = next((d for d in accounts if d['company'] == repzo_setting.company), None)
   if not matching_data:
      return f"No Mode of Payment Account found for company '{repzo_setting.company}'"
   
   account = matching_data.default_account
   currency = frappe.db.get_value("Account", account, 'account_currency')
   
   # Get customer's receivable account
   customer_account = frappe.get_value("Company", repzo_setting.company, "default_receivable_account")

   try:
      # get_outstanding_reference_documents
      from erpnext.accounts.doctype.payment_entry.payment_entry import get_outstanding_reference_documents

      
      # Prepare arguments for the standard function
      args = {
         "party_type": "Customer",
         "party": customer,
         "party_account": customer_account,
         "company": repzo_setting.company
      }
      
      # Get outstanding documents using standard ERPNext function
      outstanding_documents = get_outstanding_reference_documents(args)
      
      if not outstanding_documents:
         frappe.local.response["message"] = "No outstanding invoices found for the customer"
         return 
      print(f"Outstanding documents from standard function: {outstanding_documents}")
      
      # Create payment entry
      payment_entry = frappe.new_doc("Payment Entry")
      payment_entry.payment_type = "Receive"
      payment_entry.company = repzo_setting.company
      payment_entry.mode_of_payment = doc_mode_of_payment.mode_of_payment
      payment_entry.party_type = "Customer"
      payment_entry.party = customer
      payment_entry.paid_to = account
      payment_entry.paid_to_account_currency = currency

      print(f"Reference table: {reference_table}")
      
      references_added = 0
      total_allocated = 0
      
      
      outstanding_map = {}
      for outstanding in outstanding_documents:
         if outstanding.get("voucher_type") == "Sales Invoice":
               # Get repzo_id for this invoice
               repzo_id = frappe.db.get_value("Sales Invoice", outstanding.voucher_no, "repzo_id")
               if repzo_id:
                  outstanding_map[repzo_id] = outstanding
      
      print(f"Outstanding map: {outstanding_map}")
      
      for i, row in enumerate(reference_table):
         print(f"Processing row {i}: {row}")
         
         repzo_id = row["fullinvoice_id"]
         print(f"Looking for repzo_id: {repzo_id}")
         
         # Check if this invoice has outstanding amount using standard function
         if repzo_id not in outstanding_map:
               print(f"Invoice with repzo_id {repzo_id} has no outstanding amount or doesn't exist")
               continue
         
         outstanding_doc = outstanding_map[repzo_id]
         print(f"Found outstanding document: {outstanding_doc}")
         
         
         requested_amount = float(row.get("amount", 0)) / 1000
         
         # Use the actual outstanding amount from the standard function
         actual_outstanding = float(outstanding_doc.get("outstanding_amount", 0))
         allocated_amount = min(requested_amount, actual_outstanding)
         print(f" ======> Requested amount: {requested_amount}, Actual outstanding: {actual_outstanding}, Allocated amount: {allocated_amount}")
         if allocated_amount <= 0:
               print(f"No valid amount to allocate for invoice {outstanding_doc.voucher_no}")
               continue
         
         reference_dict = {
               "reference_doctype": outstanding_doc.get("voucher_type"),
               "reference_name": outstanding_doc.get("voucher_no"),
               "due_date": outstanding_doc.get("due_date"),
               "total_amount": float(outstanding_doc.get("invoice_amount", 0)),
               "outstanding_amount": actual_outstanding,
               "allocated_amount": allocated_amount,
               "exchange_rate": outstanding_doc.get("exchange_rate", 1)
         }
         
         print(f"Adding reference: {reference_dict}")
         payment_entry.append("references", reference_dict)
         references_added += 1
         total_allocated += allocated_amount
         print(f"References added so far: {references_added}, Total allocated: {total_allocated}")
      
      if references_added == 0:
         # frappe.db.rollback()
         frappe.local.response["message"] = "No invoices with outstanding amounts found for payment allocation"
         frappe.local.response["http_status_code"] = 404
         return
      
      
      payment_entry.paid_amount = amount
      # payment_entry.base_paid_amount = amount
      payment_entry.received_amount = amount
      # payment_entry.total_allocated_amount = amount
      payment_entry.setup_party_account_field()
      payment_entry.set_missing_values()
      # Save and submit using standard validation
      payment_entry.save(ignore_permissions=True)
      payment_entry.submit()
      print(f"Payment entry created and submitted: {payment_entry.name}")
      
      create_success_log("create_payement_based_on_outstanding", "Payment Entry", f"{payment_entry.name} successfully created")
      frappe.local.response["message"] = "Payment entry created and submitted"
      frappe.local.response["http_status_code"] = 200
      return 
      
   except Exception as e:
      print(f"Main exception: {str(e)}")
      import traceback
      print(f"Full traceback: {traceback.format_exc()}")
      # frappe.db.rollback()
      create_error_log("create_payement_based_on_outstanding", "Sales Invoice", str(e))
      return False

# @frappe.whitelist()
# def create_payement_based_on_outstanding(amount = False,client_id = None,creator = None):
#       """


#       this fucntion will use throw create payment end point  
#       repzo_id = string  sales invoice .repzo id
      
#       amount  = float if amout paid_amount will set else paid_amount will = invoice total 
#       """
#       repzo_setting = frappe.get_single("Repzo Integration")

      
#       customer = frappe.get_value("Customer" , {"repzo_id" : client_id} ,'name')
#       sales_person = get_rep_with_repzo_name(creator) 

#       doc_mode_of_payment = frappe.get_doc("Mode of Payment" , frappe.db.get_value("Sales Person" , sales_person , 'mode_of_payment'))
#       accounts = frappe.get_all(
#          "Mode of Payment Account",
#          filters={"parent": doc_mode_of_payment.name},
#          fields=["company", "default_account"]
#       )
#       matching_data = next((d for d in accounts if d['company'] == repzo_setting.company), None)
#       if not matching_data:
#         return f"No Mode of Payment Account found for company '{repzo_setting.company}'"
     
#       account = matching_data.default_account
#       currency = frappe.db.get_value("Account" , account , 'account_currency')

#       # get all outstanding invoices
#       outstanding_invoices = frappe.get_all(
#          "Sales Invoice",
#          filters={"customer":customer,"outstanding_amount": ["!=", 0],"docstatus":1},
#          fields=["name", "outstanding_amount","grand_total","due_date"],
#          order_by="posting_date asc"
#       )
#       if not outstanding_invoices:
#          frappe.local.response["message"] = "No outstanding invoices found for the customer"
#          frappe.local.response["http_status_code"] = 404
#          return
         
            
#      # Create payment entry
#       payment_entry = frappe.new_doc("Payment Entry")
#       payment_entry.payment_type = "Receive"
#       payment_entry.company = repzo_setting.company
#       payment_entry.mode_of_payment = doc_mode_of_payment.mode_of_payment
#       payment_entry.party_type = "Customer"
#       payment_entry.party = customer
#       payment_entry.paid_to = account
#       payment_entry.paid_to_account_currency = currency

#       allocated_amount = 0
#       remaining_amount = float(amount) if amount else 0

#       for invoice in outstanding_invoices:
#          print(f"{remaining_amount}")
#          if remaining_amount <= 0:
#             frappe.local.response["message"] = "No Paid Amount Entered"
#             frappe.local.response["http_status_code"] = 400
            
#             break

#          alloc_amount =  remaining_amount
#          remaining_amount -= alloc_amount
#          allocated_amount += alloc_amount
#          print(f" allocated amount {alloc_amount}")
#          print(f"outstanding {invoice.outstanding_amount}")
#          payment_entry.append("references", {
#                 "reference_doctype": "Sales Invoice",
#                 "reference_name": invoice.name,
#                 "due_date": invoice.due_date,
#                 "total_amount": invoice.grand_total,
#                 "outstanding_amount": invoice.outstanding_amount,
#                 "allocated_amount": alloc_amount
#             })
         
#          if allocated_amount == 0:
#             frappe.local.response["message"] =  "No invoices could be allocated with the provided amount."
#             frappe.local.response["http_status_code"] = 400
#             break 

#       payment_entry.paid_amount = allocated_amount
#       payment_entry.base_paid_amount = allocated_amount
#       payment_entry.received_amount = allocated_amount
#       payment_entry.total_allocated_amount = allocated_amount

      
#       try:
#          payment_entry.save(ignore_permissions = True)
#          payment_entry.docstatus = 1
#          payment_entry.save(ignore_permissions = True)
#          frappe.db.commit()
#          create_success_log("create_payement_based_on_outstanding", "Payment Entry", f"{payment_entry.name} succefuly created")
#       except Exception as e :
#          create_error_log("create_payement_based_on_outstanding", "Sales Invoice", e )
#          return False
   
   
# from moyate_integration.moyate_integration.controlers import get_invoice_id   get_invoice_id("INV-1006-616")


def get_invoice_id(serial) :
   repzo = get_repzo_setting()
   #https://sv.api.repzo.me/fullinvoices?is_void=false&search=INV-1545-368
   url = f"{repzo.url}fullinvoices?is_void=false&search={serial}"
   headers= {"api-key" : repzo.api_key , "Content-Type" :"application/json"}
   request = requests.get(url , headers=headers)
   if request.status_code not in [200 , 201] :
      create_error_log("create_payment" , f"Sales Invoice {serial}" , f"Has error {request.text} " )
   response = request.json()
   data = response.get("data")
   id = data[0].get("_id")
   return id
   