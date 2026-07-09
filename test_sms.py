import requests

url = "https://api.iranpayamak.com/ws/v1/sms/pattern"
headers = {
    "Api-Key": "ekkE2QERFUex04JMJjqoIRvHtEzriHHF0jJv1dfOWpDx2D8RxO",
    "Content-Type": "application/json"
}
body = {
    "code": "pJHnuEmOlu",
    "attributes": {
        "code": "1234",
        "verification-code": "1234"
    },
    "recipient": "09123456789",
    "line_number": "90008361",
    "number_format": "english"
}
try:
    response = requests.post(url, headers=headers, json=body)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
