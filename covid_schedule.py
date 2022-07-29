"""Queries for available vaccination appointments within 100 miles of my zip

Then shoots me a text if some become available."""

import json
import requests
import smtplib
import time

from pyzipcode import ZipCodeDatabase

from_email = ""
to_email = ""
password = ""

zdb = ZipCodeDatabase()
in_radius = [z.zip for z in zdb.get_zipcodes_around_radius('68506', 30)]
zip_set = set(in_radius)

# Email/Text stuff
port = 465

session = smtplib.SMTP("smtp.gmail.com", 587)
session.starttls()
session.login("", password)

while True:
  r = requests.get("https://www.vaccinespotter.org/api/v0/states/NE.json")
  data = r.json()
  for feature in data["features"]:
    if not feature["properties"]["appointments_available"]:
      continue

    if feature["properties"]["postal_code"] not in zip_set:
      continue

    city = feature["properties"]["city"]
    url = feature["properties"]["url"]

    print(city)
    print(url)
    print()

    session.sendmail(from_email, to_email, f"Appointment available in {city}.")

  time.sleep(5)
