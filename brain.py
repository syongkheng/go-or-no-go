import logging
import logging.config

import coin
import config
from user import User

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

x = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    global x
    x = User(update.message.chat.id, update.message.chat.username)
    welcome_text = f"""
        Hello {x.username}!\n\nHaving trouble making decisions?\n\nFlip a coin, or use the result of a game of Rock Paper Scissors, to help you make a decision!\n\nFeel free to play as many times as you would like!
    """
    keyboard = [
        [
            InlineKeyboardButton("Coin flip", callback_data="0"),
            InlineKeyboardButton("Rock Paper Scissors", callback_data="1"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    logger.debug("%s (%s) has started the bot.", x.uid, x.username)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    if query.data == "0":
        logger.debug("%s (%s) has chosen to Flip a Coin!.", x.uid, x.username)
        await coin_flip(update, context)
    elif query.data == "1":
        logger.debug(
            "%s (%s) has chosen to Play a game of Rock Paper Scissors.",
            x.uid,
            x.username,
        )
    elif query.data == "Head" or "Tail":
        await brain_coin_flip(update, context, query.data)
    elif query.data == "Rock":
        logger.debug(
            "Rock Paper Scissors: %s (%s) - Choice: Rock.",
            x.uid,
            x.username,
        )
    elif query.data == "Paper":
        logger.debug(
            "Rock Paper Scissors: %s (%s) - Choice: Paper.",
            x.uid,
            x.username,
        )
    elif query.data == "Scissors":
        logger.debug(
            "Rock Paper Scissors: %s (%s) - Choice: Scissors.",
            x.uid,
            x.username,
        )
    # await query.edit_message_text(text=f"Selected option: {query.data}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


async def coin_flip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """called when user flips a coin"""
    logger.debug("Within coin_flip")
    keyboard = [
        [
            InlineKeyboardButton("Heads", callback_data="Head"),
            InlineKeyboardButton("Tails", callback_data="Tail"),
        ]
    ]
    query = update.callback_query
    # await query.answer()
    # await query.edit_message_text(text="Flipping a coin!")
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "Choose a side of the coin!", reply_markup=reply_markup
    )


async def brain_coin_flip(
    update: Update, context: ContextTypes.DEFAULT_TYPE, choice
) -> None:
    logger.debug(
        "Coin Flip: brain_coin_flip(): %s (%s) - Choice: %s.",
        x.uid,
        x.username,
        choice,
    )
    query = update.callback_query
    c = coin.Coin(x.uid, choice)
    if c.flip():
        await query.edit_message_text(
            f"""The {c.outcome} side is facing you! The number used was {c.program_choice}.\n\nYou can be sure of your decision!\n\n/start to play again!"""
        )
    else:
        await query.edit_message_text(
            f"""The {c.outcome} side is facing you! The number used was {c.program_choice}.\n\nYou should rethink your decision!\n\n/start to play again!"""
        )
    logger.debug("End of game for %s (%s)", x.uid, x.username)


def main() -> None:
    """Run the bot."""
    api_key = config.TELEGRAM_API_KEY
    application = Application.builder().token(api_key).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("simpleExample")
    main()
