
import requests
import base64
from datetime import datetime
import keys
from access_token import generate_access_token
from encode import generate_password
from utils import get_timestamp




# Create your views here.

def lipa_na_mpesa():
    access_token = generate_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = keys.short_code
   # decoded_password = generate_password(formatted_time)
    passkey = keys.lipa_na_mpesa_passkey
    formatted_time = get_timestamp()
    #decoded_password = generate_password(formatted_time)
    stk_password = base64.b64encode((shortcode + passkey + timestamp).encode('utf-8')).decode('utf-8')
    

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {"Authorization": "Bearer %s" % access_token}

    request = {
        "BusinessShortCode": keys.business_shortcode,
       # "Password": decoded_password,
        "Password": stk_password,
        "Timestamp": formatted_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": keys.phone_number,
        "PartyB": keys.business_shortcode,
        "PhoneNumber": keys.phone_number,
        "CallBackURL": 'https://a45c-197-232-90-116.ngrok-free.app/api/payments/lnm/',
        "AccountReference": "STORAGE",
        "TransactionDesc": "Pay for spaces booked",
    }

    response = requests.post(api_url, json=request, headers=headers)
    print(response.text)


lipa_na_mpesa()  