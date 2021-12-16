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
    elif data['fields[request_type][value]'] == "Event Request":
        form_type = "Event Request"
    elif data['fields[request_type][value]'] == "Webinar Recording":
        form_type = "Webinar Recording Request"
    
    #check the type of interest.
    if data['fields[more_about][value]'] == "Speaking":
        interest = "Speaker"
    elif data['fields[more_about][value]'] == "Attending":
        interest = "Attendee"
    elif data['fields[more_about][value]'] == "Sponsoring":
        interest = "Sponsor"
    elif data['fields[more_about][value]'] == "Exhibiting":
        interest = "Exhibitor"
    
    free_request = frappe.get_doc({
        "doctype": "Request",
        "type_of_request": form_type,
        "subject": data['fields[subject][value]'],
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
        "type": interest,
        "payment_status": "Free",
        "speaker_bio": data['fields[more_about][value]'],
        "topic": data['fields[more_about][value]'],
        })
    free_request.insert(ignore_permissions=True)
    return context
