# Copyright (c) 2021, Bantoo Accounting and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import requests
import json
from frappe.utils import today
import re
from twilio.rest import Client
import os
from twilio.twiml.voice_response import VoiceResponse
import pytracking
from pytracking.webhook import send_webhook
                
@frappe.whitelist(allow_guest=True)
def register_click(link):
    url = frappe.db.exists({
        "doctype": "Email Links",
        "original_url": link
    })
    frappe.errprint(url)    
    frappe.errprint(url[0])
    #original_url = frappe.db.sql("""SELECT original_url FROM `tabEmail Links` WHERE """)
    #Get current click count
    click_count = frappe.db.sql("""SELECT click_rate FROM `tabEmail Links` WHERE name=%s """, url[0])
    
    if click_count != None:
        next_count = click_count[0][0] + 1
        #return next_count
    
        return frappe.db.sql("""UPDATE `tabEmail Links` SET clicked = 1, click_rate = %s WHERE original_url=%s""", (next_count, link))

@frappe.whitelist(allow_guest=True)
def read_receipt(em_id):
    doc = frappe.get_doc("Email Queue", em_id)
    doc.read_by_recipient = 1
    doc.save()
"""
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
"""
@frappe.whitelist()
def call_logs():
    account_sid = frappe.db.get_single_value("Twilio Settings", "twilio_account_sid")
    auth_token = frappe.db.get_single_value("Twilio Settings", "twilio_auth_token")
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
    account_sid = frappe.db.get_single_value("Twilio Settings", "twilio_account_sid")
    auth_token = frappe.db.get_single_value("Twilio Settings", "twilio_auth_token")
    number = frappe.db.get_single_value("Twilio Settings", "twilio_number")
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        to=str(to_number),
        from_=str(number),
        url="http://demo.twilio.com/docs/voice.xml"
    )

    new = frappe.get_doc({
        "doctype": 'GIA Call Log',
        "from": str(number),
        "to": str(to_number),
        "type_of_call": 'Outgoing',
        "status": call.status,
        "duration": call.duration,
        "date": call.date_created,
    })
    new.flags.ignore_permission = True
    frappe.msgprint("Calling 📞")
    new.insert()

"""@frappe.whitelist(allow_guest=True)
def multiple_calls(x, y):
    account_sid = ""
    auth_token = ""
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        to=str(x), str(y)
        from_="+14422526335",
        url="http://demo.twilio.com/docs/voice.xml"
    )"""

@frappe.whitelist(allow_guest=True)
def answer_call(from_number):
    ignore_permissions = True

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

    account_sid = frappe.db.get_single_value("Twilio Settings", "twilio_account_sid")
    auth_token = frappe.db.get_single_value("Twilio Settings", "twilio_auth_token")
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
               
def update_link(communication, method):
    data = communication.message
    patterns = {"link": "href\=\"(.*?)\" rel"}

    for pattern in patterns.values():
        result = re.findall(pattern, data)
        for link in result:
            tracking_link = str(frappe.utils.get_url()) + "/email-tracking?link=" + link
            data = data.replace(link, tracking_link)
            communication.message = data
            row = communication.append("email_links", {
                "link_id": tracking_link,
                "original_url": link
                })
            row.insert()
            communication.save()
            
    communication.message += '<img src="https://script.google.com/macros/s/AKfycbxJUkxR-xCwSHtGh04r3hvQyzcytLRCGwFwyovD3WZvVawx8WI/exec?email_id=%s" height="1" width="1" />' % communication.name
    communication.save()

def update_link_newsletter(newsletter, method):
    data = newsletter.message
    patterns = {"link": "href\=\"(.*?)\" rel"}

    for pattern in patterns.values():
        result = re.findall(pattern, data)
        for link in result:
            tracking_link = str(frappe.utils.get_url()) + "/email-tracking?link=" + link
            data = data.replace(link, tracking_link)
            newsletter.message = data
            row = newsletter.append("email_links", {
                "link_id": tracking_link,
                "original_url": link
                })
            row.insert()
            newsletter.save()
            
    #newsletter.message += '<img src="https://script.google.com/macros/s/AKfycbxJUkxR-xCwSHtGh04r3hvQyzcytLRCGwFwyovD3WZvVawx8WI/exec?email_id=%s" height="1" width="1" />' % newsletter.name
    #newsletter.save()

def add_pixel_tracker(email_queue, method):
    email_queue.message += '<img src="https://script.google.com/macros/s/AKfycbxJUkxR-xCwSHtGh04r3hvQyzcytLRCGwFwyovD3WZvVawx8WI/exec?email_id=%s" height="1" width="1" />' % email_queue.name

    #Add email links
    if email_queue.reference_doctype == "Newsletter":
        newsletter_name = frappe.get_doc("Newsletter", email_queue.reference_name)

        #Empty table to avoid duplicates
        email_queue.email_links.clear()

        for link in newsletter_name.email_links:
            email_queue.append("email_links", {
                "link_id": link.link_id,
                "original_url": link.original_url,
                "clicked": link.clicked,
                "click_rate": link.click_rate
            })

    email_queue.save()
   
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
            "event": request.event_name,
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
                "description": str(request.full_name) + " would like a brochure for " + str(request.subject) + " Request ID: " + str(request.name) + " Email ID: " + str(request.email_address)
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

def insert_attendee(lead, method):
    if lead.workflow_state == 'Confirmed':

        new = frappe.get_doc({
            "doctype": lead.type,
            "first_name": lead.first_name,
            "last_name": lead.last_name,
            "full_name": lead.lead_name,
            "email_address": lead.email_id,
            "country": lead.country,
            "phone_number": lead.mobile_number,
            "event": lead.event,
            "company": lead.company_name,
            "job_title": lead.designation
        })
        new.flags.ignore_permission = True
        new.insert()
        if not new:
            frappe.throw("Attendee could not be added")
        frappe.db.commit()
        insert_event_attendee(lead.email_id, lead.event)

def insert_event_attendee(attendee_email, event):
    event = frappe.get_doc('Events', event)
    row = event.append("attendees", {
        "attendee_name": attendee_email,
        "status": "Invited"
    })
    row.insert()
    if not row:
        frappe.msgprint("The attendee was created but not added to the event, please add them manually")

def speaker_row(speaker, method):
    event = frappe.get_doc('Events', speaker.event)
    row = event.append("speakers", {
        "speaker_name": speaker.name,
        "location": speaker.country,
        "status": "Invited"
    })
    row.insert()

def media_row(media, method):
    event = frappe.get_doc('Events', media.event)
    row = event.append("media", {
        "media_name": media.name,
        "status": "Invited",
        "location": media.country
    })
    row.insert()

def sponsor_row(sponsor, method):
    event = frappe.get_doc('Events', sponsor.event)
    row = event.append("media", {
        "sponsor_name": sponsor.sponsor_name,
        "location": sponsor.country
    })
    row.insert()
    