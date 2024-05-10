from time import time
from asyncio import create_task, gather, sleep as asleep
from pyrogram.filters import command, user
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from pyrogram.enums import MessageEntityType
from pyrogram.errors import QueryIdInvalid

from FZBypass import Config, Bypass, BOT_START
from FZBypass.core.bypass_checker import direct_link_checker, is_excep_link
from FZBypass.core.bot_utils import AuthChatsTopics, convert_time, BypassFilter


@Bypass.on_message(command("start"))
async def start_msg(client, message):
    await message.reply(
        f"<b><i>CS Bypass Bot!</i></b>\n\n"
        f"<b>A Powerful Elegant Multi Threaded Bot written in Python... which can Bypass Various Shortener Links, Scrape links, and More ...</b>\n\n"
        f"<b>Bot Started {convert_time(time() - BOT_START)} ago...</b>",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton("🎓 Dev", url="https://t.me/CSAdmin69_bot"),
                ]
            ]
        ),
    )


@Bypass.on_message(BypassFilter & (user(Config.OWNER_ID) | AuthChatsTopics))
async def bypass_check(client, message):
    uid = message.from_user.id
    if (reply_to := message.reply_to_message) and (
        reply_to.text is not None or reply_to.caption is not None
    ):
        txt = reply_to.text or reply_to.caption
        entities = reply_to.entities or reply_to.caption_entities
    elif Config.AUTO_BYPASS or len(message.text.split()) > 1:
        txt = message.text
        entities = message.entities
    else:
        return await message.reply("<i>Link Evu raa pukesh...!</i>")

    wait_msg = await message.reply("<i>Bypassing...</i>")
    start = time()

    link, tlinks, no = "", [], 0
    atasks = []
    for enty in entities:
        if enty.type == MessageEntityType.URL:
            link = txt[enty.offset : (enty.offset + enty.length)]
        elif enty.type == MessageEntityType.TEXT_LINK:
            link = enty.url

        if link:
            no += 1
            tlinks.append(link)
            atasks.append(create_task(direct_link_checker(link)))
            link = ""

    completed_tasks = await gather(*atasks, return_exceptions=True)

    parse_data = ""
    for result, link in zip(completed_tasks, tlinks):
        parse_data += f"━━━━━━━✦✗✦━━━━━━━\n\n"
        parse_data += f"» sᴏᴜʀᴄᴇ ʟɪɴᴋ : {link}\n"
        if isinstance(result, Exception):
            parse_data += f"» ʙʏᴘᴀss ᴇʀʀᴏʀ : {result}\n"
        else:
            parse_data += f"» ʙʏᴘᴀssᴇᴅ ʟɪɴᴋ : {result}\n"

    end = time()

    if parse_data:
        parse_data += f"━━━━━━━✦✗✦━━━━━━━\n\n"
        parse_data += f"🫅 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.username}\n"
        parse_data += f"✨ ɪᴅ : {uid}\n"
        parse_data += f"♻️ ᴛᴏᴛᴀʟ ʟɪɴᴋs : {no}\n"
        parse_data += f"⚡️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : <a href='https://t.me/CSAdmin69_bot'>CS</a>\n"

        await wait_msg.edit(parse_data, disable_web_page_preview=True)
    else:
        await wait_msg.delete()


@Bypass.on_message(command("log") & user(Config.OWNER_ID))
async def send_logs(client, message):
    await message.reply_document("log.txt", quote=True)


@Bypass.on_inline_query()
async def inline_query(client, query):
    answers = []
    string = query.query.lower()
    if string.startswith("!bp "):
        link = string.strip("!bp ")
        start = time()
        try:
            bp_link = await direct_link_checker(link, True)
            end = time()

            if not is_excep_link(link):
                bp_link = (
                    f"┎ <b>Source Link:</b> {link}\n┃\n┖ <b>Bypass Link:</b> {bp_link}"
                )
            answers.append(
                InlineQueryResultArticle(
                    title="✅️ Bypass Link Success !",
                    input_message_content=InputTextMessageContent(
                        f"{bp_link}\n\n✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏\n\n🧭 <b>Took Only <code>{convert_time(end - start)}</code></b>",
                        disable_web_page_preview=True,
                    ),
                    description=f"Bypass via !bp {link}",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Bypass Again",
                                    switch_inline_query_current_chat="!bp ",
                                )
                            ]
                        ]
                    ),
                )
            )
        except Exception as e:
            bp_link = f"<b>Bypass Error:</b> {e}"
            end = time()

            answers.append(
                InlineQueryResultArticle(
                    title="❌️ Bypass Link Error !",
                    input_message_content=InputTextMessageContent(
                        f"┎ <b>Source Link:</b> {link}\n┃\n┖ {bp_link}\n\n✎﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏\n\n🧭 <b>Took Only <code>{convert_time(end - start)}</code></b>",
                        disable_web_page_preview=True,
                    ),
                    description=f"Bypass via !bp {link}",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Bypass Again",
                                    switch_inline_query_current_chat="!bp ",
                                )
                            ]
                        ]
                    ),
                )
            )

    else:
        answers.append(
            InlineQueryResultArticle(
                title="♻️ Bypass Usage: In Line",
                input_message_content=InputTextMessageContent(
                    f"<b><i>CS Bypass Bot!</i></b>\n\n"
                    f"<b>A Powerful Elegant Multi Threaded Bot written in Python... which can Bypass Various Shortener Links, Scrape links, and More ...</b>\n\n"
                    f"<b>Bot Started {convert_time(time() - BOT_START)} ago...</b>",
                    quote=True
                ),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton("🎓 Dev", url="https://t.me/CSAdmin69_bot"),
                        ]
                    ]
                )
            )
        )

    try:
        await query.answer(results=answers, cache_time=0)
    except QueryIdInvalid:
        pass
