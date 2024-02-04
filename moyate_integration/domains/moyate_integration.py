




from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        'Customer':[
             {
                "label":_("Remote ID"),
                "fieldname":"remote_id",
                "fieldtype":"Data",
                "insert_after":"naming_series",
                # "read_only" :1
            },
        ],
        'Item':[
             {
                "label":_("Remote ID"),
                "fieldname":"remote_id",
                "fieldtype":"Data",
                "insert_after":"naming_series",
                # "read_only" :1
            },
        ],
        'Item Group':[
             {
                "label":_("Remote ID"),
                "fieldname":"remote_id",
                "fieldtype":"Data",
                "insert_after":"item_group_name",
                # "read_only" :1
            },
        ],
        'UOM':[
             {
                "label":_("Remote ID"),
                "fieldname":"remote_id",
                "fieldtype":"Data",
                "insert_after":"uom_name",
                # "read_only" :1
            },
        ],
        'Price List':[
             {
                "label":_("Remote ID"),
                "fieldname":"remote_id",
                "fieldtype":"Data",
                "insert_after":"price_list_name",
                # "read_only" :1
            },
        ],
 
    },
      "properties": [
        
    ],
  
}







