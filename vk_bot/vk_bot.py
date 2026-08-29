import logging
import random
import time

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from . import config, database
from .autoresponses import ADMIN_PHONES, find_response

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("vk_bot")

BROADCAST_COMMAND = "/рассылка"


class Bot:
    def __init__(self):
        if not config.VK_TOKEN:
            raise RuntimeError("VK_TOKEN is not set")
        if not config.GROUP_ID:
            raise RuntimeError("VK_GROUP_ID is not set")

        self.vk_session = vk_api.VkApi(token=config.VK_TOKEN)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, group_id=config.GROUP_ID)
        database.init_db()

    def run(self):
        log.info("Bot started, listening for events...")
        for event in self.longpoll.listen():
            try:
                self._handle_event(event)
            except Exception:
                log.exception("Error while handling event")

    def _handle_event(self, event):
        if event.type != VkBotEventType.MESSAGE_NEW:
            return

        message = event.obj.message
        user_id = message["from_id"]
        text = message.get("text", "")

        is_first_message = database.remember_user(user_id)

        if text.strip().lower().startswith(BROADCAST_COMMAND):
            self._handle_broadcast(user_id, text)
            return

        reply = find_response(text)
        if is_first_message:
            reply = f"{reply}\n\nНомера администрации для связи: {ADMIN_PHONES}"
        self.send_message(user_id, reply)

    def _handle_broadcast(self, user_id: int, text: str):
        if user_id not in config.ADMIN_IDS:
            self.send_message(user_id, "У вас нет прав для рассылки.")
            return

        payload = text[len(BROADCAST_COMMAND):].strip()
        if not payload:
            self.send_message(user_id, "Использование: /рассылка <текст сообщения>")
            return

        subscribers = [uid for uid in database.all_subscribers() if uid != user_id]
        self.send_message(user_id, f"Начинаю рассылку для {len(subscribers)} получателей...")

        sent, failed = 0, 0
        for subscriber_id in subscribers:
            try:
                self.send_message(subscriber_id, payload)
                sent += 1
            except Exception:
                log.exception("Failed to send broadcast message to %s", subscriber_id)
                failed += 1
            time.sleep(config.BROADCAST_DELAY_SECONDS)

        self.send_message(user_id, f"Рассылка завершена: отправлено {sent}, ошибок {failed}.")

    def send_message(self, user_id: int, text: str):
        self.vk.messages.send(
            user_id=user_id,
            message=text,
            random_id=random.randint(1, 2**31 - 1),
        )


def main():
    Bot().run()


if __name__ == "__main__":
    main()
