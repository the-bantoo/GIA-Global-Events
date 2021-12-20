import frappe
from frappe import _
from frappe.utils import today

def get_context(context):
    context.name = "Administrator"
    data = frappe.form_dict

    if frappe.db.exists({'doctype': 'Lead', 'email_id': data["paymentEmail"]}):
        request_status = True
    else:
        request_status = False
    
    paid_request = frappe.get_doc({
        "doctype": "Request",
        "request_type": "Paid Request",
        "event_name": data["eventTitle"],
        "already_exists": request_status,
        "first_name": data["paymentFirstName"],
        "last_name": data["paymentLastName"],
        "full_name": data["paymentFirstName"] + " " + data["paymentLastName"],
        "email_address": data["paymentEmail"],
        "interest_type": "Attending",
        "type": "Attendee",
        "payment_status": "Paid"
        })
    paid_request.insert(ignore_permissions=True)
    return context


i = 0
while i < ticketnum:
    "first_name": data["paymentFirstName"] + i
    
i++