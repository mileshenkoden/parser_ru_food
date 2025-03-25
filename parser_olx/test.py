import requests

response = requests.get('https://www.olx.ua/uk/')
print("Status Code:", response.status_code)
print("Headers:", response.headers)
print("Body (первые 500 символов):")
print(response.text)