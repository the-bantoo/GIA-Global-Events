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
    
    #Check what type of request the data is for.
    if data['fields[request_type][value]'] == "Brochure Request":
        form_type = "Brochure Request"
    elif data['fields[request_type][value]'] == "Attendance/Participation Request":
        form_type = "Attendance/Participation Request"
    elif data['fields[request_type][value]'] == "Webinar Recording":
        form_type = "Webinar Recording Request"
    elif data['fields[request_type][value]'] == "Discount Request":
        form_type = "Discount Request"
    
    #check the type of interest.
    if data['fields[more_about][value]'] == "Speaking":
        interest = "Speaker"
    elif data['fields[more_about][value]'] == "Attending":
        interest = "Attendee"
    elif data['fields[more_about][value]'] == "Sponsoring":
        interest = "Sponsor"
    elif data['fields[more_about][value]'] == "Exhibiting":
        interest = "Exhibitor"
    
    new_request = frappe.get_doc({
        "doctype": "Request",
        "type_of_request": form_type,
        "already_exists": request_status,
        "first_name": data['fields[f_name][value]'],
        "last_name": data['fields[l_name][value]'],
        "full_name": data['fields[f_name][value]'] + " " + data['fields[l_name][value]'],
        "job_title": data['fields[job_title][value]'],
        "company": data['fields[company][value]'],
        "email_address": data['fields[email][value]'],
        "phone_number": data['fields[phone][value]'],
        "country": data['fields[country][value]'],
        "interest_type": data['fields[more_about][value]'],
        "type": interest
        })
    new_request.insert(ignore_permissions=True)
    return context
