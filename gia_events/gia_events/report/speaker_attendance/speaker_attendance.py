# Copyright (c) 2013, Bantoo Accounting Innovations and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	return get_columns(), get_data(filters)

def get_data(filters):
    data = frappe.db.sql("""SELECT parent, COUNT(speaker_name), location FROM `tabSpeaker Table` GROUP BY location;""")
    return data

def get_columns():
    return [
        "Event: Data",
		"Number Of Speakers: Data",
		"Location: Data"
	]
