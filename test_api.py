
import requests

url = "http://127.0.0.1:5000/predict"

passenger = {
    "Gender": "Female",
    "Customer Type": "Loyal Customer",
    "Age": 35,
    "Type of Travel": "Business travel",
    "Class": "Business",
    "Flight Distance": 1200,
    "Inflight wifi service": 4,
    "Departure/Arrival time convenient": 4,
    "Ease of Online booking": 4,
    "Gate location": 3,
    "Food and drink": 4,
    "Online boarding": 5,
    "Seat comfort": 4,
    "Inflight entertainment": 4,
    "On-board service": 4,
    "Leg room service": 4,
    "Baggage handling": 4,
    "Checkin service": 4,
    "Inflight service": 4,
    "Cleanliness": 4,
    "Departure Delay in Minutes": 0,
    "Arrival Delay in Minutes": 0
}

try:
    response = requests.post(url, json=passenger, timeout=10)

    print("Status code:", response.status_code)
    print("Response:")
    print(response.text)

except requests.exceptions.RequestException as error:
    print("Could not connect to the API:", error)
