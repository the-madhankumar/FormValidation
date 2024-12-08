import requests

# URL of the FastAPI backend
url = "http://127.0.0.1:8000/insert"

# Prepare data in JSON format
data = {
    "Name": "Madhan Kumar M",
    "EmployeeID": "12",
    "Email": "madhan@gmail.com",
    "PhoneNumber": "9655364633",
    "Department": "Engineering",
    "DateOfJoining": "05-12-2024",
    "Role": "Manager"
}

# Send POST request with JSON data
response = requests.post(url, json=data)

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")
