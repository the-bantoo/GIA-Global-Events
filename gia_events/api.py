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
    account_sid = "ACd5dcbba47db1d63459b8bd128f775b72"
    auth_token = "18a11e7a97d973d16bbe303dd4caca06"
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        to=str(to_number),
        from_="+14422526335",
        url="http://demo.twilio.com/docs/voice.xml"
    )
    
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
    
    #Create call log
    call_log = frappe.get_doc({
        "doctype" : "Call Log Twilio",
        "caller_number": from_number
    })
    call_log.insert(ignore_permissions=True)
    #return last_call[0]
    

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
        #Contact doesn't, create new
        
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

def verify(request, method):
    if request.workflow_state == 'Approved': #Create Lead
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
        })
        new_lead.flags.ignore_permission = True
        new_lead.insert()
        
    elif request.workflow_state == 'Updated': #Update Lead
        frappe.errprint("Hi there... ")
        leads = frappe.get_all('Lead', filters={'email_id': request.email_address}, fields=['name'])
        if len(leads) != 0:
            i = 0
            while i < len(leads):
                value = leads[i]['name']
                doc = frappe.get_doc('Lead', value)
                doc.mobile_number = request.phone_number
                doc.save()
                i+=1


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


@frappe.whitelist()
def delete_spam():
    request = frappe.get_list(
        'Request', filters={'workflow_state': 'Spam'}, fields=['name'])
    if not request:
        pass
    else:
        for name in request:
            for x in name.values():
                doc = frappe.get_doc('Request', x)
                doc.delete()


def designation(request, method):
    titles = frappe.get_all('Designation', fields=['name'])
    name = {'name': request.job_title}
    if name not in titles:
        new_designation = frappe.get_doc({
            "doctype": "Designation",
            "designation_name": request.job_title
        })
        new_designation.flags.ignore_permission = True
        new_designation.insert()
    else:
        pass
    
    countries = frappe.get_all('Country', fields=['name'])
    name = {'name': request.country}
    if name not in countries:
        new_country = frappe.get_doc({
            "doctype": "Country",
            "country_name": request.country
        })
        new_country.flags.ignore_permission = True
        new_country.insert()
    else:
        pass


def create_task(request, method):
    if request.workflow_state == 'Approved':
        new_lead = frappe.get_doc({
            "doctype": "ToDo",
            "Priority": "High",
            "date": today(),
            "subject": request.full_name,
        })
        new_lead.flags.ignore_permission = True
        new_lead.insert()

"""
def data_extraction(commuincation):
    if commuincation.sender == "info@giaglobalgroup.com":
        email_content = commuincation.content
        x = json.dumps(email_content)
        data = x.replace('<br>', ' ')

        pattern = {"first_name": "First Name\:(.*?)Last",
                   "last_name": "Last Name\:(.*?)Job",
                   "job_title": "Title\:(.*?)Company",
                   "company_name": "Company\:(.*?)Email",
                   "email": "Email\:(.*?)Business",
                   "phone_number": "Phone\:(.*?)Country",
                   "country": "Country\:(.*?)I",
                   "interest_type": "about\:(.*?)Acceptance",
                   "source": "URL\:(.*?)User"}

        data_list = []
        for value in pattern.values():
            result = re.search(value, data).group(1)
            data_list.append(result)

        new_request = frappe.get_doc({
            "doctype": "Request",
            "first_name": data_list[0],
            "last_name": data_list[1],
            "job_title": data_list[2],
            "company": data_list[3],
            "email_address": data_list[4],
            "phone_number": data_list[5],
            "country": data_list[6],
            "interest_type": data_list[7],
            "source__url": data_list[8],
        })
        new_request.flags.ignore_permission = True
        new_request.insert()"""
   

@frappe.whitelist()   
def check(name):
    request = frappe.get_doc('Request', name)
    leads = frappe.get_all('Lead', filters={'email_id': request.email_address}, fields=['name'])
    if len(leads) > 0:
        request.already_exists = True
        request.workflow_state = "Already Exists"
        request.flags.ignore_permission = True
        request.save()
