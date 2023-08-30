import requests
from datetime import datetime as dt
import os

GENDER = "female"
WEIGHT_KG = 67.9
HEIGHT_CM = 167.8
AGE = 26

SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
NUTRITIONIX_ID = os.environ.get("NUTRITIONIX_ID")
NUTRITIONIX_API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

user_input = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": NUTRITIONIX_ID,
    "x-app-key": NUTRITIONIX_API_KEY
}
bearer_headers = {
        "Authorization": f"Bearer {SHEETY_TOKEN}"
    }

parameters = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(NUTRITIONIX_ENDPOINT, headers=headers, json=parameters)
response.raise_for_status()
data = response.json()
print(data)

today_date = dt.today().strftime("%Y/%m/%d")
now_time = dt.now().strftime("%X")

# Define the data you want to send in the body
for exercise in data["exercises"]:
    data_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["user_input"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    data_response = requests.post(SHEETY_ENDPOINT, headers=bearer_headers, json=data_inputs)
    data_response.raise_for_status()
    print(data_response.json())
