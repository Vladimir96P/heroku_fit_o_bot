import telebot
from telebot import types
import datetime as dt
import psycopg2
from bob_telegram_tools.bot import TelegramBot
import matplotlib.pyplot as plt

bot = telebot.TeleBot("5058162485:AAGSB2FehnhupFU5ViiEwRgypDMJmddcpmg")
bot.delete_webhook()
db_URL = "postgres://qmvydayqnuuxxz:40dc9792c9d15977ed989756198fbbba01983157173a98d5840e92c8c71928a8@ec2-54-74-102-48.eu-west-1.compute.amazonaws.com:5432/dcanatqglrancq"
db_con = psycopg2.connect(db_URL, sslmode = "require")
backslash = "\\"
warning = "Рекомендация носит исключительно ознакомительный характер\\. Перед применением проконсультируйтесь со специалистом\\."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, '''Хэй\! Меня зовут Фитобот😊 А тебя как? Напиши, пожалуйста: свое *имя*, *возраст*, *рост* \(в сантиметрах\) и *пол* \(русскоязычной раскладкой м/ж\) на моем примере \(обязательно следуй формату, если с первого раза не получится \- вызови повторно команду start и повтори попытку, данные пишем через пробел\):
    \n*Фитобот 25 175 М*''', parse_mode="MarkdownV2")
    bot.register_next_step_handler(msg, user_name)

def send_keyboard(message, text = "Выбери интересующий раздел 😉"):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    itembtn0 = types.KeyboardButton('Хочу сообщить свой вес 😱')
    itembtn1 = types.KeyboardButton('Хочу посмотреть статистику веса 😈')
    itembtn2 = types.KeyboardButton('Хочу согнать жирок 🥦')
    itembtn3 = types.KeyboardButton('Хочу набрать массу 💪')
    itembtn9 = types.KeyboardButton('Поддержание текущего веса 🥳')
    itembtn4 = types.KeyboardButton('Удалить последнюю запись веса')
    itembtn5 = types.KeyboardButton("Удалить все записи веса")
    itembtn6 = types.KeyboardButton("Не худею/не набираю 👿")
    itembtn7 = types.KeyboardButton("Очистить данные из базы (имя, возраст, пол, рост)")
    itembtn8 = types.KeyboardButton('Хочу сообщить % подкожного жира 🐻')
    keyboard.add(itembtn0, itembtn1, itembtn8, itembtn2, itembtn3, itembtn9, itembtn4, itembtn5, itembtn6, itembtn7)
    msg = bot.send_message(message.from_user.id,text=text, reply_markup=keyboard)
    bot.register_next_step_handler(msg, callback_worker)

def user_name(msg):
    try:
        name = msg.text.split()[0].title()
        age = msg.text.split()[1]
        age = int(age)
        height = msg.text.split()[2]
        height = int(height)
        sex = msg.text.split()[3].title()
        if sex == 'М' or sex == 'Ж':
            try:
                with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                    db_obj = postgre_con.cursor()
                    db_obj.execute(f'DELETE FROM bot_users_list WHERE "user_id"={msg.from_user.id}')
                    postgre_con.commit()
                    db_obj.execute(
                        '''INSERT INTO bot_users_list (user_id, name, age, height, sex) 
                        VALUES (%s, %s, %s, %s, %s);''', (msg.from_user.id, name, age, height, sex))
                    postgre_con.commit()
                    db_obj.close()
                    message = bot.send_message(msg.from_user.id, f'''Привет! Приятно познакомиться, {name} 😜. Выбирай интересующую тебя тему:) И при первом использовании не забудь ввести свой текущий вес!)''')
                    send_keyboard(msg)
            except:
                with psycopg2.connect(db_URL, sslmode = "require") as postgre_con:
                    db_obj = postgre_con.cursor()
                    db_obj.execute(
                        '''INSERT INTO bot_users_list (user_id, name, age, height, sex) 
                        VALUES (%s, %s, %s, %s, %s);''', (msg.from_user.id, name, age, height, sex))
                    postgre_con.commit()
                    db_obj.close()
                    message = bot.send_message(msg.from_user.id, f'''Привет! Приятно познакомиться, {name} 😜. Выбирай интересующую тебя тему:) И при первом использовании не забудь ввести свой текущий вес!)''')
                    send_keyboard(msg)
    except Exception as e:
        bot.reply_to(msg, 'Что-то не так.. проверь корректность ввода и давай попробуем еще раз 🙏')

def activity_keyboard(message, text):
    activitykeyboard = types.ReplyKeyboardMarkup(row_width=1)
    but0 = types.KeyboardButton('Офисная улитка 🐌')
    but1 = types.KeyboardButton('До 3-х кардио/фитнес тренировки 🏊‍♂️🤸‍♂️ в неделю')
    but2 = types.KeyboardButton('3 силовые/высокоинтервальные тренировки в неделю 🏋️ 🔥 🏋️')
    but3 = types.KeyboardButton('Более 3-х силовых/высокоинтервальных тренировок в неделю 🤖 👺')
    activitykeyboard.add(but0, but1, but2, but3)
    msg = bot.send_message(message.from_user.id, '''
    В соответствии со своей активностью нажми на нужую кнопку 😉.
    \n- Офисная улитка 🐌 (обычно передвигаешь свое тело до ближайшей кофейни или метро и на этом все)
    \n- До 3-х кардио/фитнес тренировки 🏊‍♂️🤸‍♂️ в неделю (немного занимаешься спортом, но нагрузки небольшие)
    \n- 3 силовые/высокоинтервальные тренировки в неделю 🏋️ 🔥 🏋 ️(это уже что-то посерьезнее, ты тренируешься тяжело, на прогресс)
    \n- Более 3-х силовых/высокоинтервальных тренировки в неделю 🤖 👺 ️(очень большая активность, можно сказать ты живешь спортом)
    ''', reply_markup = activitykeyboard)
    if text == "Хочу набрать массу 💪":
        bot.register_next_step_handler(msg, increase_weight_diet)
    elif text == "Хочу согнать жирок 🥦":
        bot.register_next_step_handler(msg, diet_type)
    elif text == "Поддержание текущего веса 🥳":
        bot.register_next_step_handler(msg, weight_sup)

def increase_weight_diet(message):
    activitykeyboard = types.ReplyKeyboardMarkup(row_width=1)
    b0 = types.KeyboardButton('Плавный набор сухой массы 🐅')
    b1 = types.KeyboardButton('Активный набор 🦍')
    activitykeyboard.add(b0, b1)
    msg = bot.send_message(message.from_user.id, f'''
    Что выбираешь?
    \n◌ *Плавный набор* {backslash}- более чистый набор, без лишних жировых отложений{backslash}. Подходит для склонных к полноте людей 😉
    \n◌ *Активный набор* {backslash}- активный набор массы{backslash}. Подходит для тех, кому тяжело набрать 😎
    ''', reply_markup = activitykeyboard, parse_mode="MarkdownV2")
    if message.text == "Офисная улитка 🐌":
        bot.register_next_step_handler(msg, office_activity_increase)
    elif message.text == 'До 3-х кардио/фитнес тренировки 🏊‍♂️🤸‍♂️ в неделю':
        bot.register_next_step_handler(msg, fitness_activity_increase)
    elif message.text == '3 силовые/высокоинтервальные тренировки в неделю 🏋️ 🔥 🏋️':
        bot.register_next_step_handler(msg, gym_activity_increase)
    elif message.text == 'Более 3-х силовых/высокоинтервальных тренировок в неделю 🤖 👺':
        bot.register_next_step_handler(msg, advanced_activity_increase)

def diet_type(message):
    activitykeyboard = types.ReplyKeyboardMarkup(row_width=1)
    b0 = types.KeyboardButton('Низкоуглеводка 🍤🥜🥩')
    b1 = types.KeyboardButton('Классика 🍝🍗🥙')
    activitykeyboard.add(b0, b1)
    msg = bot.send_message(message.from_user.id, f'''
    Что выбираешь?
    \n◌ *Низкоуглеводка* {backslash}- имеет ряд противопоказаний{backslash}. Но также имеет и ряд положительных свойств 😉
    \n◌ *Классика* {backslash}- общепринятые пропорции белков, жиров и углеводов{backslash}.
    ''', reply_markup = activitykeyboard, parse_mode="MarkdownV2")
    if message.text == "Офисная улитка 🐌":
        bot.register_next_step_handler(msg, office_activity_decrease)
    elif message.text == 'До 3-х кардио/фитнес тренировки 🏊‍♂️🤸‍♂️ в неделю':
        bot.register_next_step_handler(msg, fitness_activity_decrease)
    elif message.text == '3 силовые/высокоинтервальные тренировки в неделю 🏋️ 🔥 🏋️':
        bot.register_next_step_handler(msg, gym_activity_decrease)
    elif message.text == 'Более 3-х силовых/высокоинтервальных тренировок в неделю 🤖 👺':
        bot.register_next_step_handler(msg, advanced_activity_decrease)

def office_activity_increase(msg):
    try:
        if msg.text == "Плавный набор сухой массы 🐅":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 450)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 500
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nУ тебя низкая активность, добавь прогулки и ежедневные отжимания с приседаниями дома{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nУ тебя низкая активность, добавь прогулки и ежедневные отжимания с приседаниями дома{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 600)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 300
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.40 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.45 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nУ тебя низкая активность, добавь прогулки и ежедневные отжимания с приседаниями дома{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nУ тебя низкая активность, добавь прогулки и ежедневные отжимания с приседаниями дома{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
        elif msg.text == "Активный набор 🦍":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 450)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 1000
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nУ тебя низкая активность{backslash}. Если нет противопоказаний *обязательно* добавь прогулки и ежедневные отжимания с приседаниями дома{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nУ тебя низкая активность{backslash}. Если нет противопоказаний *обязательно* добавь прогулки и ежедневные отжимания с приседаниями дома{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 600)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 650
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.40 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.45 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nУ тебя низкая активность{backslash}. Если нет противопоказаний *обязательно* добавь прогулки и ежедневные отжимания с приседаниями дома{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nУ тебя низкая активность{backslash}. Если нет противопоказаний *обязательно* добавь прогулки и ежедневные отжимания с приседаниями дома{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
    except Exception as e:
        bot.send_message(msg.chat.id, '''
        Кажется, мне не достает данных, проверь был ли введен вес и первичные данные, которые вводились на старте 😉
        ''')
        send_keyboard(msg)

def fitness_activity_increase(msg):
    try:
        if msg.text == "Плавный набор сухой массы 🐅":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 450)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 600
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 600)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 400
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.40 * target_calories) / 9)
                        protein_nutrient = round((0.20 * target_calories) / 4)
                        carbs_nutrient = round((0.4 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
        elif msg.text == "Активный набор 🦍":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round(0.8 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 1200
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round(0.8 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 850
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.4 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.45 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
    except Exception as e:
        bot.send_message(msg.chat.id, '''
        Кажется, мне не достает данных, проверь был ли введен вес и первичные данные, которые вводились на старте 😉
        ''')
        send_keyboard(msg)

def gym_activity_increase(msg):
    try:
        if msg.text == "Плавный набор сухой массы 🐅":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 450)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 850
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 600)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 650
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.40 * target_calories) / 9)
                        protein_nutrient = round((0.20 * target_calories) / 4)
                        carbs_nutrient = round((0.40 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
        elif msg.text == "Активный набор 🦍":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round(0.8 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 1700
                    water_quantity = round(((target_calories / 1000) * 1), 2)
                    fat_nutrient = round((0.2 * target_calories) / 9)
                    protein_nutrient = round((0.25 * target_calories) / 4)
                    carbs_nutrient = round((0.55 * target_calories) / 4)
                    last_weight_str = str(last_weight).replace('.', '\.')
                    water_quantity_str = str(water_quantity).replace('.', '\.')
                    bot.send_message(msg.chat.id, f'''
                    🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                    \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                    \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                    \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                    \n★ *{fat_nutrient}* г жиров;
                    \n★ *{protein_nutrient}* г белков;
                    \n★ *{carbs_nutrient}* г углеводов{backslash}.
                    \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                    \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                    \n{warning}
                    \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                    \nУдачи{backslash}! Все получится ☺️
                    ''', parse_mode="MarkdownV2")
                    send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round(0.8 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 1000
                    water_quantity = round((target_calories / 1000), 2)
                    fat_nutrient = round((0.2 * target_calories) / 9)
                    protein_nutrient = round((0.25 * target_calories) / 4)
                    carbs_nutrient = round((0.55 * target_calories) / 4)
                    last_weight_str = str(last_weight).replace('.', '\.')
                    water_quantity_str = str(water_quantity).replace('.', '\.')
                    bot.send_message(msg.chat.id, f'''
                    🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                    \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                    \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                    \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                    \n★ *{fat_nutrient}* г жиров;
                    \n★ *{protein_nutrient}* г белков;
                    \n★ *{carbs_nutrient}* г углеводов{backslash}.
                    \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                    \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                    \n{warning}
                    \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                    \nУдачи{backslash}! Все получится ☺️
                    ''', parse_mode="MarkdownV2")
                    send_keyboard(msg)
    except Exception as e:
        bot.send_message(msg.chat.id, '''
        Кажется, мне не достает данных, проверь был ли введен вес и первичные данные, которые вводились на старте 😉
        ''')
        send_keyboard(msg)

def advanced_activity_increase(msg):
    try:
        if msg.text == "Плавный набор сухой массы 🐅":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 450)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 1400
                    water_quantity = round((target_calories / 1000), 2)
                    fat_nutrient = round((0.2 * target_calories) / 9)
                    protein_nutrient = round((0.25 * target_calories) / 4)
                    carbs_nutrient = round((0.55 * target_calories) / 4)
                    last_weight_str = str(last_weight).replace('.', '\.')
                    water_quantity_str = str(water_quantity).replace('.', '\.')
                    bot.send_message(msg.chat.id, f'''
                    🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                    \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                    \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                    \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                    \n★ *{fat_nutrient}* г жиров;
                    \n★ *{protein_nutrient}* г белков;
                    \n★ *{carbs_nutrient}* г углеводов{backslash}.
                    \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                    \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                    \n{warning}
                    \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                    \nУдачи{backslash}! Все получится ☺️
                    ''', parse_mode="MarkdownV2")
                    send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 600)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 1000
                    water_quantity = round((target_calories / 1000), 2)
                    fat_nutrient = round((0.2 * target_calories) / 9)
                    protein_nutrient = round((0.25 * target_calories) / 4)
                    carbs_nutrient = round((0.55 * target_calories) / 4)
                    last_weight_str = str(last_weight).replace('.', '\.')
                    water_quantity_str = str(water_quantity).replace('.', '\.')
                    bot.send_message(msg.chat.id, f'''
                    🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                    \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                    \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                    \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                    \n★ *{fat_nutrient}* г жиров;
                    \n★ *{protein_nutrient}* г белков;
                    \n★ *{carbs_nutrient}* г углеводов{backslash}.
                    \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                    \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                    \n{warning}
                    \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                    \nУдачи{backslash}! Все получится ☺️
                    ''', parse_mode="MarkdownV2")
                    send_keyboard(msg)
        elif msg.text == "Активный набор 🦍":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round(0.8 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 2000
                    water_quantity = round(((target_calories / 1000) * 1), 2)
                    fat_nutrient = round((0.2 * target_calories) / 9)
                    protein_nutrient = round((0.25 * target_calories) / 4)
                    carbs_nutrient = round((0.55 * target_calories) / 4)
                    last_weight_str = str(last_weight).replace('.', '\.')
                    water_quantity_str = str(water_quantity).replace('.', '\.')
                    bot.send_message(msg.chat.id, f'''
                    🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                    \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                    \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                    \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                    \n★ *{fat_nutrient}* г жиров;
                    \n★ *{protein_nutrient}* г белков;
                    \n★ *{carbs_nutrient}* г углеводов{backslash}.
                    \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                    \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                    \n{warning}
                    \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                    \nУдачи{backslash}! Все получится ☺️
                    ''', parse_mode="MarkdownV2")
                    send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round(0.8 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 1400
                    water_quantity = round((target_calories / 1000), 2)
                    fat_nutrient = round((0.2 * target_calories) / 9)
                    protein_nutrient = round((0.25 * target_calories) / 4)
                    carbs_nutrient = round((0.55 * target_calories) / 4)
                    last_weight_str = str(last_weight).replace('.', '\.')
                    water_quantity_str = str(water_quantity).replace('.', '\.')
                    bot.send_message(msg.chat.id, f'''
                    🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                    \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                    \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                    \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                    \n★ *{fat_nutrient}* г жиров;
                    \n★ *{protein_nutrient}* г белков;
                    \n★ *{carbs_nutrient}* г углеводов{backslash}.
                    \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                    \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                    \n{warning}
                    \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                    \nУдачи{backslash}! Все получится ☺️
                    ''', parse_mode="MarkdownV2")
                    send_keyboard(msg)
    except Exception as e:
        bot.send_message(msg.chat.id, '''
        Кажется, мне не достает данных, проверь был ли введен вес, процент подкожного жира и первичные данные, которые вводились на старте 😉
        ''')
        send_keyboard(msg)

def office_activity_decrease(msg):
    try:
        if msg.text == "Низкоуглеводка 🍤🥜🥩":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 450)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nВвиду твоей низкой активности и желания поджечь жирок *установим* целевую суточную *калорийность равную BMR*{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 600)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.40 * target_calories) / 9)
                        protein_nutrient = round((0.40 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nВвиду твоей низкой активности и желания поджечь жирок установим целевую суточную *калорийность равную BMR*{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
        elif msg.text == "Классика 🍝🍗🥙":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round(0.8 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nВвиду твоей низкой активности и желания поджечь жирок *установим* целевую суточную *калорийность равную BMR*{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round(0.8 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.4 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.45 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nВвиду твоей низкой активности и желания поджечь жирок установим целевую суточную *калорийность равную BMR*{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
    except Exception as e:
        bot.send_message(msg.chat.id, '''
        Кажется, мне не достает данных, проверь был ли введен вес и первичные данные, которые вводились на старте 😉
        ''')
        send_keyboard(msg)

def fitness_activity_decrease(msg):
    try:
        if msg.text == "Низкоуглеводка 🍤🥜🥩":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 450)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 200
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 600)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 100
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.40 * target_calories) / 9)
                        protein_nutrient = round((0.40 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
        elif msg.text == "Классика 🍝🍗🥙":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round(0.8 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 200
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round(0.8 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 100
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.4 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.45 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
    except Exception as e:
        bot.send_message(msg.chat.id, '''
        Кажется, мне не достает данных, проверь был ли введен вес и первичные данные, которые вводились на старте 😉
        ''')
        send_keyboard(msg)

def gym_activity_decrease(msg):
    try:
        if msg.text == "Низкоуглеводка 🍤🥜🥩":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 450)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 450
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 600)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 250
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.40 * target_calories) / 9)
                        protein_nutrient = round((0.40 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
        elif msg.text == "Классика 🍝🍗🥙":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round(0.8 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 450
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round(0.8 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 250
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.4 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.45 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
    except Exception as e:
        bot.send_message(msg.chat.id, '''
        Кажется, мне не достает данных, проверь был ли введен вес и первичные данные, которые вводились на старте 😉
        ''')
        send_keyboard(msg)

def advanced_activity_decrease(msg):
    try:
        if msg.text == "Низкоуглеводка 🍤🥜🥩":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 450)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 800
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round((1.2 * (10 * last_weight) + (6.25 * height) - (5 * age) + 5) - 600)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 400
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.40 * target_calories) / 9)
                        protein_nutrient = round((0.40 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.30 * target_calories) / 9)
                        protein_nutrient = round((0.50 * target_calories) / 4)
                        carbs_nutrient = round((0.20 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nПосле месяца низкоуглеводного питания рекомендую перейти на классическое{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
        elif msg.text == "Классика 🍝🍗🥙":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round(0.8 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 800
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round(0.8 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 400
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.4 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.45 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
    except Exception as e:
        bot.send_message(msg.chat.id, '''
        Кажется, мне не достает данных, проверь был ли введен вес, процент подкожного жира и первичные данные, которые вводились на старте 😉
        ''')
        send_keyboard(msg)

def weight_sup(msg):
    try:
        if msg.text == "Офисная улитка 🐌":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round(0.8 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 200
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составляет *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.35*200/9)}* г жиров;
                        \n★ *{int(0.15*200/4)}* г белков;
                        \n★ *{int(0.5*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.35*200/9)}* г жиров;
                        \n★ *{int(0.15*200/4)}* г белков;
                        \n★ *{int(0.5*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round(0.8 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 100
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.4 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.45 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.4*200/9)}* г жиров;
                        \n★ *{int(0.15*200/4)}* г белков;
                        \n★ *{int(0.45*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.35*200/9)}* г жиров;
                        \n★ *{int(0.15*200/4)}* г белков;
                        \n★ *{int(0.5*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
        elif msg.text == 'До 3-х кардио/фитнес тренировки 🏊‍♂️🤸‍♂️ в неделю':
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round(0.8 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 400
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составляет *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.35*200/9)}* г жиров;
                        \n★ *{int(0.15*200/4)}* г белков;
                        \n★ *{int(0.5*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.35*200/9)}* г жиров;
                        \n★ *{int(0.15*200/4)}* г белков;
                        \n★ *{int(0.5*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round(0.8 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 220
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.4 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.45 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.4*200/9)}* г жиров;
                        \n★ *{int(0.15*200/4)}* г белков;
                        \n★ *{int(0.45*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.35 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.5 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.35*200/9)}* г жиров;
                        \n★ *{int(0.15*200/4)}* г белков;
                        \n★ *{int(0.5*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
        elif msg.text == '3 силовые/высокоинтервальные тренировки в неделю 🏋️ 🔥 🏋️':
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round(0.8 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 700
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составляет *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.2*200/9)}* г жиров;
                        \n★ *{int(0.25*200/4)}* г белков;
                        \n★ *{int(0.55*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.2*200/9)}* г жиров;
                        \n★ *{int(0.25*200/4)}* г белков;
                        \n★ *{int(0.55*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round(0.8 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 500
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.4 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.45 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.4*200/9)}* г жиров;
                        \n★ *{int(0.15*200/4)}* г белков;
                        \n★ *{int(0.45*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.2*200/9)}* г жиров;
                        \n★ *{int(0.25*200/4)}* г белков;
                        \n★ *{int(0.55*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
        elif msg.text == 'Более 3-х силовых/высокоинтервальных тренировок в неделю 🤖 👺':
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                # db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # age = int(pretiffy(db_obj.fetchall()))
                # db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                # height = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT bodyfat FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                bodyfat = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    # target_calories = round(0.8 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 1000
                    if target_calories < 1580:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у мужчин равен 1580 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1580
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составляет *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.2*200/9)}* г жиров;
                        \n★ *{int(0.25*200/4)}* г белков;
                        \n★ *{int(0.55*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round(((target_calories / 1000) * 1), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *мужской*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию в соответствующих командах{backslash}. Иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.2*200/9)}* г жиров;
                        \n★ *{int(0.25*200/4)}* г белков;
                        \n★ *{int(0.55*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                elif sex == 'Ж':
                    # target_calories = round(0.8 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age) + 50)
                    LBM = last_weight * (100 - bodyfat) / 100
                    BMR = int(370 + (21.6 * LBM))
                    target_calories = BMR + 650
                    if target_calories < 1150:
                        bot.send_message(msg.chat.id, f'''По формуле расчета у тебя получилось {target_calories} ккал/сутки. 
                        \nНо если брать усредненные данные - минимальный обмен веществ (в покое) у женщин равен 1150 ккал/сутки. Поэтому мой расчет будет исходя из этой калорийности.''')
                        target_calories = 1150
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.4 * target_calories) / 9)
                        protein_nutrient = round((0.15 * target_calories) / 4)
                        carbs_nutrient = round((0.45 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.4*200/9)}* г жиров;
                        \n★ *{int(0.15*200/4)}* г белков;
                        \n★ *{int(0.45*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
                    else:
                        water_quantity = round((target_calories / 1000), 2)
                        fat_nutrient = round((0.2 * target_calories) / 9)
                        protein_nutrient = round((0.25 * target_calories) / 4)
                        carbs_nutrient = round((0.55 * target_calories) / 4)
                        last_weight_str = str(last_weight).replace('.', '\.')
                        water_quantity_str = str(water_quantity).replace('.', '\.')
                        bot.send_message(msg.chat.id, f'''
                        🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Процент подкожного жира {backslash}= *{bodyfat}* *%*{backslash}. Пол {backslash}= *женский*{backslash}.
                        \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                        \nТвой *BMR* {backslash}(Basal Metabolic Rate / Основной обмен веществ в покое{backslash}) {backslash}= *{BMR}* ккал{backslash} в сутки{backslash}.
                        \nЧтобы поддерживать свой текущий вес тебе следует придерживаться следующих ежесуточных пропорций в питании:
                        \n★ *{fat_nutrient}* г жиров;
                        \n★ *{protein_nutrient}* г белков;
                        \n★ *{carbs_nutrient}* г углеводов{backslash}.
                        \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                        \nИтого твой суммарный рацион за день составит *{target_calories}* ккал{backslash}.
                        \nЕсли вес через неделю увеличится или уменьшится {backslash}- измени калорийность в большую или меньшую сторону на *200 ккал*{backslash}, по следующим БЖУ:
                        \n★ *{int(0.2*200/9)}* г жиров;
                        \n★ *{int(0.25*200/4)}* г белков;
                        \n★ *{int(0.55*200/4)}* г углеводов{backslash}.
                        \n{warning}
                        \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                        \nУдачи{backslash}! Все получится ☺️
                        ''', parse_mode="MarkdownV2")
                        send_keyboard(msg)
    except Exception as e:
        bot.send_message(msg.chat.id, '''
        Кажется, мне не достает данных, проверь был ли введен вес, процент подкожного жира и первичные данные, которые вводились на старте 😉
        ''')
        send_keyboard(msg)

def pretiffy(last_val):
    for val in last_val:
        last_v = val[0]
        return last_v

def increase_weight(msg):
    try:
        if msg.text == "Низкая активность 🐌":
            bot.send_message(msg.chat.id, '''
            Я даже боюсь представить, какая у тебя цель набора при малоактивном образе жизни 😱! Но это точно не в рамках моих компетенций 😂
            ''')
            send_keyboard(msg)
        elif msg.text == "Средняя активность 🏄‍♀️🏄‍♂️":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                age = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                height = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    target_calories = round(1.2 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age))
                    water_quantity = round(((target_calories/ 1000) * 1),2)
                    fat_nutrient = round((0.35 * target_calories) / 9)
                    protein_nutrient = round((0.25 * target_calories) / 4)
                    carbs_nutrient = round((0.4 * target_calories) / 4)
                    last_weight_str = str(last_weight).replace('.', '\.')
                    water_quantity_str = str(water_quantity).replace('.', '\.')
                    bot.send_message(msg.chat.id, f'''
                    🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Рост {backslash}= *{height}* cм{backslash}. Возраст {backslash}= *{age}*{backslash}. Пол {backslash}= *мужской*{backslash}.
                    \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                    \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                    \n★ *{fat_nutrient}* г жиров;
                    \n★ *{protein_nutrient}* г белков;
                    \n★ *{carbs_nutrient}* г углеводов{backslash}.
                    \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                    \nИтого твой суммарный рацион за день составит *{target_calories}* калорий{backslash}.
                    \n{warning}
                    \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                    \nУдачи{backslash}! Все получится ☺️
                    ''', parse_mode="MarkdownV2")
                    send_keyboard(msg)
                elif sex == 'Ж':
                    target_calories = round(1.2 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age))
                    water_quantity = round(((target_calories / 1000) * 1), 2)
                    fat_nutrient = round((0.35 * target_calories) / 9)
                    protein_nutrient = round((0.25 * target_calories) / 4)
                    carbs_nutrient = round((0.4 * target_calories) / 4)
                    last_weight_str = str(last_weight).replace('.', '\.')
                    water_quantity_str = str(water_quantity).replace('.', '\.')
                    bot.send_message(msg.chat.id, f'''
                    🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Рост {backslash}= *{height}* cм{backslash}. Возраст {backslash}= *{age}*{backslash}. Пол {backslash}= *женский*{backslash}.
                    \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                    \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                    \n★ *{fat_nutrient}* г жиров;
                    \n★ *{protein_nutrient}* г белков;
                    \n★ *{carbs_nutrient}* г углеводов{backslash}.
                    \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                    \nИтого твой суммарный рацион за день составит *{target_calories}* калорий{backslash}.
                    \n{warning}
                    \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                    \nУдачи{backslash}! Все получится ☺️
                    ''', parse_mode="MarkdownV2")
                    send_keyboard(msg)
        elif msg.text == "Высокая активность 🏋️ 🔥 🏋️":
            with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'''
                SELECT weight
                FROM
                    (
                    SELECT weight, to_date(date, 'DD/MM/YYYY') as date_form
                    FROM bot_users_weights_table
                    WHERE "user_id"={msg.from_user.id}
                    ORDER BY date_form
                    DESC LIMIT 1) 
                    AS last_weight''')
                last_weight = float(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT sex FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                sex = pretiffy(db_obj.fetchall())
                db_obj.execute(f'SELECT age FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                age = int(pretiffy(db_obj.fetchall()))
                db_obj.execute(f'SELECT height FROM bot_users_list WHERE "user_id"={msg.from_user.id} ORDER BY ID DESC LIMIT 1')
                height = int(pretiffy(db_obj.fetchall()))
                postgre_con.commit()
                db_obj.close()
                if sex == 'М':
                    target_calories = round(1.4 * (13.397 * last_weight + 88.362 + 4.799 * height - 5.677 * age))
                    water_quantity = round(((target_calories/ 1000) * 1),2)
                    fat_nutrient = round((0.3 * target_calories) / 9)
                    protein_nutrient = round((0.3 * target_calories) / 4)
                    carbs_nutrient = round((0.4 * target_calories) / 4)
                    last_weight_str = str(last_weight).replace('.', '\.')
                    water_quantity_str = str(water_quantity).replace('.', '\.')
                    bot.send_message(msg.chat.id, f'''
                    🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Рост {backslash}= *{height}* cм{backslash}. Возраст {backslash}= *{age}*{backslash}. Пол {backslash}= *мужской*{backslash}.
                    \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                    \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                    \n★ *{fat_nutrient}* г жиров;
                    \n★ *{protein_nutrient}* г белков;
                    \n★ *{carbs_nutrient}* г углеводов{backslash}.
                    \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                    \nИтого твой суммарный рацион за день составит *{target_calories}* калорий{backslash}.
                    \n{warning}
                    \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                    \nУдачи{backslash}! Все получится ☺️
                    ''', parse_mode="MarkdownV2")
                    send_keyboard(msg)
                elif sex == 'Ж':
                    target_calories = round(1.4 * (9.247 * last_weight + 447.593 + 3.098 * height - 4.33 * age))
                    water_quantity = round(((target_calories / 1000) * 1), 2)
                    fat_nutrient = round((0.3 * target_calories) / 9)
                    protein_nutrient = round((0.3 * target_calories) / 4)
                    carbs_nutrient = round((0.4 * target_calories) / 4)
                    last_weight_str = str(last_weight).replace('.', '\.')
                    water_quantity_str = str(water_quantity).replace('.', '\.')
                    bot.send_message(msg.chat.id, f'''
                    🤔 По моим данным твой текущий и последний записанный вес составляет *{last_weight_str}* кг{backslash}. Рост {backslash}= *{height}* cм{backslash}. Возраст {backslash}= *{age}*{backslash}. Пол {backslash}= *женский*{backslash}.
                    \nЕсли это не так {backslash}- тебе нужно обновить информацию, в соответствующих командах, иначе расчет будет некорректным 😔{backslash}.
                    \nДля достижения цели тебе следует придерживаться следующих ежесуточных пропорций в питании:
                    \n★ *{fat_nutrient}* г жиров;
                    \n★ *{protein_nutrient}* г белков;
                    \n★ *{carbs_nutrient}* г углеводов{backslash}.
                    \n★ А также выпивать не меньше, чем *{water_quantity_str}* л чистой воды{backslash}!
                    \nИтого твой суммарный рацион за день составит *{target_calories}* калорий{backslash}.
                    \n{warning}
                    \nДля подсчета рациона тебе пригодятся соответствующие приложения и необходимо приобрести кухонные весы{backslash}. Подробнее про питание и тренировки узнаешь в *@fit{backslash}_o{backslash}_blog* 😎
                    \nУдачи{backslash}! Все получится ☺️
                    ''', parse_mode="MarkdownV2")
                    send_keyboard(msg)
    except Exception as e:
        bot.send_message(msg.chat.id, '''
        Кажется, мне не достает данных, проверь был ли введен вес и первичные данные, которые вводились на старте 😉
        ''')
        send_keyboard(msg)

def variation(msg):
    # variation_calories = round(200)
    # fat_nutrient = round((0.35 * variation_calories) / 9)
    # protein_nutrient = round((0.25 * variation_calories) / 4)
    # carbs_nutrient = round((0.4 * variation_calories) / 4)
    # fat_nutrient_lc = round((0.3 * variation_calories) / 9)
    # protein_nutrient_lc = round((0.5 * variation_calories) / 4)
    # carbs_nutrient_lc = round((0.2 * variation_calories) / 4)
    bot.send_message(msg.chat.id, f'''
    Каждый из нас индивидуален, поэтому если процесс не идет или идет слишком быстро {backslash}- попробуй изменить рекомендованный рацион на {backslash}+{backslash}- *200* ккал в сутки{backslash}.
    \nМинимально рекомендованная и допустимая калорийность для мужчин составляет *1580* ккал в сутки{backslash}. Для женщин *1150* ккал в сутки{backslash}. Поэтому иногда целесообразнее увеличить активность, чем сократить питание{backslash}.  
    \nУспехов{backslash}! 😎
    ''', parse_mode="MarkdownV2")
    send_keyboard(msg)

def callback_worker(call):
    if call.text == "Хочу сообщить свой вес 😱":
        msg = bot.send_message(call.chat.id, f'''
        \nСупер! Можешь прислать текущий вес или исторический, я все отсортирую 😜
        \nОтправляй в формате "дата вес" разделение = пробел, мне нужно записать это в свой журнал:)
        \nПример формата: dd-mm-yyyy 85.4 
        \nПервая часть = дата (например: 31-12-2021), а вторая = вес (в нашем примере: 85.4)''')
        bot.register_next_step_handler(msg, add_weight)
    elif call.text == "Хочу согнать жирок 🥦":
        try:
            activity_keyboard(call, text = "Хочу согнать жирок 🥦")
        except Exception as e:
            bot.send_message(call.chat.id, 'Кажется, нет данных о твоем весе, необходимо сначала их ввести 😛')
            send_keyboard(call, "Чем еще могу помочь?")
    elif call.text == "Хочу набрать массу 💪":
        try:
            activity_keyboard(call, text = "Хочу набрать массу 💪")
        except Exception as e:
            bot.send_message(call.chat.id, 'Кажется, нет данных о твоем весе, необходимо сначала их ввести 😛')
            send_keyboard(call, "Чем еще могу помочь?")
    elif call.text == "Поддержание текущего веса 🥳":
        try:
            activity_keyboard(call, text = "Поддержание текущего веса 🥳")
        except Exception as e:
            bot.send_message(call.chat.id, 'Кажется, нет данных о твоем весе, необходимо сначала их ввести 😛')
            send_keyboard(call, "Чем еще могу помочь?")
    elif call.text == "Хочу посмотреть статистику веса 😈":
        try:
            weight_statistic(call)
        except Exception as e:
            bot.send_message(call.chat.id, 'Кажется, нет данных о твоем весе, необходимо сначала их ввести 😛')
            send_keyboard(call, "Чем еще могу помочь?")
    elif call.text == "Удалить последнюю запись веса":
        try:
            delete_last(call)
        except:
            bot.send_message(call.chat.id, 'Кажется, нет данных о твоем весе, необходимо сначала их ввести 😛')
            send_keyboard(call, "Чем еще могу помочь?")
    elif call.text == "Удалить все записи веса":
        try:
            delete_all(call)
        except Exception as e:
            bot.send_message(call.chat.id, 'Кажется, нет данных, необходимо сначала их ввести 😛')
            send_keyboard(call, "Чем еще могу помочь?")
    elif call.text == "Не худею/не набираю 👿":
        try:
            variation(call)
        except:
            bot.send_message(call.chat.id, 'Произошла ошибка, повтори команду.')
    elif call.text == "Очистить данные из базы (имя, возраст, пол, рост)":
        try:
            delete_user_info(call)
        except Exception as e:
            bot.send_message(call.chat.id, 'Кажется, нет данных, необходимо сначала их ввести 😛')
            send_keyboard(call, "Чем еще могу помочь?")
    elif call.text == 'Хочу сообщить % подкожного жира 🐻':
        bot.send_photo(call.chat.id, '''https://ie.wampi.ru/2022/01/15/main-qimg-9cc4a7a667ac55c9e4b14155f2cc29e1.png''')
        msg = bot.send_message(call.chat.id, f'''
                \nПосмотри на картинку и на себя - так наиболее точно можно определить процент подкожного жира.
                \nЕсли у тебя есть весы - можешь свериться с их показаниями, но часто они дают погрешность (причем иногда существенную).
                \nПришли мне в чат ответным сообщением процент своего подкожного жира. Пример: 20''')
        bot.register_next_step_handler(msg, add_bodyfat)

def add_weight(msg):
    current_date = msg.text.split()[0]
    current_weight = msg.text.split()[1]
    try:
        float(current_weight)
        current_weight = float(current_weight)
        dt_obj = dt.datetime.strptime(f"{current_date}", "%d-%m-%Y").date()
        with psycopg2.connect(db_URL, sslmode = "require") as postgre_con:
            db_obj = postgre_con.cursor()
            db_obj.execute(
                '''INSERT INTO bot_users_weights_table (user_id, date, weight) 
                VALUES (%s, %s, %s);''', (msg.from_user.id, current_date, current_weight))
            postgre_con.commit()
            db_obj.close()
            bot.send_message(msg.chat.id, 'Зафиксировал!😨 Как когда-то сказал Аристотель: \"Познание всегда начинается с удивления\"..')
            send_keyboard(msg)
    except:
        bot.send_message(msg.chat.id, 'Введен некорректный формат 😟. Попробуй еще раз 😉')
        send_keyboard(msg)

def add_bodyfat(msg):
    try:
        current_bodyfat = msg.text
        current_bodyfat = int(current_bodyfat)
        try:
            with psycopg2.connect(db_URL, sslmode = "require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(f'DELETE FROM bot_users_bodyfat_table WHERE "user_id"={msg.from_user.id}')
                postgre_con.commit()
                db_obj.execute(
                    '''INSERT INTO bot_users_bodyfat_table (user_id, bodyfat)
                    VALUES (%s, %s);''', (msg.from_user.id, current_bodyfat))
                postgre_con.commit()
                db_obj.close()
                bot.send_message(msg.chat.id, 'Записал 😉')
                send_keyboard(msg)
        except:
            with psycopg2.connect(db_URL, sslmode = "require") as postgre_con:
                db_obj = postgre_con.cursor()
                db_obj.execute(
                    '''INSERT INTO bot_users_bodyfat_table (user_id, bodyfat) 
                    VALUES (%s, %s);''', (msg.from_user.id, current_bodyfat))
                postgre_con.commit()
                db_obj.close()
                bot.send_message(msg.chat.id, 'Записал 😉')
                send_keyboard(msg)
    except Exception as e:
        bot.reply_to(msg, 'Что-то не так.. проверь корректность ввода и давай попробуем еще раз 🙏')

def weight_statistic(msg):
    with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
        db_obj = postgre_con.cursor()
        db_obj.execute(f'''SELECT to_date(date, 'DD/MM/YYYY') AS date_column, weight FROM bot_users_weights_table WHERE "user_id"={msg.from_user.id} ORDER BY date_column''')
        date_column = []
        weight_column = []
        c = db_obj.fetchall()
        for val in list(c):
            date_column.append(val[0])
            weight_column.append(val[1])
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(date_column, weight_column, color='darkorchid', marker='*', mec="gold", mew=2, mfc="white",
                 linewidth=2, markersize=20, ls='--')
        rect = fig.patch
        rect.set_facecolor('gold')
        plt.rc('ytick', labelsize=10)
        ax.set_xlabel('дата', weight="bold", size=13)
        plt.rc('xtick', labelsize=10)
        ax.set_ylabel('вес, кг', weight="bold", size=13)
        plt.title("Статистика твоего веса", size=15, weight="bold")
        for index in range(len(date_column)):
            ax.text(date_column[index], weight_column[index], weight_column[index], size=12, weight="bold", horizontalalignment='center')
        user_id = int(msg.chat.id)
        token = "5058162485:AAGSB2FehnhupFU5ViiEwRgypDMJmddcpmg"
        bot_for_plot = TelegramBot(token, user_id)
        bot_for_plot.send_plot(plt)
        bot_for_plot.clean_tmp_dir()
        postgre_con.commit()
        db_obj.close()
        send_keyboard(msg, "Ох! Сначала подумал, что это пример геометрической прогрессии, а оказалось..")

def delete_last(msg):
    with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
        db_obj = postgre_con.cursor()
        db_obj.execute(f'''
        DELETE FROM bot_users_weights_table 
        WHERE id = (SELECT MAX(id) as max_id 
            FROM bot_users_weights_table 
            WHERE user_id = {msg.from_user.id})
        ''')
        postgre_con.commit()
        db_obj.close()
        bot.send_message(msg.chat.id, 'Прошло успешно!')
        send_keyboard(msg, "Чем еще могу помочь?")

def delete_all(msg):
    with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
        db_obj = postgre_con.cursor()
        db_obj.execute(f'DELETE FROM bot_users_weights_table WHERE "user_id"={msg.from_user.id}')
        postgre_con.commit()
        db_obj.close()
        bot.send_message(msg.chat.id, 'И начнем все с чистого листа! 🥂')
        send_keyboard(msg, "Чем еще могу помочь?")

def delete_user_info(msg):
    with psycopg2.connect(db_URL, sslmode="require") as postgre_con:
        db_obj = postgre_con.cursor()
        db_obj.execute(f'DELETE FROM bot_users_list WHERE "user_id"={msg.from_user.id}')
        postgre_con.commit()
        db_obj.close()
        bot.send_message(msg.chat.id, 'Все данные удалены 🥳')
        send_keyboard(msg, "Чем еще могу помочь?")

@bot.message_handler(commands=['help'])
def help(message):
    msg = bot.reply_to(message, "Выбирай интересующий тебя раздел! Если я еще не знаю твой возраст и рост - вызывай команду start 😉")
    send_keyboard(message)

@bot.message_handler(content_types=['text'])
def sorry(message):
    send_keyboard(message, text="Я не понимаю!🌚 Выбери один из пунктов меню:")



bot.infinity_polling()
