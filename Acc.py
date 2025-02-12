import pdfplumber

from pandas.tseries.offsets import BMonthEnd
import re
import pandas as pd
from datetime import datetime, timedelta, date
import time
import sys

# Function to get dates between two dates
def date_range(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)

def missing_date_range(prev, curr):
    date1 = datetime.strptime(prev, '%d-%b-%y') + timedelta(1)
    date2 = datetime.strptime(curr, '%d-%b-%y') + timedelta(-1)
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)

# Applies regex to the string passed and returns matched groups as a list
def get_data(line):
    rows = r"(\d+\d+) (\d+\d+) (\d+\d+) (\d+\d+) (\d+\d+) (\d+.\d+) (\de.\d+)"
    match = re.search(rows, line)

    if match is None:
        rows = r"(\d+\d+) (\d+\d+) (\d+\d+) (\d+\d+) (\de.\d+) (\de.\d+) (\d+.\d+)"
        match = re.search(rows, line)

    if match:
        return [float(x) for x in match.groups()]
    return []

# Get the month-end date for the provided month
def get_month_end(month):
    current_month = datetime.now().strftime('%m')

    if current_month == '01':
        passed_month = datetime(date.today().year - 1, month, 1)
    else:
        passed_month = datetime(date.today().year, month, 1)

    offset = BMonthEnd()
    month_end = offset.rollforward(passed_month)
    return month_end.strftime('%d-%b-%y').upper()

def cmp_prev_n_curr_date(prev, curr):
    date1 = datetime.strptime(prev, '%d-%b-%y')
    date2 = datetime.strptime(curr, '%d-%b-%y')
    delta = date2 - date1
    return delta.days

# Execution starts here
month = int(input("1. January\n2. February\n3. March\n4. April"
                  "\n5. May \n6. June\n7. July\n8. August \n9. September"
                  "\n10. October\n11. November\n12. December"
                  "\n\n Select month from above (Enter number): \n"))

if not (1 <= month <= 12):
    raise Exception("Input is expected between 1 and 12 where number corresponds to a month")

task_to_perform = int(input("\nSelect the task you want to perform:\n"
                            "1. Get the NOT APPROVED timesheet details.\n"
                            "2. Generate excel.\n"
                            "3. Employee Count.\n\nEnter selection (1, 2, or 3): "))

if task_to_perform not in [1, 2, 3]:
    raise Exception("Allowed values are only 1, 2, or 3")

month_word_list = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
month_word = month_word_list[month - 1]

# Open PDF
file_path = input("Enter the PDF file path: ")
pdf = pdfplumber.open(file_path)
total_pages = len(pdf.pages)
print("\nTotal pages in PDF:", total_pages)

data = pd.DataFrame()
emp_name_list = []
list_per_emp = []
date_list = []
emp_page_count = 1
prev_fetch_dict = {}
emp_count = 0
name1 = ""
period_new = ""

for i in range(total_pages):
    page = pdf.pages[i]
    content = page.extract_text()
    lines = content.split("\n")

    line_count = 0
    temp_list = []
    name_change_flag = False
    name = ""
    name_count = 0
    total_hours = [0.0] * 7
    ext_count = 0
    task_count = 0

    if task_to_perform == 3:
        for line in lines:
            if line.startswith("Employee Name"):
                name = line.split("Name")[-1].strip()
                if name1 != name:
                    emp_count += 1
                    name1 = name
                break

    if task_to_perform == 1:
        not_approved_count = 0
        for line in lines:
            if line.startswith("Employee Name"):
                name = line.split("Name")[-1].strip()
            if line.startswith("Period"):
                period = line.split("Period")[-1].strip()
                if period == period_new:
                    print("\nDuplicate data exists for employee:", name, ":", period)
                else:
                    period_new = period
            if line.startswith("Status"):
                status = line.split("Status")[-1].strip()
                if status != "Approved":
                    not_approved_count += 1
                    print("\n", name, ":", period, "", status)
                    break

    if task_to_perform == 2:
        for line in lines:
            ext_count += 1
            if line.startswith("Employee Name"):
                name = line.split("Name")[-1].strip()
                if name not in emp_name_list:
                    emp_name_list.append(name)
                    name_count += 1

            if month_end not in temp_list and emp_name_list:
                list_per_emp.insert(0, emp_name_list[name_count - 1])
                date_list.insert(0, "Employee_name")

            df = pd.DataFrame([list_per_emp], columns=date_list)
            df.set_index('Employee_name', inplace=True)
            data = pd.concat([data, df], axis=0)

            list_per_emp = []
            date_list = []
            emp_page_count = 1
            prev_fetch_dict = {
