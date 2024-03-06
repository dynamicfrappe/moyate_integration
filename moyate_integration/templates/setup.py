import frappe 




"""
Create Repzo custom domain 


"""


repzo = frappe.db.exists("Domain" , "Repzo")
if not repzo :
   #create domain name 
   repzo = frappe.new_doc("Domain")
   repzo.domain = "Repzo"
   print("Repzo domain Added")
   repzo.save()
   
