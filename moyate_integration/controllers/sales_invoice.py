import frappe 

from moyate_integration.controllers.repzo_stock_adjustment import create_adjustment
from moyate_integration.moyate_integration.controlers import get_uid
from moyate_integration.moyate_integration.controlers import ( create_error_log )
def submit_sales_invoice(doc ,*args , **kwargs) :
    if doc.update_stock ==1 and not doc.repzo_id :
        for item in doc.items :
         create_adjustment(doc.set_warehouse ,
                           -1 *float( item.stock_qty or 1),
                           item.item_code  ,
                           get_uid(doc.name))
      
def submit_delivery_note(doc,*args , **kwargs) :
      for item in doc.items :
         create_adjustment(doc.set_warehouse ,
                           -1 *float( item.stock_qty or 1),
                           item.item_code  ,
                           get_uid(doc.name))
         


def get_item_defaulte_tax_template(item )  : 
    
    template = frappe.db.sql(f""" 
    SELECT item_tax_template FROM `tabItem Tax` WHERE parent = '{item}'
    
    """,as_dict=1)
    
    return template[0].get('item_tax_template') if template else None
def validate_sales_invoice(doc ,*args , **kwargs)  :
    for item in doc.items :
        create_error_log("item_tax_template" , get_item_defaulte_tax_template(item.item_code)  , get_item_defaulte_tax_template(item.item_code))
        item.item_tax_template = get_item_defaulte_tax_template(item.item_code)