"""
🤖 بوت التداول بالذكاء الاصطناعي - تلغرام
=============================================
المتطلبات:
  pip install python-telegram-bot==20.7
  pip install pandas ta requests

الإعداد:
  1. أنشئ بوت عبر @BotFather في تلغرام
  2. انسخ الـ TOKEN وضعه في BOT_TOKEN أدناه
  3. شغّل: python trading_bot.py
"""

import logging
import random
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

# ============================================================
# ⚙️  الإعدادات - ضع التوكن هنا
# ============================================================
BOT_TOKEN = "8204087269:AAFMdeAj2l1fECqI5icdldw-R9jV9bc9z8Y"

# ============================================================
# 📊 قائمة الأسواق
# ============================================================
MARKETS = {
    # ============ فوركس ============
    "eurusd_otc":  {"name": "EUR/USD (OTC)",  "emoji": "🇪🇺", "cat": "forex"},
    "gbpusd_otc":  {"name": "GBP/USD (OTC)",  "emoji": "🇬🇧", "cat": "forex"},
    "usdjpy_otc":  {"name": "USD/JPY (OTC)",  "emoji": "🇯🇵", "cat": "forex"},
    "usdngn_otc":  {"name": "USD/NGN (OTC)",  "emoji": "🇳🇬", "cat": "forex"},
    "audusd_otc":  {"name": "AUD/USD (OTC)",  "emoji": "🇦🇺", "cat": "forex"},
    "usdcad_otc":  {"name": "USD/CAD (OTC)",  "emoji": "🇨🇦", "cat": "forex"},
    "usdchf_otc":  {"name": "USD/CHF (OTC)",  "emoji": "🇨🇭", "cat": "forex"},
    "nzdusd_otc":  {"name": "NZD/USD (OTC)",  "emoji": "🇳🇿", "cat": "forex"},
    "eurgbp_otc":  {"name": "EUR/GBP (OTC)",  "emoji": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "cat": "forex"},
    "eurjpy_otc":  {"name": "EUR/JPY (OTC)",  "emoji": "🇯🇵", "cat": "forex"},
    "gbpjpy_otc":  {"name": "GBP/JPY (OTC)",  "emoji": "🇬🇧", "cat": "forex"},
    "usdzar_otc":  {"name": "USD/ZAR (OTC)",  "emoji": "🇿🇦", "cat": "forex"},
    "usdmxn_otc":  {"name": "USD/MXN (OTC)",  "emoji": "🇲🇽", "cat": "forex"},
    "usdbrl_otc":  {"name": "USD/BRL (OTC)",  "emoji": "🇧🇷", "cat": "forex"},
    "usdinr_otc":  {"name": "USD/INR (OTC)",  "emoji": "🇮🇳", "cat": "forex"},
    "usdegp_otc":  {"name": "USD/EGP (OTC)",  "emoji": "🇪🇬", "cat": "forex"},
    "usdsar_otc":  {"name": "USD/SAR (OTC)",  "emoji": "🇸🇦", "cat": "forex"},
    "usdaed_otc":  {"name": "USD/AED (OTC)",  "emoji": "🇦🇪", "cat": "forex"},
    # ============ كريبتو ============
    "btcusd":      {"name": "Bitcoin/USD",    "emoji": "⚡",  "cat": "crypto"},
    "ethusd":      {"name": "Ethereum/USD",   "emoji": "💎",  "cat": "crypto"},
    "bnbusd":      {"name": "BNB/USD",        "emoji": "🟡",  "cat": "crypto"},
    "xrpusd":      {"name": "XRP/USD",        "emoji": "🔵",  "cat": "crypto"},
    "solusd":      {"name": "Solana/USD",     "emoji": "🌅",  "cat": "crypto"},
    "adausd":      {"name": "Cardano/USD",    "emoji": "🔷",  "cat": "crypto"},
    "dotusd":      {"name": "Polkadot/USD",   "emoji": "🔴",  "cat": "crypto"},
    "ltcusd":      {"name": "Litecoin/USD",   "emoji": "🥈",  "cat": "crypto"},
    "dogeusd":     {"name": "Dogecoin/USD",   "emoji": "🐕",  "cat": "crypto"},
    "maticusd":    {"name": "MATIC/USD",      "emoji": "🟣",  "cat": "crypto"},
    # ============ سلع ============
    "gold":        {"name": "Gold",           "emoji": "🥇",  "cat": "commodity"},
    "silver":      {"name": "Silver",         "emoji": "⚪",  "cat": "commodity"},
    "oil_brent":   {"name": "Brent Oil",      "emoji": "🛢️",  "cat": "commodity"},
    "oil_wti":     {"name": "WTI Oil",        "emoji": "⛽",  "cat": "commodity"},
    "platinum":    {"name": "Platinum",       "emoji": "🔘",  "cat": "commodity"},
    "palladium":   {"name": "Palladium",      "emoji": "🔲",  "cat": "commodity"},
    "copper":      {"name": "Copper",         "emoji": "🟤",  "cat": "commodity"},
    "natgas":      {"name": "Natural Gas",    "emoji": "🔥",  "cat": "commodity"},
    "wheat":       {"name": "Wheat",          "emoji": "🌾",  "cat": "commodity"},
    "corn":        {"name": "Corn",           "emoji": "🌽",  "cat": "commodity"},
    # ============ أسهم ============
    "aapl":        {"name": "Apple",          "emoji": "🍎",  "cat": "stock"},
    "nflx":        {"name": "Netflix",        "emoji": "🎬",  "cat": "stock"},
    "intc":        {"name": "Intel (OTC)",    "emoji": "💻",  "cat": "stock"},
    "ba":          {"name": "Boeing",         "emoji": "✈️",  "cat": "stock"},
    "mcd":         {"name": "McDonald's",     "emoji": "🍔",  "cat": "stock"},
    "tsla":        {"name": "Tesla",          "emoji": "⚡",  "cat": "stock"},
    "amzn":        {"name": "Amazon",         "emoji": "📦",  "cat": "stock"},
    "googl":       {"name": "Google",         "emoji": "🔍",  "cat": "stock"},
    "msft":        {"name": "Microsoft",      "emoji": "🪟",  "cat": "stock"},
    "meta":        {"name": "Meta",           "emoji": "👤",  "cat": "stock"},
    "nvda":        {"name": "NVIDIA",         "emoji": "🎮",  "cat": "stock"},
    "baba":        {"name": "Alibaba (OTC)",  "emoji": "🛒",  "cat": "stock"},
    "dis":         {"name": "Disney (OTC)",   "emoji": "🏰",  "cat": "stock"},
    "ko":          {"name": "Coca-Cola",      "emoji": "🥤",  "cat": "stock"},
    "jpm":         {"name": "JPMorgan",       "emoji": "🏦",  "cat": "stock"},
    "v":           {"name": "Visa (OTC)",     "emoji": "💳",  "cat": "stock"},
    "uber":        {"name": "Uber",           "emoji": "🚗",  "cat": "stock"},
    "shop":        {"name": "Shopify",        "emoji": "🛍️",  "cat": "stock"},
}

CATEGORIES = {
    "forex":     "💱 فوركس",
    "crypto":    "₿ كريبتو",
    "commodity": "🏅 سلع",
    "stock":     "📈 أسهم",
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================
# 🧠 محرك التحليل (يمكن استبداله بـ API حقيقي)
# ============================================================
def analyze_market(market_id: str) -> dict:
    """
    تحليل فني مبسط للسوق.
    يمكن ربط هذه الدالة بـ API حقيقي مثل:
      - Polygon.io
      - Alpha Vantage
      - Binance API (للكريبتو)
    """
    rsi = random.randint(20, 80)
    macd = round(random.uniform(-0.005, 0.005), 5)
    ma_trend = random.choice(["صاعد", "هابط"])
    bb_status = random.choice(["مشتري", "محايد", "مبيع"])
    stoch = random.randint(10, 90)

    # منطق بسيط لتحديد الاتجاه
    bullish_signals = sum([
        rsi < 50,
        macd > 0,
        ma_trend == "صاعد",
        bb_status == "مشتري",
        stoch < 50,
    ])

    direction = "BUY" if bullish_signals >= 3 else "SELL"
    strength = 55 + bullish_signals * 7 + random.randint(-5, 5)
    strength = max(55, min(95, strength))

    base_price = random.uniform(0.8, 200)
    spread = base_price * 0.003
    if direction == "BUY":
        tp = round(base_price + spread * 2, 5)
        sl = round(base_price - spread, 5)
    else:
        tp = round(base_price - spread * 2, 5)
        sl = round(base_price + spread, 5)

    timeframes = ["1m", "5m", "15m", "30m"]

    # الوقت المتوقع للصفقة بناءً على الإطار الزمني
    durations = {
        "1m":  [30, 60, 90, 120],           # 30ث — 2د
        "5m":  [60, 120, 180, 300],         # 1د — 5د
        "15m": [300, 600, 900],             # 5د — 15د
        "30m": [600, 900, 1200, 1800],      # 10د — 30د
    }
    chosen_tf = random.choice(timeframes)
    duration_sec = random.choice(durations[chosen_tf])

    # تحويل الثواني لنص مقروء
    if duration_sec < 60:
        duration_label = f"{duration_sec} ثانية"
    elif duration_sec < 3600:
        mins = duration_sec // 60
        secs = duration_sec % 60
        duration_label = f"{mins} دقيقة" + (f" و{secs} ثانية" if secs else "")
    else:
        duration_label = f"{duration_sec // 3600} ساعة"

    return {
        "direction":       direction,
        "strength":        strength,
        "rsi":             rsi,
        "macd":            macd,
        "ma_trend":        ma_trend,
        "bb_status":       bb_status,
        "stoch":           stoch,
        "entry":           round(base_price, 5),
        "tp":              tp,
        "sl":              sl,
        "timeframe":       chosen_tf,
        "duration_sec":    duration_sec,
        "duration_label":  duration_label,
        "time":            datetime.now().strftime("%H:%M:%S"),
    }


def format_signal(market_id: str, data: dict, analysis: dict) -> str:
    """تنسيق رسالة الإشارة"""
    direction_ar = "🟢 شراء (BUY)" if analysis["direction"] == "BUY" else "🔴 بيع (SELL)"
    bar = "█" * (analysis["strength"] // 10) + "░" * (10 - analysis["strength"] // 10)

    return f"""
{'='*30}
{data['emoji']} *{data['name']}*
{'='*30}

📌 *الإشارة:* {direction_ar}
💪 *القوة:* {bar} {analysis['strength']}%
⏱ *الإطار الزمني:* {analysis['timeframe']}
⏳ *مدة الصفقة:* {analysis['duration_label']}

📊 *المؤشرات الفنية:*
• RSI: `{analysis['rsi']}` {'(تشبع بيع)' if analysis['rsi'] < 30 else '(تشبع شراء)' if analysis['rsi'] > 70 else '(محايد)'}
• MACD: `{analysis['macd']}` {'↑' if analysis['macd'] > 0 else '↓'}
• MA Trend: {analysis['ma_trend']}
• Bollinger Bands: {analysis['bb_status']}
• Stochastic: `{analysis['stoch']}`

💰 *مستويات التداول:*
🎯 دخول: `{analysis['entry']}`
✅ هدف (TP): `{analysis['tp']}`
🛑 وقف (SL): `{analysis['sl']}`

🕐 {analysis['time']}

⚠️ _هذه إشارة تحليلية للمساعدة فقط._
_التداول ينطوي على مخاطر. لا توجد ضمانات._
""".strip()


# ============================================================
# 🤖 معالجات البوت
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /start"""
    keyboard = []
    row = []
    for cat_id, cat_name in CATEGORIES.items():
        row.append(InlineKeyboardButton(cat_name, callback_data=f"cat_{cat_id}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("📊 عرض جميع الأسواق", callback_data="all_markets")])

    await update.message.reply_text(
        "🤖 *بوت التداول بالذكاء الاصطناعي*\n\n"
        "مرحباً! أنا بوت تحليل الأسواق المالية.\n"
        "اختر فئة السوق الذي تريد تحليله:\n\n"
        "⚠️ _تنبيه: الإشارات للمساعدة فقط وليست ضماناً للربح_",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أزرار الكيبورد"""
    query = update.callback_query
    await query.answer()
    data = query.data

    # عرض فئة معينة
    if data.startswith("cat_"):
        cat = data[4:]
        markets_in_cat = {k: v for k, v in MARKETS.items() if v["cat"] == cat}
        keyboard = []
        for market_id, mdata in markets_in_cat.items():
            keyboard.append([InlineKeyboardButton(
                f"{mdata['emoji']} {mdata['name']}",
                callback_data=f"analyze_{market_id}"
            )])
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_main")])
        await query.edit_message_text(
            f"اختر السوق من فئة *{CATEGORIES[cat]}*:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # عرض جميع الأسواق
    elif data == "all_markets":
        keyboard = []
        for market_id, mdata in MARKETS.items():
            keyboard.append([InlineKeyboardButton(
                f"{mdata['emoji']} {mdata['name']}",
                callback_data=f"analyze_{market_id}"
            )])
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_main")])
        await query.edit_message_text(
            "📊 *جميع الأسواق المتاحة:*\nاختر السوق الذي تريد تحليله:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # تحليل سوق معين
    elif data.startswith("analyze_"):
        market_id = data[8:]
        if market_id not in MARKETS:
            await query.edit_message_text("❌ سوق غير موجود")
            return

        market_data = MARKETS[market_id]
        # رسالة انتظار
        await query.edit_message_text(
            f"⏳ *جاري تحليل {market_data['emoji']} {market_data['name']}...*\n\n"
            "🔄 جلب بيانات السوق...\n"
            "📊 تحليل المؤشرات الفنية...\n"
            "🧠 معالجة الإشارة...",
            parse_mode="Markdown",
        )

        # محاكاة وقت التحليل
        await asyncio.sleep(2)

        analysis = analyze_market(market_id)
        signal_text = format_signal(market_id, market_data, analysis)

        keyboard = [
            [
                InlineKeyboardButton("🔄 تحليل مجدداً", callback_data=f"analyze_{market_id}"),
                InlineKeyboardButton("📋 أسواق أخرى", callback_data="all_markets"),
            ],
            [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_main")],
        ]

        await query.edit_message_text(
            signal_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # رجوع للقائمة الرئيسية
    elif data == "back_main":
        keyboard = []
        row = []
        for cat_id, cat_name in CATEGORIES.items():
            row.append(InlineKeyboardButton(cat_name, callback_data=f"cat_{cat_id}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("📊 عرض جميع الأسواق", callback_data="all_markets")])

        await query.edit_message_text(
            "🤖 *بوت التداول بالذكاء الاصطناعي*\n\n"
            "اختر فئة السوق الذي تريد تحليله:\n\n"
            "⚠️ _تنبيه: الإشارات للمساعدة فقط وليست ضماناً للربح_",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *مساعدة البوت*\n\n"
        "/start - تشغيل البوت\n"
        "/help - عرض المساعدة\n\n"
        "كيفية الاستخدام:\n"
        "1. اضغط /start\n"
        "2. اختر فئة السوق\n"
        "3. اختر السوق المحدد\n"
        "4. انتظر الإشارة والتحليل\n\n"
        "⚠️ *تحذير هام:*\n"
        "هذا البوت أداة تحليل فقط.\n"
        "لا يوجد ضمان للربح في التداول.\n"
        "تداول بمسؤولية وفق قدرتك على تحمل المخاطر.",
        parse_mode="Markdown",
    )


# ============================================================
# 🚀 تشغيل البوت
# ============================================================
def main():
    print("🤖 جاري تشغيل بوت التداول...")
    print("⚠️  تأكد من وضع TOKEN الصحيح في BOT_TOKEN")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("✅ البوت يعمل! اضغط Ctrl+C للإيقاف")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
