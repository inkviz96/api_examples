from datetime import datetime
from urllib.parse import urlencode

import requests
import json
import hmac
import hashlib
import base64


def huobi_api(method: str, endpoint: str, data: dict = None):
    access_api_key = ''
    secret_key = ''
    base_uri = 'api.huobi.pro'

    params = urlencode({
        'AccessKeyId': str(access_api_key),
        'SignatureMethod': 'HmacSHA256',
        'SignatureVersion': '2',
        'Timestamp': str(datetime.utcnow().isoformat())[0:19],
    })
    pre_signed_text = f'{method}\n{base_uri}\n{endpoint}\n{params}'
    hash_code = hmac.new(secret_key.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
    signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})
    url = f'https://{base_uri}{endpoint}?{params}&{signature}'
    response = requests.request(method, url, json=data)
    return json.loads(response.text)

# Get Fee for huobi withdraw
method = 'GET'
endpoint = '/v2/reference/currencies'
data = {'currency': 'btc'}
response = huobi_api(method=method, endpoint=endpoint, data=data)
fee = None
for x in response['data']:
    if x['currency'] == 'btc':
        for y in x['chains']:
            if y['chain'] == 'hrc20btc':
                fee = y['transactFeeWithdraw']

# Withdraw from huobi
data = {
        'address': 'some_address', 'amount': '1111.1111',
        'currency': 'btc', 'fee': fee, 'chain': 'hrc20btc'
    }
method = 'POST'
endpoint = '/v1/dw/withdraw/api/create'
withdraw_id = huobi_api(method=method, endpoint=endpoint, data=data)
