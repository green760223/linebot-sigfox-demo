import requests
import pytz
import json

from line_bot_api import *
from sigfox_api import *
from datetime import datetime


def event_location(event):
    user_id = event.source.user_id
    device_id = event.message.text

    information_api_url = 'https://api.sigfox.com/v2/devices/417EAD'

    req = requests.get(information_api_url,
                       auth=HTTPBasicAuth(api_account, api_password))
    device_info = json.loads(req.text)
    print(device_info)

    device_lat = device_info['location']['lat']
    device_lng = device_info['location']['lng']
    device_name = device_info['name']

    print(device_lat, device_lng, device_name)

    line_bot_api.reply_message(
        event.reply_token,
        [LocationSendMessage(
            title='device_name',
            address='test',
            latitude=device_lat,
            longitude=device_lng)])
