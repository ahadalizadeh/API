from datetime import datetime
import base64
import hmac
import json
import hashlib
import requests
########################## A function for creating signature
def create_signature(secret_key, full_path, request_method, request_data=None):
    timestamp = int(datetime.utcnow().now().timestamp() * 1000)
    msg = f'{request_method.upper()}\n{full_path}\n{timestamp}'   
    if request_data:
        base64encode = base64.b64encode(json.dumps(request_data).encode()).decode()
        msg += f'\n{base64encode}'
    signed_key = hmac.new(
        bytes(secret_key, "utf-8"),
        msg=bytes(msg, "utf-8"),
        digestmod=hashlib.sha256).hexdigest()
    return signed_key, timestamp

secret_key =  "**********************"      ################# Add secret key
API        =  "**********************"      ################# Add API
address = "https://api.ok-ex.io"
subaddress = "/api/v2/otc/estimate"
parameters =  {"fromAsset": "USDT", "amount": 1, "side": "BUY", "mode": "AMOUNT"}
parameters_signature =  "?fromAsset=USDT&amount=1&side=BUY&mode=AMOUNT"
sig = create_signature(secret_key = secret_key, full_path =  subaddress + parameters_signature, 
                       request_method = "POST", request_data = parameters)
headers = {"Content-Type": "application/json", "x-api-key":   API, "x-signature": sig[0], "x-timestamp": str(sig[1])}
r = requests.post(url = address + subaddress + parameters_signature, headers= headers)
print(r) 
data = r.json()
print(data)
