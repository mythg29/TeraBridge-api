import os
import logging
from upstash_redis import Redis

logger = logging.getLogger("terabridge.redis")

# Try loading env in case it is imported standalone
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

UPSTASH_REDIS_REST_URL = os.environ.get("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN")

redis_client = None

if UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN:
    try:
        redis_client = Redis(url=UPSTASH_REDIS_REST_URL, token=UPSTASH_REDIS_REST_TOKEN)
        redis_client.ping()
        logger.info("Successfully connected to Upstash Redis.")
    except Exception as e:
        logger.error("Failed to initialize Upstash Redis: %s", e)
        redis_client = None
else:
    logger.info("Upstash Redis credentials not detected. Caching and Rate Limiting will use local in-memory.")
