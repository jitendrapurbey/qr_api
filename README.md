
# QR Code API
QR Code API is built using DRF (Django Rest Framework) to generate QR Code.  This API usage Token based authentication to authenticate the user and also use Throttle concept which is rate-limit.

You can generate 2 QR code per day without login. To create QR code without login use this:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"text":"text to be generated in QR Code"}' \
  http://127.0.0.1:8000/api/create
```
To register use this:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"user_name","password":"your_password", "email":"your_email@gmail.com"}' \
   http://127.0.0.1:8000/api/auth/register/
``` 
To login use this:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"user_name","password":"your_password"}' \
   http://127.0.0.1:8000/api/auth/register/
```


The live website is running here [QR Code API]([http://jp-qr.herokuapp.com/](https://jp-qr.herokuapp.com/)) with some changes.
