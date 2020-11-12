from telegram.ext import (
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
    CommandHandler
)

from interaction.rest_handlers import (
    count_rest_part,
    full_rest,
    part_rest
)


from interaction.handlers import rest_message, print_rest_fallback, set_pomadoro_timer, print_pomodoro_fallback
from interaction.rest_handlers import count_rest_part
from interaction.dialogues import send_pomodoro_message

rest_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(rest_message, pattern='^(rest|work|dinner)$')],
    states={'wait_answer': [CallbackQueryHandler(full_rest, pattern='full_rest'),
                            CallbackQueryHandler(part_rest, pattern='partial_rest')],
            'get_percent': [MessageHandler(Filters.regex('^\d+$'), count_rest_part)]
            },
    fallbacks=[MessageHandler(Filters.all, print_rest_fallback)]
)


set_pomadoro_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^(Поставить Pomodoro)$'), send_pomodoro_message)],
    states={'get_pomadoro_time': [MessageHandler(Filters.regex('^\d+$'), set_pomadoro_timer)]},
    fallbacks=[MessageHandler(Filters.all, print_pomodoro_fallback)]
)