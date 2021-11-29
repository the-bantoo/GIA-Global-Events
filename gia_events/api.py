# Copyright (c) 2021, Bantoo Accounting and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import requests
import json
from frappe.utils import today
import re
import docx2txt
from twilio.rest import Client
import os
#from twilio.twiml.voice_response import VoiceResponse
import pytracking
from pytracking.webhook import send_webhook
                
@frappe.whitelist(allow_guest=True)
def register_click(link):
    url = frappe.db.exists({
        "doctype": "Email Links",
        "original_url": link
    })
    frappe.errprint(url)    
    frappe.log(url)
    #Get current click count
    click_count = frappe.db.sql("""SELECT click_rate FROM `tabEmail Links` WHERE name IN %s """, url)
    
    if click_count != None:
        next_count = click_count[0][0] + 1
        #return next_count
    
        return frappe.db.sql("""UPDATE `tabEmail Links` SET clicked = 1, click_rate = %s WHERE original_url=%s""", (next_count, link))
    
@frappe.whitelist(allow_guest=True)
def read_receipt(em_id):
    doc = frappe.get_doc("Communication", em_id)
    doc.read_by_recipient = 1
    doc.save()

@frappe.whitelist(allow_guest=True)
def em_tracking():
    # Assumes that the webhook url is encoded in the url.
    full_url = "https://thebantoo.com/hello"
    tracking_result = pytracking.get_open_tracking_result(
    full_url, base_click_tracking_url="https://thebantoo.com/retail")
    
    send_webhook(tracking_result)
    
    doc = frappe.get_doc({
    "doctype": "ToDo",
    "description": "My new project",
    "status": "Open"
    })
    doc.flags.ignore_permission = True
    doc.insert()
    return "Hook working"

@frappe.whitelist()
def call_logs():
    account_sid = 'ACd5dcbba47db1d63459b8bd128f775b72'
    auth_token = '18a11e7a97d973d16bbe303dd4caca06'
    client = Client(account_sid, auth_token)

    calls = client.calls.list()

    call_log = []

    for c in calls:
        log = {
            "from_": c.from_,
            "to": c.to,
            "duration": c.duration,
            "status": c.status
        }
        call_log.append(log)

    return call_log

@frappe.whitelist(allow_guest=True)
def make_call(to_number):
    account_sid = 'AC7c2a4056b4e47914b6c9931c6b8b902f'
    auth_token = '44ac96267802ca99e06449f35016f01c'
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        to=str(to_number),
        from_="+14179224443",
        url="http://demo.twilio.com/docs/voice.xml"
    )

    new = frappe.get_doc({
        "doctype": 'GIA Call Log',
        "from": "+14179224443",
        "to": str(to_number),
        "type_of_call": 'Outgoing',
        "status": call.status,
        "duration": call.duration,
        "date": call.date_created,
    })
    new.flags.ignore_permission = True
    new.insert()

"""@frappe.whitelist(allow_guest=True)
def multiple_calls(x, y):
    account_sid = "ACd5dcbba47db1d63459b8bd128f775b72"
    auth_token = "18a11e7a97d973d16bbe303dd4caca06"
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        to=str(x), str(y)
        from_="+14422526335",
        url="http://demo.twilio.com/docs/voice.xml"
    )"""

@frappe.whitelist(allow_guest=True)
def answer_call(from_number):
    ignore_permissions = True

    """account_sid = 'ACd5dcbba47db1d63459b8bd128f775b72'
    auth_token = '18a11e7a97d973d16bbe303dd4caca06'
    client = Client(account_sid, auth_token)

    calls = client.calls.list(limit=1)

    last_call = []

    for c in calls:
        last_call.append(c.from_)"""

    # Create call log
    call_log = frappe.get_doc({
        "doctype": "Call Log Twilio",
        "caller_number": from_number
    })
    call_log.insert(ignore_permissions=True)
    # return last_call[0]

@frappe.whitelist(allow_guest=True)
def check_number(phone_number):
    ignore_permissions = True

    account_sid = 'ACd5dcbba47db1d63459b8bd128f775b72'
    auth_token = '18a11e7a97d973d16bbe303dd4caca06'
    client = Client(account_sid, auth_token)

    calls = client.calls.list(limit=1)

    last_call = []

    for c in calls:
        last_call.append(c.from_)

    return last_call[0]

    number_exists = frappe.db.exists({
        'doctype': 'Contact Phone',
        'phone': phone_number
    })

    if not number_exists:
        # Contact doesn't, create new

        doc = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "Unkown",
        })

        doc.insert(ignore_permissions=True)

        row = doc.append("phone_nos", {
            "phone": phone_number
        })

        row.insert(ignore_permissions=True)
        return "Strange number"

    else:
        return "Number exists"

@frappe.whitelist()
def new_invoice(name):
    lead = frappe.get_doc('Lead', name)
    customer_list = frappe.get_list('Customer', fields=['customer_name'])
    check = {'customer_name': lead.lead_name}
    if check not in customer_list:
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": lead.lead_name,
            "type": 'Individual',
        })
        customer.insert()

    sales_invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": lead.lead_name,
        "items": [
            {
                "item_code": "Ticket",
                "qty": 1,
                "rate": lead.deal_value,
            }
        ]
    })
    sales_invoice.insert()
    frappe.msgprint(_("Sales Invoice Created"))

def attendee_row(attendee, method):
    event = frappe.get_doc('Events', attendee.event)
    row = event.append("attendees", {
        "attendee_name": attendee.email_address,
        "status": "Invited"
    })
    row.insert()

def speaker_row(speaker, method):
    event = frappe.get_doc('Events', speaker.event)
    row = event.append("speakers", {
        "speaker_name": speaker.email_address,
        "status": "Invited"
    })
    row.insert()

def media_row(media, method):
    event = frappe.get_doc('Events', media.event)
    row = event.append("media", {
        "media_name": media.email_address,
        "status": "Invited"
    })
    row.insert()
               
def update_link(communication, method):
    data = communication.content
    patterns = {"link": "href\=\"(.*?)\" rel"}

    for pattern in patterns.values():
        result = re.findall(pattern, data)
        for link in result:
            tracking_link = "https://giaevents.thebantoo.com/email-tracking?link=" + link
            data = data.replace(link, tracking_link)
            communication.content = data
            row = communication.append("email_links", {
                "link_id": tracking_link,
                "original_url": link
                })
            row.insert()
            communication.save()
            
    communication.content += '<img src="https://script.google.com/macros/s/AKfycbxGKeREVNWPvAzApaqVDVeuJVfLB1TCs_VS2XZJqV3EA-b8ieeTzMCUBmAYtQx1_ovZ/exec?email_id=%s" height="1" width="1" />' % communication.name
    communication.save()
   
def check(request, method):
    if frappe.db.exists({'doctype': 'Lead', 'email_id': request.email_address}):
        request_status = "Already Exists"
    else:
        request_status = "Pending Verification"
    frappe.db.set_value("Request", request.name, "workflow_state", request_status)
    
@frappe.whitelist()
def delete_spam():
    frappe.db.delete("Request", {
    "workflow_state": "Spam"
    })

def verify(request, method):
    if request.workflow_state == "Approved":
        #Create new Designation
        if frappe.db.exists({"doctype": "Designation", "name": request.job_title}):
            pass
        else:
            new_designation = frappe.get_doc({
                "doctype": "Designation",
                "designation_name": request.job_title
                })
            new_designation.insert(ignore_permissions=True)
            
        #Create a new Country
        if frappe.db.exists({"doctype": "Country", "name": request.country}):
            pass
        else:
            new_country = frappe.get_doc({
                "doctype": "Country",
                "country_name": request.country
                })
            new_country.insert(ignore_permissions=True)
            
        new_lead = frappe.get_doc({
            "doctype": "Lead",
            "first_name": request.first_name,
            "last_name": request.last_name,
            "lead_name": request.full_name,
            "designation": request.job_title,
            "company_name": request.company,
            "email_id": request.email_address,
            "country": request.country,
            "phone": request.phone_number,
            "industry": request.industry,
            "type": request.type,
            "request_type": request.interest_type,
            "type": request.type,
            "mobile_number": request.phone_number,
            "source": "Online Form"
            })
        new_lead.insert(ignore_permissions=True)
        
        if request.type_of_request == "Brochure Request":
            new_task = frappe.get_doc({
                "doctype": "Task",
                "Priority": "High",
                "type": "Send Brochure",
                "expected_start_date": today(),
                "subject": "Send Brochure",
                "description": str(request.full_name) + " would like a brochure, Request ID: " + str(request.name) + " Email ID: " + str(request.email_address)
                })
            new_task.insert(ignore_permissions=True)
        
    elif request.workflow_state == 'Updated':
        leads = frappe.get_all(
            'Lead', filters={'email_id': request.email_address}, fields=['name'])
        if len(leads) != 0:
            i = 0
            while i < len(leads):
                value = leads[i]['name']
                doc = frappe.get_doc('Lead', value)
                row = doc.append("lead_requests", {
                    "full_name": request.full_name,
                    "email_address": request.email_address,
                    "phone_number": request.phone_number,
                    "country": request.country,
                    "company": request.company,
                    "job_title": request.job_title
                    })
                row.insert(ignore_permissions=True)
                i += 1

"""
def insert_attendant(lead, method):
    type = ''
    if lead.workflow_state == 'Confirmed':
        if lead.type == 'Attendee':
            type = 'Attendee'
        elif lead.type == 'Speaker':
            type = 'Speaker'
        elif lead.type == 'Media':
            type = 'Media'
        else:
            type = 'Sponsor'

        new = frappe.get_doc({
            "doctype": type,
            "first_name": lead.first_name,
            "last_name": lead.last_name,
            "full_name": lead.lead_name,
            "email_address": lead.email_id,
            "country": lead.country,
            "phone_number": lead.mobile_number,
            "event": lead.event
        })
        new.flags.ignore_permission = True
        new.insert()"""
