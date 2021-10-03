import time

import requests
import datetime as dt
import smtplib

MY_LAT = 13.8355807
MY_LNG = 78.7999762

NOW_HOUR = dt.datetime.now().hour
MY_EMAIL = ""
MY_PASSWORD = "*******"


parametes = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}


def is_iss_overhead():
    res = requests.get(url="http://api.open-notify.org/iss-now.json")
    res.raise_for_status()
    iss_data = res.json()
    iss_longitude = float(iss_data["iss_position"]["longitude"])
    iss_latitude = float(iss_data["iss_position"]["latitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LNG - 5 <= iss_longitude <= MY_LNG + 5:
        return True


def is_night():

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parametes)
    response.raise_for_status()
    data = response.json()
    sunrise = float(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = float(data["results"]["sunset"].split("T")[1].split(":")[0])

    if sunset <= NOW_HOUR or sunrise >= NOW_HOUR:
        return True


while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        with smtplib.SMTP(host="smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="mohangudluri@gmail.com",
                msg="Subject:ISS EMAIL\n\nLet look iss")
