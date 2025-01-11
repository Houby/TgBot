from aiogram import types


main_kb = types.ReplyKeyboardMarkup(keyboard=[
            [types.KeyboardButton(text="📅 Binance Today", callback_data="BToday"),
             types.KeyboardButton(text="🗓 Binance Month", callback_data="BMonth"),
             types.KeyboardButton(text="📜 Binance Year", callback_data="BYear")
             ]
        ], resize_keyboard=True)
