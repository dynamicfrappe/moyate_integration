## moyate_integration

moyate_integration

#### License

MIT


Repzo Integration



On Save 
 Create custom fields for all doctypes on this document 

## Documentation

### create_adjustment(warehouse, qty, item_code, name)
 #### Args

   - warehouse -- string warehouse name
   - actual_qty -- float negative or positive 
   - item_code -- string Item Code
   - name -- string source document name

#### Description:

###### This function sends a stock adjustment request to the Repzo system by triggering the adjust-inventory webhook. It is used to synchronize inventory changes (positive or negative) from Frappe/ERPNext to Repzo.

 ## Hooks
   ### after_migrate : execute a certain function after migration
   ### after_install : execute a certain function after install the app
   
   ### Doc Events 
   #### Sales Invoice 
   
   1-   On Validaet Event -> execute moyate_integration.controllers.sales_invoice.validate_sales_invoice 
   2-   On Submit Event -> execute moyate_integration.controllers.sales_invoice.submit_sales_invoice
       Which On Cetain Condation Can Trigger The Webhook adjust-inventory using create adjustment function
   #### Delivery Note
   1-   On Submit Event -> execute moyate_integration.controllers.sales_invoice.submit_delivery_note
        Submit The Delivery Note by using create adjustment function

   #### Purchase Receipt
   1-   On Submit Event -> execute moyate_integration.controllers.purchase_invoice.submit_purchase_receipt
        Submit the Purchase Invoice and create adjustment 


   #### Purchase Invoice
   1-   On Submit Event -> execute moyate_integration.controllers.purchase_invoice.submit_purchase_invoice
        Submit the Purchase Invoice and create adjustment 
        
   #### Stock Entry
   1-   On Submit Event -> moyate_integration.controllers.stock_entry.submit_stock_entry
        Submit the Stock Entry Entry and create adjustment 

   ### Domains
   - Create Domain Repzo

   ### Schedular Events
   - Cron Job to execute moyate_integration.moyate_integration.utils.integration.sync_now every 5 minutes
        

   ### APIs
   - moyate_integration\moyate_integration\api.invoice -> Triggered By The Webhook in The Repzo to create 
     All Sales Invoices Returned or not based on the table return_items has data or not and save the id of        the document in repzo_id field  

   - moyate_integration\moyate_integration\api.payment -> Triggered By The Webhook in The Repzo to create 
    Payments Recieved From CLients and save the id of the document in repzo_id field  

   - moyate_integration\moyate_integration\api.customer -> Triggered By The Webhook in The Repzo to create 
     New Customers The Are Created as new In Repzo and save the id of the document in repzo_id field  
     
   - moyate_integration\moyate_integration\api.post_sales_person -> Triggered By The Webhook in The Repzo to      Get The Sales Persons and Create Them In ERPNext If not found and save the id of the document in             repzo_id field  
 

     



     
    
    
