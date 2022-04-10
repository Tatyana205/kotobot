import json
import random

import pandas as pd
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

vk_session = vk_api.VkApi(token='4b2134ee4257eb8d3754b172bdcbb5f559a81f23327905aa9e00d52c4c383f615796b4cd7dc9dafbcff16')

color = VkKeyboardColor.SECONDARY

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Ответить на вопросы', color=VkKeyboardColor.PRIMARY, payload='1')
keyboard.add_line()
keyboard.add_button('Мем', color=VkKeyboardColor.POSITIVE, payload='2')
keyboard.add_button('Статистика', color=VkKeyboardColor.NEGATIVE, payload='3')

keyboard1 = VkKeyboard(one_time=True)
keyboard1.add_button('Синего', color=VkKeyboardColor.PRIMARY, payload='10')
keyboard1.add_button('Белого', color=VkKeyboardColor.SECONDARY, payload='11')
keyboard1.add_line()
keyboard1.add_button('Красного', color=VkKeyboardColor.NEGATIVE, payload='12')
keyboard1.add_button('Зелёного', color=VkKeyboardColor.POSITIVE, payload='13')

keyboard9 = VkKeyboard(one_time=True)
keyboard9.add_button('👍', color=VkKeyboardColor.SECONDARY, payload='90')
keyboard9.add_button('👎', color=VkKeyboardColor.SECONDARY, payload='91')

attachment = dict.fromkeys(range(19, 69))

data = pd.read_csv('data.csv', encoding='ISO-8859-1')
print(data)


# ToDo Try except

def msg(message, kb):
    vk.messages.send(
        user_id=event.message.from_id,
        random_id=get_random_id(),
        message=message,
        keyboard=kb
    )


def upload_memes():
    if str(float(event.message.from_id)) not in list(data['users']):
        data.loc[len(data)] = [float(event.message.from_id)] + ['None'] * 50
        data.to_csv(r'data.csv', index=False)
    print(data['users'])
    i = list(data['users']).index(float(event.message.from_id))
    at = [x for x in range(19, 69) if (data[str(x)][i] != 'True') and (data[str(x)][i] != 'False')]
    if len(at) != 0:
        rand = random.choice(at)
        vk.messages.send(
            user_id=event.message.from_id,
            random_id=get_random_id(),
            message='',
            attachment=f'photo-212547487_4572390{rand}',
            keyboard=keyboard9.get_keyboard()
        )
        return rand, i
    else:
        msg('Пока вы посмотрели все мемы, жду вас позже', keyboard.get_empty_keyboard())
        return None


def statistics():
    i = list(data['users']).index(str(float(event.message.from_id)))
    l = len([x for x in range(19, 69) if data[str(x)][i] == 'True'])
    d = len([x for x in range(19, 69) if data[str(x)][i] == 'False'])
    msg(f'Количество лайков: {l}\nКоличество дизлайков: {d}', keyboard.get_empty_keyboard())


meme_id = 0
longpoll = VkBotLongPoll(vk_session, 212547487)
vk = vk_session.get_api()
while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.message.payload:
                if event.message.payload == '1':
                    msg('1. Какого цвета сделать кнопки?', keyboard1.get_keyboard())
                elif event.message.payload == '10':
                    color = VkKeyboardColor.PRIMARY
                elif event.message.payload == '11':
                    color = VkKeyboardColor.SECONDARY
                elif event.message.payload == '12':
                    color = VkKeyboardColor.NEGATIVE
                elif event.message.payload == '13':
                    color = VkKeyboardColor.POSITIVE
                if (event.message.payload == '10') or (event.message.payload == '11') or (
                        event.message.payload == '12') or (event.message.payload == '13'):
                    keyboard2 = VkKeyboard(one_time=True)
                    keyboard2.add_button('Положительно', color=color, payload='20')
                    keyboard2.add_button('Нейтрально', color=color, payload='21')
                    keyboard2.add_line()
                    keyboard2.add_button('Отношусь', color=color, payload='22')
                    msg('2. Как вы относитесь к котикам?', keyboard2.get_keyboard())
                elif event.message.payload == '20':
                    msg('Это прекрасно! Значит, мы можем подружиться)', keyboard.get_empty_keyboard())
                elif event.message.payload == '21':
                    msg('Я вас понял', keyboard.get_empty_keyboard())
                elif event.message.payload == '22':
                    msg('Получается, мы родные души)', keyboard.get_empty_keyboard())
                if (event.message.payload == '20') or (event.message.payload == '21') or (
                        event.message.payload == '22'):
                    keyboard3_1 = VkKeyboard(one_time=True)
                    keyboard3_1.add_button('Да', color=color, payload='30')
                    keyboard3_1.add_button('Нет', color=color, payload='31')
                    msg('3. Готовы рассказать о том, где вы сейчас находитесь?', keyboard3_1.get_keyboard())
                elif event.message.payload == '30':
                    keyboard3_2 = VkKeyboard(one_time=True)
                    keyboard3_2.add_location_button(payload='32')
                    msg('Тогда можете поделиться своей геопозицией', keyboard3_2.get_keyboard())
                elif event.message.payload == '31':
                    msg('Тогда перейдём к следующему вопросу', keyboard.get_empty_keyboard())
                elif event.message.payload == '32':
                    msg('Хорошо, что расстояние не мешает нашему общению', keyboard.get_empty_keyboard())
                if (event.message.payload == '31') or (event.message.payload == '32'):
                    keyboard4 = VkKeyboard(one_time=True)
                    keyboard4.add_openlink_button(label='Открыть видосик',
                                                  link='https://vk.com/video-130936589_456240749')
                    keyboard4.add_button('Следующий пункт', color=color, payload='40')
                    msg('4. Предлагаю отвлечься от дел и посмотреть на котика', keyboard4.get_keyboard())
                if event.message.payload == '40':
                    keyboard5 = VkKeyboard(one_time=True)
                    keyboard5.add_callback_button(label='Посмотреть сообщение',
                                                  color=color,
                                                  payload={'type': 'show_snackbar', 'text': 'Мур'})
                    msg('5. У меня есть для вас сообщение', keyboard5.get_keyboard())
                if event.message.payload == '60':
                    keyboard7 = VkKeyboard(one_time=True)
                    keyboard7.add_vkpay_button(hash='action=transfer-to-group&group_id=212547487', payload='70')
                    keyboard7.add_line()
                    keyboard7.add_button('В другой раз', color=color, payload='71')
                    msg('7. Вы непротив порадовать Котокодеров монеткой?', keyboard7.get_keyboard())
                elif event.message.payload == '70':
                    msg('Мурси)', keyboard.get_empty_keyboard())
                if (event.message.payload == '70') or (event.message.payload == '71'):
                    keyboard8 = VkKeyboard(one_time=True)
                    keyboard8.add_button('До встречи!', color=color, payload='8')
                    msg('8. Было очень приятно пообщаться с вами!', keyboard8.get_keyboard())
                if event.message.payload == '8':
                    msg('🐾', keyboard.get_empty_keyboard())
                elif event.message.payload == '2':
                    meme_id = upload_memes()
                elif event.message.payload == '90':
                    data[str(meme_id[0])][meme_id[1]] = True
                    data.to_csv(r'data.csv')
                    # at.remove(meme_id)
                elif event.message.payload == '91':
                    data[str(meme_id[0])][meme_id[1]] = False
                    data.to_csv(r'data.csv')
                    # at.remove(meme_id)
                elif event.message.payload == '3':
                    statistics()
            else:
                if event.message.text.lower() == 'привет':
                    msg('Привет вездекодерам!', keyboard.get_keyboard())
                elif event.message.text.lower() == 'мем':
                    meme_id = upload_memes()
                elif event.message.text.lower() == 'статистика':
                    statistics()
                else:
                    msg('Я пока не знаю, что тебе ответить, но я работаю над этим', keyboard.get_empty_keyboard())
        else:
            if event.object.payload.get('type') == 'show_snackbar':
                vk.messages.send_message_event_answer(
                    event_id=event.object.event_id,
                    user_id=event.object.user_id,
                    random_id=get_random_id(),
                    peer_id=event.object.peer_id,
                    event_data=json.dumps(event.object.payload))

                keyboard6 = VkKeyboard(one_time=True)
                keyboard6.add_vkapps_button(label='Вперёд за идеями', app_id=7598034,
                                            owner_id=197700721, hash='')
                keyboard6.add_button('Двигаемся дальше', color=color, payload='60')

                vk.messages.send(
                    user_id=event.object.user_id,
                    random_id=get_random_id(),
                    message='6. Как насчёт генерации идеи для стартапа?',
                    keyboard=keyboard6.get_keyboard()
                )
