// Copyright (c) 2021, Bantoo Accounting and contributors
// For license information, please see license.txt

frappe.ui.form.on('Request', {
    interest_type(frm){
        if(frm.doc.interest_type == "Speaking"){
            frm.doc.type = "Speaker";
        }
        
        else if(frm.doc.interest_type == "Attending"){
            frm.doc.type = "Attendee";
        }
        
        else if(frm.doc.interest_type == "Sponsoring"){
            frm.doc.type = "Sponsor";
        }
        
        else if (frm.doc.interest_type == "Exhibiting"){
            frm.doc.type = "Exhibitor";
        }
        
        else{
            frm.doc.type = "Other";
        }
    },
    
    //First name field is changed
	first_name(frm) {
	    
	    //First and last name is undefined so set full name to empty string
	    if(frm.doc.first_name === undefined && frm.doc.last_name === undefined){
	        frm.set_value('full_name', "");
	    }
	    
	    //First name is set and last name is not, set full name to first name only
	    else if(frm.doc.first_name !== undefined && frm.doc.last_name === undefined){
	        frm.set_value('full_name', frm.doc.first_name);
	    }
	    
	    //Last name is set and first name is not, so det full name to last name
	    else if(frm.doc.first_name === undefined && frm.doc.last_name !== undefined){
	        frm.set_value('full_name', frm.doc.last_name);
	    }
	    
	    //Both first and last names are set so set full name to first and last name
	    else{
	        frm.set_value('full_name', frm.doc.first_name + " " + frm.doc.last_name);
	    }
	},
	
	//Last name field is changed
	last_name(frm) {
	    
	    //First and last name is undefined so set full name to empty string
	    if(frm.doc.first_name === undefined && frm.doc.last_name === undefined){
	        frm.set_value('full_name', "");
	    }
	    
	    //First name is set and last name is not, set full name to first name only
	    else if(frm.doc.first_name !== undefined && frm.doc.last_name === undefined){
	        frm.set_value('full_name', frm.doc.first_name);
	    }
	    
	    //Last name is set and first name is not, so det full name to last name
	    else if(frm.doc.first_name === undefined && frm.doc.last_name !== undefined){
	        frm.set_value('full_name', frm.doc.last_name);
	    }
	    
	    //Both first and last names are set so set full name to first and last name
	    else{
	        frm.set_value('full_name', frm.doc.first_name + " " + frm.doc.last_name);
	    }
	}
});


frappe.ui.form.on('Request',  {
    after_save: function(frm) {
        frappe.call({
            method: "gia_events.api.check_lead",
            args: {
                'name': frm.doc.name
            },
	});
    }
});
