from aiogram import Bot, Dispatcher, types
from random import shuffle
from data.secondary_functions import read_test_file, read_theory_file
from CONSTANTS import *

import json
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "5623811204:AAE01YyB1eviNsIRVJ12qjmLAK7jtXiJJRc"

storage = {}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    _id = message.from_user.id

    if _id not in storage:
        storage[_id] = {
            "curr_task": {
                "is_active": False,
                "task_no": None,
                "task_test_data": None,
                "curr_idx": 0
            }
        }

    tasks_btn = KeyboardButton("4")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).insert(tasks_btn)

    await bot.send_message(_id,
                           "Этот бот предназначен для подготовки к ЕГЭ по русскому языку."
                           "Выберите номер задания."
                           "\n\n"
                           "_P.S. пока что только 4-е задание_",
                           parse_mode="Markdown",
                           reply_markup=markup)


@dp.message_handler(lambda message: message.text in map(str, range(4, 5)))
async def start_task(message: types.Message):
    _id = message.from_user.id

    if message.text == "4":
        storage[_id]["curr_task"]["task_no"] = 4

    test_btn = KeyboardButton("Тест")
    theory_btn = KeyboardButton("Теория")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(test_btn, theory_btn)

    await bot.send_message(_id,
                           "Выберите режим",
                           reply_markup=markup)


@dp.message_handler(lambda message: message.text.lower() == "тест")
async def start_test(message: types.Message):
    _id = message.from_user.id

    if storage[_id]["curr_task"]["task_no"] == 4:
        storage[_id]["curr_task"]["curr_idx"] = 0

        test_data = read_test_file("4")
        shuffle(test_data)

        storage[_id]["curr_task"]["task_test_data"] = test_data
        storage[_id]["curr_task"]["is_active"] = True

        print(test_data)

        await go_on_test(message)


@dp.message_handler(lambda message: message.text.lower() == "меню")
async def start_test(message: types.Message):
    _id = message.from_user.id

    tasks_btn = KeyboardButton("4")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(tasks_btn)

    if storage[_id]["curr_task"]["task_no"] == 4:
        storage[message.from_user.id]["curr_task"]["is_active"] = False

        await bot.send_message(_id,
                               "Меню",
                               reply_markup=markup)


@dp.message_handler(lambda message: storage[message.from_user.id]["curr_task"]["is_active"])
async def go_on_test(message: types.Message):
    _id = message.from_user.id

    if storage[_id]["curr_task"]["task_no"] == 4:
        curr_idx = storage[_id]["curr_task"]["curr_idx"]
        if curr_idx > 0:
            prev_word = storage[_id]["curr_task"]["task_test_data"][curr_idx - 1]

            if set(message.text).intersection(set(VOWElS)) == set(
                    [letter.lower() for letter in prev_word if letter.isupper()][0]
            ):
                await bot.send_message(_id,
                                       "Верно! Идем дальше.")
            else:
                await bot.send_message(_id,
                                       f"Неверно! Правильно - *{prev_word}*",
                                       parse_mode="Markdown")

        current_word = storage[_id]["curr_task"]["task_test_data"][curr_idx]

        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        _curr_word_copy = current_word.lower()
        for letter in current_word.lower():
            if letter not in VOWElS:
                continue

            idx_of_curr_vowel = _curr_word_copy.find(letter)
            markup.row(KeyboardButton(_curr_word_copy[:idx_of_curr_vowel + 1]))

            _curr_word_copy = _curr_word_copy[idx_of_curr_vowel + 1:]

        markup.insert("Меню")

        await bot.send_message(_id,
                               current_word.lower(),
                               reply_markup=markup)

        if storage[_id]["curr_task"]["curr_idx"] + 1 == len(storage[_id]["curr_task"]["task_test_data"]):
            test_data = read_test_file("4")
            shuffle(test_data)
            storage[_id]["curr_task"]["task_test_data"] = test_data
            storage[_id]["curr_task"]["curr_idx"] = 0
        else:
            storage[_id]["curr_task"]["curr_idx"] += 1


@dp.message_handler(lambda message: message.text.lower() == "теория")
async def start_test(message: types.Message):
    _id = message.from_user.id

    tasks_btn = KeyboardButton("4")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(tasks_btn)

    if storage[_id]["curr_task"]["task_no"] == 4:
        await bot.send_message(_id,
                               read_theory_file("4"),
                               parse_mode="Markdown",
                               reply_markup=markup)
