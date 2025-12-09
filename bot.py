#!/usr/bin/env python3
# SUB ROSA BOT - СКРЫТЫЙ ТОКЕН ДОСТУПА

import logging
import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes

# Настройка
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Токен берется из настроек BotHost
TOKEN = os.getenv("BOT_TOKEN")

# СКРЫТЫЙ ТОКЕН ДЛЯ QR КОДА
QR_TOKEN = "SR_INVITE_2024"

# Состояния
NICKNAME, AGE, SOURCE, STORY, EXPERIENCE, COMFORT, LEVEL, FREQUENCY, READINESS = range(9)

# Файл
DATA_FILE = "subrosa_apps.json"

# Словари для ответов
EXP_MAP = {
    "exp_yes": "Да, был участником",
    "exp_no": "Нет, первый опыт", 
    "exp_heard": "Слышал, но не участвовал"
}

COM_MAP = {
    "com_trust": "Полностью доверяю",
    "com_questions": "Есть вопросы по безопасности",
    "com_guarantees": "Нужны дополнительные гарантии"
}

LEV_MAP = {
    "lev_beginner": "Начинающий",
    "lev_amateur": "Любитель", 
    "lev_experienced": "Опытный",
    "lev_pro": "Профессионал"
}

FREQ_MAP = {
    "freq_weekly": "Еженедельно",
    "freq_biweekly": "1-2 раза в месяц",
    "freq_monthly": "Раз в месяц",
    "freq_invitation": "По особому приглашению"
}

READY_MAP = {
    "ready_week": "Да, в течение недели",
    "ready_month": "Да, в течение месяца", 
    "ready_looking": "Пока присматриваюсь",
    "ready_conditions": "Зависит от условий"
}

def save_data(data):
    all_data = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
        except:
            pass
    
    all_data.append(data)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

# ========== СТАРТ С ПРОВЕРКОЙ ТОКЕНА ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    
    # Проверяем, есть ли скрытый токен в команде
    if args and args[0] == QR_TOKEN:
        # Токен верный, сразу показываем кнопку анкеты
        keyboard = [[InlineKeyboardButton("▶️ НАЧАТЬ АНКЕТУ", callback_data="begin")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🔓 *Доступ предоставлен*\n\n"
            "QR код активирован.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # Если токена нет или неверный
    await update.message.reply_text(
        "🔒 *Доступ ограничен*\n\n"
        "Требуется активация через QR код.",
        parse_mode='Markdown'
    )

# ========== НАЧАЛО АНКЕТЫ ==========
async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🔒 *Sub Rosa*\n\n"
        "*Ludus clausus, fortuna aperta.*\n"
        "Игра закрыта, удача открыта.\n\n"
        "Фишка выбрала вас.\n"
        "Теперь вы выбираете — готовы ли вы?\n\n"
        "9 вопросов отделяют наблюдателя от участника.",
        parse_mode='Markdown'
    )
    
    await query.message.reply_text(
        "1. *Как вас представить в обществе?*\n"
        "(Имя, псевдоним или как обращаться)",
        parse_mode='Markdown'
    )
    return NICKNAME

# ========== ВОПРОС 1 ==========
async def ask_nickname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nickname"] = update.message.text
    context.user_data["access_token"] = QR_TOKEN  # Сохраняем какой токен использовался
    
    await update.message.reply_text(
        "2. *Ваш возраст?*\n"
        "(Только цифра)",
        parse_mode='Markdown'
    )
    return AGE

# ========== ВОПРОС 2 ==========
async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        age = int(update.message.text)
        if age < 18:
            await update.message.reply_text("❌ Доступ разрешен с 18 лет")
            return ConversationHandler.END
        
        context.user_data["age"] = age
        await update.message.reply_text(
            "3. *Как фишка попала к вам?*\n"
            "(Напишите кратко)",
            parse_mode='Markdown'
        )
        return SOURCE
    except:
        await update.message.reply_text("❌ Введите число")
        return AGE

# ========== ВОПРОС 3 ==========
async def ask_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["source"] = update.message.text
    await update.message.reply_text(
        "4. *Опишите момент получения*\n"
        "(1-2 предложения)",
        parse_mode='Markdown'
    )
    return STORY

# ========== ВОПРОС 4 ==========
async def ask_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["story"] = update.message.text
    
    keyboard = [
        [InlineKeyboardButton("Да, был участником", callback_data="exp_yes")],
        [InlineKeyboardButton("Нет, первый опыт", callback_data="exp_no")],
        [InlineKeyboardButton("Слышал, но не участвовал", callback_data="exp_heard")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "5. *Знакомы с приватными закрытыми встречами?*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return EXPERIENCE

# ========== ВОПРОС 5 ==========
async def ask_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    context.user_data["experience"] = EXP_MAP.get(query.data, "Не указано")
    
    keyboard = [
        [InlineKeyboardButton("Полностью доверяю", callback_data="com_trust")],
        [InlineKeyboardButton("Есть вопросы по безопасности", callback_data="com_questions")],
        [InlineKeyboardButton("Нужны дополнительные гарантии", callback_data="com_guarantees")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "6. *Ваше отношение к конфиденциальности формата?*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return COMFORT

# ========== ВОПРОС 6 ==========
async def ask_comfort(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    context.user_data["comfort"] = COM_MAP.get(query.data, "Не указано")
    
    keyboard = [
        [InlineKeyboardButton("Начинающий (первый раз)", callback_data="lev_beginner")],
        [InlineKeyboardButton("Любитель (играю для удовольствия)", callback_data="lev_amateur")],
        [InlineKeyboardButton("Опытный (понимаю нюансы)", callback_data="lev_experienced")],
        [InlineKeyboardButton("Профессионал (серьёзный подход)", callback_data="lev_pro")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "7. *Уровень подготовки?*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return LEVEL

# ========== ВОПРОС 7 ==========
async def ask_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    context.user_data["level"] = LEV_MAP.get(query.data, "Не указано")
    
    keyboard = [
        [InlineKeyboardButton("Еженедельно", callback_data="freq_weekly")],
        [InlineKeyboardButton("1-2 раза в месяц", callback_data="freq_biweekly")],
        [InlineKeyboardButton("Раз в месяц", callback_data="freq_monthly")],
        [InlineKeyboardButton("По особому приглашению", callback_data="freq_invitation")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "8. *Предпочтительная частота?*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return FREQUENCY

# ========== ВОПРОС 8 ==========
async def ask_frequency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    context.user_data["frequency"] = FREQ_MAP.get(query.data, "Не указано")
    
    keyboard = [
        [InlineKeyboardButton("Да, в течение недели", callback_data="ready_week")],
        [InlineKeyboardButton("Да, в течение месяца", callback_data="ready_month")],
        [InlineKeyboardButton("Пока присматриваюсь", callback_data="ready_looking")],
        [InlineKeyboardButton("Зависит от условий", callback_data="ready_conditions")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "9. *Готовы к участию в ближайшее время?*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return READINESS

# ========== ВОПРОС 9 ==========
async def ask_readiness(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    context.user_data["readiness"] = READY_MAP.get(query.data, "Не указано")
    context.user_data["username"] = f"@{update.effective_user.username}" if update.effective_user.username else "Не указан"
    context.user_data["telegram_name"] = update.effective_user.full_name
    context.user_data["submitted_at"] = datetime.now().isoformat()
    
    # Сохраняем
    save_data(context.user_data.copy())
    
    await query.edit_message_text("✅ *Анкета заполнена*", parse_mode='Markdown')
    
    await query.message.reply_text(
        "🖤 *Заявка принята.*\n\n"
        "Ваши ответы переданы кураторам Sub Rosa.\n"
        "В ближайшие сутки с вами свяжется\n"
        "представитель клуба для финального подтверждения.\n\n"
        "*До связи.*\n"
        "— Команда Sub Rosa",
        parse_mode='Markdown'
    )
    
    print(f"\n✅ QR доступ: {context.user_data.get('nickname')} через {QR_TOKEN}")
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Анкета отменена")
    return ConversationHandler.END

# ========== ЗАПУСК ==========
def main():
    app = Application.builder().token(TOKEN).build()
    
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(begin, pattern="^begin$")],
        states={
            NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_nickname)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            SOURCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_source)],
            STORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_story)],
            EXPERIENCE: [CallbackQueryHandler(ask_experience, pattern="^exp_")],
            COMFORT: [CallbackQueryHandler(ask_comfort, pattern="^com_")],
            LEVEL: [CallbackQueryHandler(ask_level, pattern="^lev_")],
            FREQUENCY: [CallbackQueryHandler(ask_frequency, pattern="^freq_")],
            READINESS: [CallbackQueryHandler(ask_readiness, pattern="^ready_")]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    
    print("=" * 60)
    print("🤖 SUB ROSA BOT - QR ДОСТУП")
    print("=" * 60)
    print(f"\n🔐 Скрытый токен: {QR_TOKEN}")
    print(f"\n🔗 QR ссылка:")
    print(f"   https://t.me/YOUR_BOT_USERNAME?start={QR_TOKEN}")
    print(f"\n📱 Сканирование QR кода откроет анкету")
    print("=" * 60)
    
    app.run_polling()

if __name__ == '__main__':
    main()
