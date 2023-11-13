from line_bot_api import *
from models.users import User
from database import db_session


def device_id_input_event(event):
    msg = event.message.text
    registration = '您尚未新增設備，請輸入設備ID! (如格式: @設備417AED)'
    if msg == '@register':
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=registration))


def event_register(event):
    msg = event.message.text
    user_id = event.source.user_id

    device = msg.split('@設備')[1]
    device_id = device.upper()

    is_user = User.query.filter(User.id == user_id).first()

    if not is_user:
        user = User(id=user_id, device_id=device_id)
        db_session.add(user)
        db_session.commit()
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='新增成功!'))
