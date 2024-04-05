import frappe 

from moyate_integration.controllers.repzo_stock_adjustment import create_adjustment


def submit_purchase_invoice(doc ,*args , **kwargs ) :
    if doc.update_stock ==1 :
        for item in doc.items :
         create_adjustment(doc.set_warehouse ,
                           float( item.stock_qty or 1),
                           item.item_code  ,
                           doc.name)
         
def submit_purchase_receipt(doc,*args , **kwargs) :
      for item in doc.items :
         create_adjustment(doc.set_warehouse ,
                           float( item.received_qty or 1) * float(item.conversion_factor),
                           item.item_code  ,
                           doc.name)
         
