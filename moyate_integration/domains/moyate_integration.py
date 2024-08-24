




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
              {
                "label":_("Variant ID"),
                "fieldname":"variant_id",
                "fieldtype":"Data",
                "insert_after":"item_name",
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
        'Sales Invoice':[
            {
                "label":_("Repzo ID"),
                "fieldname":"repzo_id",
                "fieldtype":"Data",
                "insert_after":"posting_date",
                 "read_only" :1
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
        "Sales Person" :[
           {
                "label":_("Repzo name"),
                "fieldname":"repzo_name",
                "fieldtype":"Data",
                "insert_after":"employee",
                # "read_only" :1
            },
        ]
 
    },
      "properties": [
        
    ],
  
}







