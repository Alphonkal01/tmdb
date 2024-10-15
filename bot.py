import requests
from telegram import InlineQueryResultPhoto
from telegram.ext import Updater, InlineQueryHandler, CallbackContext
from uuid import uuid4
import logging

TMDB_API_KEY = 'YOUR_TMDB_API_KEY'
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_movie_details(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url).json()
    if response['results']:
        return response['results'][0]
    return None

def inline_query(update, context: CallbackContext):
    query = update.inline_query.query
    if query == "":
        return

    movie = get_movie_details(query)

    if movie:
        title = movie['title']
        overview = movie['overview']
        rating = movie['vote_average']
        poster = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
        message = f"*{title}*\nRating: {rating}/10\n\n{overview}"

        results = [
            InlineQueryResultPhoto(
                id=uuid4(),
                title=title,
                description=f"Rating: {rating}/10",
                thumb_url=poster,
                photo_url=poster,
                caption=message,
                parse_mode='Markdown',
            )
        ]
        context.bot.answer_inline_query(update.inline_query.id, results)

def start_bot():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(InlineQueryHandler(inline_query))

    logger.info("Bot is running...")

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    start_bot()
