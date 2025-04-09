import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ClickUp API sozlamalari
CLICKUP_API_TOKEN = "pk_61768760_T38YCEEX98PBHS0QNTJT6K1YX9VSQ7Q6"
LIST_ID = "901801742315"
CLICKUP_TASK_URL = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"

# Telegram bot token
TELEGRAM_BOT_TOKEN = "7665812070:AAEqtobfCNQEMxuOTEq3gtrP9MlRaEOXdMg"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ClickUp maydonlari ID-lari va bo‘limlar ...
FIELD_IDS = {
    "Email": "07f4dc1d-8b57-44b4-a7ee-874bd827f49b",
    "Murojaat mazmuni": "5fe7feac-af35-4e2a-93c3-9891b16c644f",
    "Telefon": "7cdf9086-a69a-45ca-a927-cf3b5fe4cbdd",
    "Yechim sanasi": "85ec58e1-ad76-4b3e-91f8-d78a472789bf",
    "Bo'lim": "c5bfef2a-204a-4761-b5d9-04423f408861",
    "Dasturning qaysi qismiga oid?": "8c806410-1072-4d25-a7a5-b22e9d08d04e",
    "Hozir qanday ishlayapti?": "daa749d5-8d86-4a75-8f9a-15bddf4ec74f",
    "Qanday bo'lishi kerak?": "58118395-d00e-4f1c-98fd-d0564240eb2d"
}

DEPARTMENTS = {
    "O'quv bo'limi": "82d4b51e-76d7-49c8-abfb-43a8ca0a3fb4",
    "HR bo'limi": "96b12c64-cdc9-4fb3-8c0d-bdeb33af4cdf",
    "Ta'minot bo'limi": "cbddb1d5-385b-41ff-b7c4-5c9c253a35fa",
    "Marketing bo'limi": "17ff4e75-7e1a-49e4-9ef5-b67e07b1e54e",
    "Sotuv bo'limi": "23eae117-7003-42af-ac36-444c8edf58ce",
    "Moliya bo'limi": "02843254-b7d0-4ce0-96e7-be294ebf4594",
    "Xo'jalik bo'limi": "e2797282-24d7-4913-b436-e5b80e60530b",
    "IT bo'limi": "1d830759-dd69-47ba-adb2-5b464fd32a7e",
    "Uslubiy bo'lim": "f05a8737-1c91-4a85-9284-4bc9846817ef",
    "Xavfsizlik": "1f6f8c26-a1e4-4d0b-b4aa-4d7e0727b438",
    "Ma'muriy": "8b586716-9751-42c2-b7cc-adca0c8dfb82"
}

# Foydalanuvchi ma'lumotlarini vaqtincha saqlash
user_data = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Murojatingizni /murojat buyrug‘i orqali qoldiring.")

@bot.message_handler(commands=['murojat'])
def start_request(message):
    bot.send_message(message.chat.id, "🔹 Bo‘limlarga murojaat qilish uchun kerakli ma’lumotlarni kiriting.")
    ask_fullname(message)

def ask_fullname(message):
    msg = bot.send_message(message.chat.id, "👤 Ism va familiyangizni kiriting:")
    bot.register_next_step_handler(msg, save_fullname)

def save_fullname(message):
    user_data[message.chat.id] = {"fullname": message.text}
    ask_email(message)

def ask_email(message):
    msg = bot.send_message(message.chat.id, "📧 Email manzilingizni kiriting:")
    bot.register_next_step_handler(msg, save_email)

def save_email(message):
    user_data[message.chat.id]["email"] = message.text
    ask_request_content(message)

def ask_request_content(message):
    msg = bot.send_message(message.chat.id, "📝 Murojaat mazmunini yozing:")
    bot.register_next_step_handler(msg, save_request_content)

def save_request_content(message):
    user_data[message.chat.id]["request"] = message.text
    ask_phone(message)

def ask_phone(message):
    msg = bot.send_message(message.chat.id, "📞 Telefon raqamingizni kiriting:")
    bot.register_next_step_handler(msg, save_phone)

def save_phone(message):
    user_data[message.chat.id]["phone"] = message.text
    ask_department(message)

def ask_department(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for dep in DEPARTMENTS.keys():
        markup.add(KeyboardButton(dep))
    msg = bot.send_message(message.chat.id, "🏢 Qaysi bo‘limga murojaat qilyapsiz?", reply_markup=markup)
    bot.register_next_step_handler(msg, save_department)

def save_department(message):
    department_name = message.text
    if department_name not in DEPARTMENTS:
        return ask_department(message)
    user_data[message.chat.id]["department"] = {"name": department_name, "id": DEPARTMENTS[department_name]}
    if department_name == "IT bo'limi":
        ask_additional_fields(message)
    else:
        ask_solution_date(message)

def ask_additional_fields(message):
    msg = bot.send_message(message.chat.id, "🔹 Dasturning qaysi qismiga oid?")
    bot.register_next_step_handler(msg, save_additional_field_1)

def save_additional_field_1(message):
    user_data[message.chat.id]["program_part"] = message.text
    msg = bot.send_message(message.chat.id, "🔹 Hozir qanday ishlayapti?")
    bot.register_next_step_handler(msg, save_additional_field_2)

def save_additional_field_2(message):
    user_data[message.chat.id]["current_state"] = message.text
    msg = bot.send_message(message.chat.id, "🔹 Qanday bo'lishi kerak?")
    bot.register_next_step_handler(msg, save_additional_field_3)

def save_additional_field_3(message):
    user_data[message.chat.id]["expected_state"] = message.text
    ask_solution_date(message)

def ask_solution_date(message):
    msg = bot.send_message(message.chat.id, "📅 Yechim sanasini kiriting (YYYY-MM-DD formatida):")
    bot.register_next_step_handler(msg, save_solution_date)

def save_solution_date(message):
    user_data[message.chat.id]["solution_date"] = message.text
    send_to_clickup(message)

def send_to_clickup(message):
    chat_id = message.chat.id
    task_data = {
        "name": user_data[chat_id]["fullname"],
        "description": user_data[chat_id]["request"],
        "custom_fields": [
            {"id": FIELD_IDS["Email"], "value": user_data[chat_id]["email"]},
            {"id": FIELD_IDS["Telefon"], "value": user_data[chat_id]["phone"]},
            {"id": FIELD_IDS["Yechim sanasi"], "value": user_data[chat_id]["solution_date"]},
            {"id": FIELD_IDS["Bo'lim"], "value": user_data[chat_id]["department"]["id"]},
            {"id": FIELD_IDS["Dasturning qaysi qismiga oid?"], "value": user_data[chat_id].get("program_part", "")},
            {"id": FIELD_IDS["Hozir qanday ishlayapti?"], "value": user_data[chat_id].get("current_state", "")},
            {"id": FIELD_IDS["Qanday bo'lishi kerak?"], "value": user_data[chat_id].get("expected_state", "")}
        ]
    }
    requests.post(CLICKUP_TASK_URL, headers={"Authorization": CLICKUP_API_TOKEN}, json=task_data)
    bot.send_message(chat_id, "✅ Murojaatingiz tegishli bo'limga yuborildi!")

bot.polling(none_stop=True)
