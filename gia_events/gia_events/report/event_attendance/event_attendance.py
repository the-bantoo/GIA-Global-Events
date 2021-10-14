# Copyright (c) 2013, Bantoo Accounting Innovations and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	return get_columns(), get_data(filters)

def get_data(filters):
    data = frappe.db.sql("""SELECT parent, COUNT(attendee_name), COUNT(CASE payment_status WHEN 'Paid' THEN 1 ELSE NULL END), COUNT(CASE payment_status WHEN 'Free' THEN 1 ELSE NULL END), location FROM `tabAttendee Table` GROUP BY location;""")
    return data

def get_columns():
    return [
        "Event: Data",
		"Number Of Attendees: Data",
		"Paid Attendance: Data",
		"Free Attendance: Data",
		"Location: Data"
	]
