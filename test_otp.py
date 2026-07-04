import requests

try:
    response = requests.post(
        "http://127.0.0.1:8000/users/otp/request/",
        json={"phone_number": "09123456789"}
    )
    print("STATUS:", response.status_code)
    with open("error_out.html", "w", encoding="utf-8") as f:
        f.write(response.text)
except Exception as e:
    print("ERROR:", e)
