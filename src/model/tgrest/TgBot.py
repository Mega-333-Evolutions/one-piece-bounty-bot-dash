import time

from telethon.errors import FloodWaitError, RPCError
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

import constants as c
import resources.Environment as Env
from src.model.tgrest.TgRest import TgRest

REQUEST_TIMEOUT_SECONDS = 30
REQUEST_MAX_ATTEMPTS = 3

# Base name/path for the persistent file session. Telethon stores it as SESSION_NAME + ".session"
SESSION_NAME = str(c.DATA_DIR / "tg_rest_bot")


class TgBotRequestException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class TgBot:
    def __init__(self):
        self.api_id = int(Env.TG_API_ID.get())
        self.api_hash = Env.TG_API_HASH.get()
        self.bot_token = Env.TG_REST_BOT_TOKEN.get()
        self.channel_id = self._parse_chat_id(Env.TG_REST_CHANNEL_ID.get())
        self.parse_mode = "html"

    @staticmethod
    def _parse_chat_id(raw_chat_id: str) -> str | int:
        """
        Parse the configured channel identifier. It can either be a public username
        (e.g. "@my_channel") or a numeric chat id, in the same "-100..." format used
        by the Bot API
        :param raw_chat_id: The raw TG_REST_CHANNEL_ID value
        :return: A username string or a numeric chat id
        """

        raw_chat_id = raw_chat_id.strip()
        if raw_chat_id.startswith("@"):
            return raw_chat_id

        return int(raw_chat_id)

    def _get_client(self) -> TelegramClient:
        """
        Build a new, not-yet-connected Telethon client. A persistent session is used so
        that the bot login and entity cache do not have to be rebuilt on every call
        :return: The Telethon client
        """

        session_string = Env.TG_REST_SESSION_STRING.get_or_none()
        if session_string:
            session = StringSession(session_string)
        else:
            c.DATA_DIR.mkdir(parents=True, exist_ok=True)
            session = SESSION_NAME

        return TelegramClient(session, self.api_id, self.api_hash, timeout=REQUEST_TIMEOUT_SECONDS)

    def send_message(self, tg_rest: TgRest) -> None:
        """
        Send a message to a Telegram chat
        :param tg_rest: The Telegram REST API request
        :return:
        """

        text = "<code>" + tg_rest.get_as_json_string() + "</code>"

        last_error: Exception | None = None
        for attempt in range(REQUEST_MAX_ATTEMPTS):
            try:
                with self._get_client().start(bot_token=self.bot_token) as client:
                    try:
                        client.send_message(self.channel_id, text, parse_mode=self.parse_mode)
                    except ValueError:
                        # Entity not cached yet, e.g. the very first message sent from a fresh
                        # session. Warm up the dialog cache once and retry immediately
                        client.get_dialogs()
                        client.send_message(self.channel_id, text, parse_mode=self.parse_mode)

                return
            except FloodWaitError as e:
                last_error = e
                if attempt < REQUEST_MAX_ATTEMPTS - 1 and e.seconds <= REQUEST_TIMEOUT_SECONDS:
                    time.sleep(e.seconds)
                    continue

                raise TgBotRequestException(f"Error: Telegram rate limit, retry in {e.seconds}s")
            except RPCError as e:
                # Request reached Telegram but was rejected, retrying won't change the outcome
                raise TgBotRequestException(f"Error: {e}")
            except Exception as e:
                last_error = e
                if attempt < REQUEST_MAX_ATTEMPTS - 1:
                    time.sleep(1)

        raise TgBotRequestException(f"Failed to connect to Telegram: {last_error}")
