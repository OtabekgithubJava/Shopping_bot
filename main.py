from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from datetime import datetime

admins = [5091219046]
path = 'data.txt'
cart = {}

async def save_data(name, id, username, now) -> None:
    with open(path, 'a') as file:
        data = await get_data()

        if id not in data.split():
            file.write(f"{name}\t{id}\t{username}\t at {now}\n")

async def get_data():
    with open(path, 'r') as file:
        info = file.read()
        return info


async def start(update: Update, context) -> None:
    name = update.effective_user.full_name
    id = update.effective_user.id
    username = update.effective_user.username
    now = datetime.now().strftime("%c")

    await save_data(name, id, username, now)

    buttons1 = [
        [KeyboardButton("Menu"), KeyboardButton("Cart")],
        [KeyboardButton("Cheque"), KeyboardButton("Contact")]
    ]

    buttons = ReplyKeyboardMarkup(buttons1, resize_keyboard=True)

    await update.message.reply_video(
        video="hello.mp4",
        caption="Tugmachalarni tanlang",
        reply_markup=buttons
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id = update.effective_user.id

    if id not in admins:
        await update.message.reply_text("Siz Admin Emassiz!")
    else:
        data = await get_data()
        await update.message.reply_text(f"Adminlik tekshirildi\n\n{data}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text

    if message == "Contact":
        await update.message.reply_text(
            text="Bu bizi Ultra Pro Max do'konimiz\n"
                 "Nomimiz: SF12"
        )

    elif message == "Cart":
        if not cart:
            await update.message.reply_text("Siz hali hech narsa tanlamadizgfiz")
        else:
            xabar = "Your cart: \n"
            for nom, narx in cart.items():
                xabar += f"Nomi: {nom}\tNarx: ${narx}\n"

            await update.message.reply_text(
                text=xabar
            )
    elif message == "Cheque":
        if not cart:
            await update.message.reply_text("Siz hali hech narsa tanlamadizgfiz")
        else:
            xabar = "Your cart: \n"
            for nom, narx in cart.items():
                xabar += f"Nomi: {nom}\tNarx: ${narx}\n"

            price = 0
            for i in cart.values():
                price += i
            xabar += f"\n\nUmumiy: ${price}"

            await update.message.reply_text(
                text=xabar
            )

    elif message == "Menu":
        text = '''
Apple - 100
Banana - 130
Orange - 123
Strawberry - 383
Grapes - 872
Watermelon - 200
        '''

        buttons = [
            [InlineKeyboardButton("Apple", callback_data="100"), InlineKeyboardButton("Banana", callback_data="130"), InlineKeyboardButton("Orange", callback_data="123")],
            [InlineKeyboardButton("Strawberry", callback_data="383"), InlineKeyboardButton("Grapes", callback_data="872"), InlineKeyboardButton("Watermelon", callback_data="200")]
        ]

        buttons2 = InlineKeyboardMarkup(buttons)

        await update.message.reply_photo(
            photo="fruits.jpg",
            caption=text,
            reply_markup=buttons2
        )
    else:
        await handle_qitmir(update, context)


async def handle_qitmir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_sticker(
        sticker="https://telegrambots.github.io/book/docs/sticker-fred.webp"
    )


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query.data

    if query == "100":
        cart.update({"Apple": 100})
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Apple korzinkaga qo'shildi"
        )

    elif query == "130":
        cart.update({"Banana": 130})
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Banana korzinkaga qo'shildi"
        )
    elif query == "123":
        cart.update({"Orange": 123})
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Orange korzinkaga qo'shildi"
        )
    elif query == "383":
        cart.update({"Strawberry": 383})
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Strawberry korzinkaga qo'shildi"
        )
    elif query == "872":
        cart.update({"Grapes": 872})
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Grapes korzinkaga qo'shildi"
        )
    elif query == "200":
        cart.update({"Watermelon": 200})
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Watermelon korzinkaga qo'shildi"
        )


try:
    app = ApplicationBuilder().token("7648771472:AAF8ROihft03eiZ8h3EjmssLD-_UoPAp_Ig").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))
    app.add_handler(CallbackQueryHandler(handle_query))
    app.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO | filters.AUDIO | filters.VOICE | filters.ANIMATION, handle_qitmir))

except Exception as xato:
    print(f"Xatolik ketti\n\n{xato}")
else:
    print("Bot is running...")
    app.run_polling()