import frappe 

from moyate_integration.controllers.repzo_stock_adjustment import create_adjustment

import string
import random
from moyate_integration.moyate_integration.controlers import get_uid



def async_submit_stock_entry(doc ,*args , **kwargs) :
     
      for item in doc.items :
       
        if item.s_warehouse :
            
            create_adjustment(item.s_warehouse ,
                            -1 * float( item.transfer_qty or 1) ,
                            item.item_code  ,
                           get_uid(doc.name))
        if item.t_warehouse :

            create_adjustment(item.t_warehouse ,
                            float( item.transfer_qty or 1) ,
                            item.item_code  ,
                            get_uid(doc.name))

def submit_stock_entry(doc ,*args , **kwargs) :
    async_submit_stock_entry(doc ) 
    # if frappe.flags.in_test:
    #   async_submit_stock_entry(doc ) 

    # else:
      
    #     async_submit_stock_entry(doc ) 
     
