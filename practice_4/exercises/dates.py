# Exercise #1

from datetime import datetime, timedelta

current_date = datetime.now()

five = current_date - timedelta(days=5)

print(f"Current Date: {current_date.strftime('%Y-%m-%d')}")
print(f"Date 5 days ago: {five.strftime('%Y-%m-%d')}")


# ----------------------------------------------------------------------


# Exercise 2

from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print(f"Yesterday: {yesterday.strftime('%A')}")
print(f"Today: {today.strftime('%A')}")
print(f"Tomorrow: {tomorrow.strftime('%A')}")


# ----------------------------------------------------------------------


# Exercise 3

from datetime import datetime

date = datetime.now()

print(date.strftime("%Y-%m-%d %H:%M:%S"))


# ----------------------------------------------------------------------


# Exercise 4

from datetime import datetime

date_str1 = input()
date_str2 = input()

date_format = "%Y-%m-%d %H:%M:%S"

dt1 = datetime.strptime(date_str1, date_format)
dt2 = datetime.strptime(date_str2, date_format)

time_difference = abs(dt1 - dt2)
total_seconds = time_difference.total_seconds()

print(f"Difference in seconds: {total_seconds:,.0f} seconds")