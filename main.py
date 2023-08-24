import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from pyngrok import ngrok
from vocode.streaming.telephony.config_manager.redis_config_manager import (
    RedisConfigManager,
)
from src import telephony
from src.loggers import stream_logger


# --- Configuration

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

# --- Logging

logger = stream_logger("app")


# --- Application

app = FastAPI(docs_url=None)
config_manager = RedisConfigManager()


# --- Set up ngrok tunnel unless routing is handled another way
if not BASE_URL:
    ngrok_auth = os.environ.get("NGROK_AUTH_TOKEN")
    if ngrok_auth is not None:
        ngrok.set_auth_token(ngrok_auth)

    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 3000

    # Open a ngrok tunnel to the dev server
    # TODO configure this to be stable to a predefined ngrok domain
    BASE_URL = ngrok.connect(addr=port).public_url.replace("https://", "")
    logger.info('ngrok tunnel "{}" -> "http://127.0.0.1:{}"'.format(BASE_URL, port))

if not BASE_URL:
    raise ValueError("BASE_URL must be set in environment if not using pyngrok")

# --- Telephony server - this encompasses the application, all behavioral logic is configured on this server

telephony_server = telephony.server(
    base_url=BASE_URL,
    config_manager=config_manager,
    logger=logger,
)

# --- Launch application with telephony server

app.include_router(telephony_server.get_router())
