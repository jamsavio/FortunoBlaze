import requests
import jwt

url = 'http://127.0.0.1:5000/login'
email = 'xxx@gmail.com'

response = requests.get(url, params={'email': email})

if response.status_code == 200:
    token = response.json()['token']
    decoded_token = jwt.decode(token, '7e372c35c140e6d80b6f85dce25b56e64b8a858b0151e151d464c107865a7438e0b7a268b065d2beff57f8c8ebd7f24528f3e3c3c38337f74e6d01d6a1a1827c', algorithms=['HS256'])
    print(decoded_token['email']+" "+str(decoded_token['exp']))
else:
    print(response.json()['message'])