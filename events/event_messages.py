from line_bot_api import *
from sigfox_api import *


def event_messages(event):


    line_bot_api.reply_message(
        event.reply_token,
        [ImageSendMessage(original_content_url=image_url,
                          preview_image_url=image_url),
         TextSendMessage(text='設備ID：{}'.format(device_id) +
                              '\n' + '設備名稱：{}'.format(device_name) +
                              '\n' + '最後通訊時間：{}'.format(device_last_time) +
                              '\n' + '設備狀態：{}'.format(device_activated))])

