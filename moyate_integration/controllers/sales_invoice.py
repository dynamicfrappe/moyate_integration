import frappe 

from moyate_integration.controllers.repzo_stock_adjustment import create_adjustment


def submit_sales_invoice(doc ,*args , **kwargs) :
    if doc.update_stock ==1 and not doc.repzo_id :
        for item in doc.items :
         create_adjustment(doc.set_warehouse ,
                           -1 *float( item.stock_qty or 1),
                           item.item_code  ,
                           doc.name)
      
def submit_delivery_note(doc,*args , **kwargs) :
      for item in doc.items :
         create_adjustment(doc.set_warehouse ,
                           -1 *float( item.stock_qty or 1),
                           item.item_code  ,
                           doc.name)