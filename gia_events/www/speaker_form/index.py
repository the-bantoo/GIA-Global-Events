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
    
    speaker_request = frappe.get_doc({
        "doctype": "Request",
        "request_type": "Speaker Request",
        "event_name": "World Data Summit 2022",
        "already_exists": request_status,
        "terms_conditions": True,
        "data_concent": True,
        "first_name": data['fields[f_name][value]'],
        "last_name": data['fields[l_name][value]'],
        "full_name": data['fields[f_name][value]'] + " " + data['fields[l_name][value]'],
        "job_title": data['fields[job_title][value]'],
        "company": data['fields[company][value]'],
        "email_address": data['fields[email][value]'],
        "phone_number": data['fields[mobile_phone][value]'],
        "corporate_number": data['fields[phone][value]'],
        "country": data['fields[country][value]'],
        "interest_type": "Speaking",
        "type": "Speaker",
        "speaker_bio": str(data['fields[biography][value]']),
        "topic": str(data['fields[presentation_title][value]']),
        "bullet_points": str(data['fields[bullet_points][value]']),
        "interested_session": data['fields[interested][value]'],
        "profile_image": data['fields[file][value]']
        })
    speaker_request.insert(ignore_permissions=True)
    return context
