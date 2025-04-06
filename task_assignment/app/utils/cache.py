from flask_caching import Cache
from app import Config

# Initialize the Flask-Caching extension with Redis as the backend
cache = Cache(config={
    'CACHE_TYPE': 'redis',                  # Specify Redis as the caching backend
    'CACHE_REDIS_URL': Config.CACHE_REDIS_URL  # Redis connection URL from the app's config
})
