import frappe 

from moyate_integration.controllers.repzo_stock_adjustment import create_adjustment


def submit_stock_entry(doc ,*args , **kwargs) :
      for item in doc.items :
        if item.s_warehouse :
            create_adjustment(item.s_warehouse ,
                            -1 * float( item.transfer_qty or 1) ,
                            item.item_code  ,
                            doc.name)
        if item.t_warehouse :
            create_adjustment(item.t_warehouse ,
                            float( item.transfer_qty or 1) ,
                            item.item_code  ,
                            doc.name)
