import requests
from requests.auth import HTTPBasicAuth
import json

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError, LineBotApiError)
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage,
                            ImageSendMessage,
                            LocationSendMessage)


line_bot_api = LineBotApi(
    'De/YjcShFjyEChrC7haHK3TS0gipxCL6796otKJTP18QiT8s8DnwlJ6IGAccac7WWyu9rcHeqSV/vVtBKP/MS2nacg/rIqceFeTeI1wMc5EeZXqUoNuwR1CZpyUdhow7WuToG3tWKEQSSb/9pRo09gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('26cf4066fdc23ca3f183da031edd67b5')
