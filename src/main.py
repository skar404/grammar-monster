import uvloop
from pyrogram import Client, idle, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from settings import settings
from core import log
import monster

uvloop.install()
app = Client(
    "bot",
    api_id=settings.api_id,
    api_hash=settings.api_hash,
    bot_token=settings.token,
    in_memory=settings.is_memory,
)


@app.on_message(filters.command(['start', 'help']))
async def command_pin(client: Client, message: Message):
    await client.send_message(
        message.chat.id,
        "This bot is designed to check for errors in chat messages and provide feedback."
        "It will scan the text for grammatical and spelling mistakes, "
        "as well as offer corrections and suggestions to improve writing style. "
        "\nThe bot will help users enhance the quality of their messages and make them clearer and more professional."
        "\n\nCommands:"
        "\n/del - delete message"
        "\n\nIf you have questions, ideas, want to help, or found a bug/typo, "
        "\nwrite to: @denis_malin"
        f"\n\n**Config info:**"
        f"\n{settings.available_chats=}",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("GitHub", url="https://github.com/skar404/grammar-monster/")]
            ])
    )


@app.on_message(filters.command(['ping']))
async def pong_handler(_client: Client, message: Message):
    chat = message.chat
    log.info('command_pin chat_id=%s name=%s', chat.id, chat.title)
    await message.reply_text('pong')


@app.on_message()
async def monster_handler(client: Client, message: Message):
    chat = message.chat
    if chat.id not in settings.available_chats:
        log.info('monster_handler not available chat id=%s name=%s', chat.id, chat.title)
        return

    monster_request = await monster.check_grammar(message.text)
    if not monster_request:
        return
    log.info('monster_handler reqeust=%s', monster_request)

    await client.send_message(
        settings.tmp_chat,
        f"> {message.text}"
        "\n\n**Monster response:**"
        f"\n{monster_request.message.content}"
    )


@app.on_message(filters.command(['del']) & filters.reply, group=1)
async def del_handler(client: Client, message: Message):
    if message.reply_to_message.from_user.id == client.me.id:
        await message.reply_to_message.delete()
    await message.delete()


async def bot():
    log.info('start app')

    await app.start()
    log.info('start bot')
    await idle()
    await app.stop()
    log.info('stop app')


if __name__ == '__main__':
    app.run(bot())
