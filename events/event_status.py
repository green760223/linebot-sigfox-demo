from line_bot_api import *

from sigfox_api import *

from models.users import User

from datetime import datetime
import pytz


def event_status(event):
    user_id = event.source.user_id

    user = User.query.filter(User.id == user_id).first()
    device_id = user.device_id
    print('user.device_id:', device_id)
    print('user.id:', user.id)

    if not user:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='您尚未新增設備，請輸入設備ID! (如格式: @設備417AED)'))
    else:
        user = User.query.filter(User.id == user_id).first()
        device_id = user.device_id
        image_url = 'https://i.imgur.com/gv8ZNIw.jpg'
        information_api_url = 'https://api.sigfox.com/v2/devices/{}'.format(device_id)

        req = requests.get(information_api_url,
                           auth=HTTPBasicAuth(api_account, api_password))

        print(req.status_code)
        print('url:', information_api_url)

        if req.status_code == 200:
            device_info = json.loads(req.text)
            device_name = device_info['name']
            device_last_com = device_info['lastCom']
            device_last_time = datetime.fromtimestamp(device_last_com / 1000).astimezone(
                tz=pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')
            device_activated = device_info['activable']

            # print(device_info['id'], device_info['name'], device_info['lastCom'], device_info['activable'])

            line_bot_api.reply_message(
                event.reply_token,
                [ImageSendMessage(original_content_url=image_url,
                                  preview_image_url=image_url),
                 TextSendMessage(text='設備ID：{}'.format(device_id) +
                                      '\n' + '設備名稱：{}'.format(device_name) +
                                      '\n' + '最後通訊時間：{}'.format(device_last_time) +
                                      '\n' + '設備狀態：{}'.format(device_activated))])
