import requests
import json
import os

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError, LineBotApiError)
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage,
                            ImageSendMessage,
                            LocationSendMessage)

load_dotenv()

line_bot_api = LineBotApi(os.getenv("LINE_BOT_API_KEY"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

print(line_bot_api)
