import frappe
from frappe import _
from frappe.utils import today

def get_context(context):
    context.name = "Administrator"
    data = frappe.form_dict
    
    if frappe.db.exists({'doctype': 'Lead', 'email_id': data['fields[email][value]']}):
        request_status = True
    else:
        request_status = False
    
    #check the type of interest.
    if data['fields[more_about][value]'] == "Attending":
        interest = "Attendee"
    else:
        interest = "Exhibitor"
    
    free_request = frappe.get_doc({
        "doctype": "Free Request",
        "request_type": "Free Guest Request",
        "event_name": data['fields[event_name][value]'],
        "already_exists": request_status,
        "newsletter": data['fields[acceptance][value]'],
        "first_name": data['fields[f_name][value]'],
        "last_name": data['fields[l_name][value]'],
        "full_name": data['fields[f_name][value]'] + " " + data['fields[l_name][value]'],
        "job_title": data['fields[job_title][value]'],
        "company": data['fields[company][value]'],
        "email_address": data['fields[email][value]'],
        "phone_number": data['fields[phone][value]'],
        "country": data['fields[country][value]'],
        "interest_type": data['fields[more_about][value]'],
        "type": interest,
        "payment_status": "Free"
        })
    free_request.insert(ignore_permissions=True)
    return context
