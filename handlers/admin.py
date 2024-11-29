
from main import dp
from aiogram import types
from aiogram import types, F

from aiogram.filters import Command
from aiogram.types import  WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods.send_message import SendMessage

from db import Database

import sys
import pathlib
import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

KEKSIK_TOKEN = os.getenv('KEKSIK_TOKEN')
KEKSIK_ACCOUNT = os.getenv('KEKSIK_ACCOUNT')
KEKSIK_URL = os.getenv('KEKSIK_URL')
ADMIN = int(os.getenv('ADMIN'))


script_dir = pathlib.Path(sys.argv[0]).parent
db_file = script_dir / 'db.sqlite3'

db = Database(db_file=db_file)


@dp.message(Command('add_promo'))
async def add_promo(message: types.Message):
  if message.from_user.id == ADMIN:
    amount = message.text.split(' ')[1].split('\n')[0]
    promo = message.text.split('\n')[1:]

    db.add_product(amount=amount, number=promo)
    await message.answer(f"Промокод на сумму {amount} рублей с номером {promo} добавлен успешно")

@dp.message(Command('del_promo'))
async def add_promo(message: types.Message):
  if message.from_user.id == ADMIN:
    promo = message.text.split(' ')[1]
    db.del_product(number=promo)
    await message.answer(f"Промокод с номером {promo} успешно удален")

@dp.message(F.text == "Проверить платеж")
async def check(message: types.Message):
  payload = {'account': int(KEKSIK_ACCOUNT), "token": KEKSIK_TOKEN, "id": 63}
  res = requests.post("https://tg.keksik.io/api/1.0/donates/get", data=json.dumps(payload)).json()
  if int(res['list'][0]['user'])==int(message.from_user.id) and str(res['list'][0]['status'])!="hidden":

      payload_2 = {'account': int(KEKSIK_ACCOUNT), "token": KEKSIK_TOKEN, "id": int(res['list'][0]['id']), "status": "hidden"}
      res_2 = requests.post("https://tg.keksik.io/api/1.0/donates/change-status", data=json.dumps(payload_2)).json()
      promo_text =str(db.new_buy(amount=int(res['list'][0]['amount'])))
      await message.answer(text="Ваш промокод - " + promo_text)
      if (db.check_remain(int(res['list'][0]['amount']))) <=5:
        await SendMessage(chat_id=ADMIN, text=f"Осталось {(db.check_remain(int(res['list'][0]['amount'])))} промокода(ов) на сумму {res['list'][0]['amount']} рублей!")
  else:
    await message.answer("Платеж не найден")


@dp.message(F.text)
async def admin_menu(message: types.Message):
  builder = InlineKeyboardBuilder()
  kb = [
        [types.KeyboardButton(text="Проверить платеж")],
    ]
  keyboard = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True, resize_keyboard=True)

  builder.row(types.InlineKeyboardButton(
      text="Купить промокод",
      web_app=WebAppInfo(url=KEKSIK_URL)
  ))
  await message.answer(f"Товары: в наличии:\nПромокодов на 7 дней - {(db.check_remain(220))}шт.\nПромокодов на 14 дней - {(db.check_remain(380))}шт.\nПромокодов на 30 дней - {(db.check_remain(760))}шт.\nПромокодов на 60 дней - {(db.check_remain(1300))}шт.\n\nКупить промокод:", reply_markup=builder.as_markup())
  
  await message.answer("После платежа обязательно нажмите кнопку Проверить платеж", reply_markup=keyboard)