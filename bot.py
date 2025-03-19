import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
from aiogram.client.default import DefaultBotProperties
import wikipedia

wikipedia.set_lang('uz')
# Bot token
API_TOKEN = '8001819632:AAHlbN3KaG4sP45gyrZaJ7wxQJpJUbTHHlQ'

# Logging sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher yaratamiz (parse_mode yangicha usulda)
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher(storage=MemoryStorage())

# /start yoki /help komandasi
@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: Message):
    await message.answer("Vikipediya Botiga Xush Kelibsiz!")

# Echo handler — boshqa har qanday matn uchun
@dp.message()
async def send_wiki(message: Message):
    try:
        respond = wikipedia.summary(message.text)
        await message.answer(respond)
    except:
        await message.answer("Bu mavzuga oid maqola topilmadi")


# Asosiy funksiya
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Botni ishga tushirish
if __name__ == "__main__":
    asyncio.run(main())
