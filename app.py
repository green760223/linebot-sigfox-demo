from line_bot_api import *
from flask import Flask, request, abort

import pytz
from datetime import datetime

from database import db_session, init_db
from models.users import User

from events.event_location import event_location
from events.event_messages import event_messages
from events.event_register import event_register, device_id_input_event
from events.event_status import event_status

app = Flask(__name__)


# 初始化資料庫
@app.before_first_request
def init():
    init_db()


# 關閉 db session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    user_id = event.source.user_id

    # user = User.query.filter(User.id == user_id).first()

    # if not user:
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text='Please add a device ID!(ex: @device417AED)'))

    if message_text == '@status':
        event_status(event)
    elif message_text == '@location':
        event_location(event)
    elif message_text == '@register':
        device_id_input_event(event)
    elif message_text == '@message':
        event_messages(event)
    elif message_text.startswith('@設備'):
        event_register(event)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請重新輸入有效關鍵字!'))


@app.route('/devkit/push_message', methods=['POST'])
def push_message():
    request_data = request.get_json()
    print(request_data)

    users = User.query.all()
    for user in users:
        print(user.id)

    # 8709d1095a0a
    # ambient_temperature=8709 -> 0987
    # ambient_humidity=d109 -> 09d1
    # module_temperature=5a0a -> 0a5a
    payload = request_data['data']

    raw_ambient_temperature = payload[2:4] + payload[0:2]
    ambient_temperature = int(raw_ambient_temperature, 16) / 100
    raw_ambient_humidity = payload[6:8] + payload[5:7]
    ambient_humidity = int(raw_ambient_humidity, 16) / 100
    raw_module_temperature = payload[11:13] + payload[8:10]
    module_temperature = int(raw_module_temperature, 16) / 100

    device_id = request_data['device']

    # msg_time = 1620417645
    lat = request_data['fixedLat']
    lng = request_data['fixedLng']
    msg_time = int(request_data['time'])
    device_msg_time = datetime.fromtimestamp(msg_time).astimezone(tz=pytz.timezone('Asia/Taipei'))\
        .strftime('%Y-%m-%d %H:%M:%S')

    if ambient_humidity < 70:
        for user in users:
            line_bot_api.push_message(user.id,
                                      messages=[TextSendMessage(text='＊＊＊警告＊＊＊' + '\n'
                                                                '時間：{}'.format(device_msg_time) + '\n'
                                                                '設備ID：{}'.format(device_id) +
                                                                '目前濕度為{}%'.format(ambient_humidity) +
                                                                '，已超出臨界值70%!'),
                                                LocationSendMessage(title='設備ID-{}'.format(device_id),
                                                                    address='高雄市大樹區學城路一段1號',
                                                                    latitude=lat,
                                                                    longitude=lng)])

    return "200"


if __name__ == "__main__":
    app.run()
