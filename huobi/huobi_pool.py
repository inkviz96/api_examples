import requests
import hashlib
from datetime import date, datetime
from urllib.parse import urlencode
import json



def huobi_pool_api(method: str, endpoint: str, data: dict = None):
    base_uri = 'openapi.hpt.com'
    date_today = date.today()
    ts = str(int(datetime.now().timestamp()*10**3))
    params = f'access_key=access_key&date={date_today}&sub_code=sub_code&timestamp={ts}&secret_key=secret_key'
    print(params)
    hash_code = hashlib.sha256(params.encode()).hexdigest()
    params = urlencode({
        'sub_code': "SUB_CODE",
        'access_key': "ACCESS_KEY",
        'date': date_today,
        'sign': hash_code.upper(),
        'timestamp': ts,
    })
    url = f'https://{base_uri}{endpoint}?{params}'
    response = requests.request(method, url, json=data)
    return json.loads(response.text)

# Get daily mining profit
method = 'GET'
endpoint = '/open/api/user/v1/daily_profit'
pool_response = huobi_pool_api(method=method, endpoint=endpoint)
pool_response['data'][0]['amount']