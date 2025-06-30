// Copyright (c) 2024, Hagar Mossad and contributors
// For license information, please see license.txt
frappe.ui.form.on("Monthly Account Statement", {
	refresh:function(frm) {
       console.log("hhhhh");
	},
    party:function(frm){
        if (frm.doc.party){
            frappe.call({
                method: "moyate_integration.moyate_integration.doctype.monthly_account_statement.monthly_account_statement.get_balance",
                args:{
                    "party": frm.doc.party,
                    "party_type": frm.doc.party_type
                }, 
                callback: function (r) {
                    if (r) {
                        console.log(r.message);
                        frm.set_value("balance",r.message)
                        frm.refresh_field("balance")
                    }
                }
            })
        }
    },
    gl_btn: function(frm) {
        let today = new Date();
        let from_date = new Date();
        from_date.setDate(today.getDate() - 30);

        let formatted_today = frappe.datetime.get_today();
        let formatted_from_date = moment(from_date).format('YYYY-MM-DD');

        console.log(frm.doc.party);

        if (frm.doc.party_type == "Customer"){
            frappe.set_route('query-report', 'Customer Ledger Summary', {
                "party": frm.doc.party,
                "to_date": formatted_today,
                "from_date": formatted_from_date,
            });
        }else if (frm.doc.party_type == "Supplier"){
            frappe.set_route('query-report', 'Supplier Ledger Summary', {
                "party": frm.doc.party,
                "to_date": formatted_today,
                "from_date": formatted_from_date,
            });
        }
        

        
    },

});