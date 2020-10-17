import settings


def talk_to_me(update, context):
    print(update.message.chat_id)
    user_text = update.message.text
    update.message.reply_text(user_text)


def send_message_to_user(context):
    message = f'Work - {settings.SUMMARY_WORK_TIME}, rest - {settings.SUMMARY_BREAK_TIME}'
    context.bot.send_message(chat_id=341231444, text=message)
