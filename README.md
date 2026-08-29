# VK Community Bot

Бот для сообщества ВКонтакте на Python (`vk_api`, Bot Long Poll API).

## Возможности

- Автоответы на входящие сообщения по ключевым словам (`vk_bot/autoresponses.py`).
- Рассылка сообщений всем, кто писал боту, по команде администратора.

## Настройка

### 1. Получить токен сообщества

1. Откройте настройки сообщества → «Работа с API» → «Ключи доступа».
2. Создайте ключ с правами **messages** (управление сообщениями сообщества).
3. Включите Long Poll API: «Работа с API» → «Long Poll API» → «Включить», версия API не ниже 5.103, тип — «Только для сообщений».

### 2. Узнать ID сообщества и ваш ID

- ID сообщества (`VK_GROUP_ID`) — число в настройках сообщества («Управление» → «Информация» → ссылка/ID).
- Ваш ID (`VK_ADMIN_IDS`) — можно найти на странице https://vk.com/id или через https://regvk.com/id/.

### 3. Установить зависимости

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Настроить переменные окружения

Скопируйте `.env.example` в `.env` и заполните значения:

```bash
cp .env.example .env
```

```
VK_TOKEN=токен_сообщества
VK_GROUP_ID=id_сообщества
VK_ADMIN_IDS=ваш_id,id_второго_админа
```

Перед запуском загрузите переменные в окружение (например, через `export $(cat .env | xargs)` в Linux/macOS, либо используйте `python-dotenv`, если добавите его в проект).

### 5. Запустить бота

```bash
python main.py
```

Бот подключится к Long Poll API и начнёт слушать события сообщества. Логи выводятся в консоль.

## Использование

- Любое сообщение, написанное сообществу, получает автоответ на основе ключевых слов из `vk_bot/autoresponses.py`. Если совпадений нет — отправляется ответ по умолчанию.
- Каждый написавший боту пользователь сохраняется в локальную базу `bot.db` (SQLite).
- Администратор (ID из `VK_ADMIN_IDS`) может разослать сообщение всем, кто писал боту, командой:

  ```
  /рассылка Текст сообщения для всех подписчиков
  ```

  Бот отчитается о количестве успешно отправленных и неудачных сообщений.

## Кастомизация автоответов

Отредактируйте словарь `RESPONSES` в `vk_bot/autoresponses.py` — ключ ищется как подстрока в тексте сообщения (без учёта регистра), значение — ответ бота. `DEFAULT_RESPONSE` используется, если ни одно ключевое слово не найдено.

## Развёртывание на VPS (чтобы работал постоянно)

Long Poll не требует публичного домена — подойдёт любой VPS с Ubuntu/Debian. Домашний ПК для круглосуточной работы не годится: как только его выключают, бот останавливается.

### 1. Арендовать VPS

Любой хостинг с Ubuntu 22.04/24.04, минимальная конфигурация (1 CPU, 1 ГБ RAM) достаточна. Например: Timeweb Cloud, REG.RU, Selectel, Beget, Yandex Cloud, Cloud.ru, Hetzner, Contabo и т.п. — выберите удобный по цене и оплате.

### 2. Подключиться и установить зависимости

```bash
ssh root@ваш_ip

apt update && apt install -y python3-venv git
mkdir -p /opt/vk-bot
cd /opt/vk-bot
git clone <ссылка_на_ваш_репозиторий> .
git checkout claude/hello-loapjd

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 3. Создать `.env`

```bash
cat > /opt/vk-bot/.env << 'EOF'
VK_TOKEN=токен_сообщества
VK_GROUP_ID=id_сообщества
VK_ADMIN_IDS=ваш_id
EOF
chmod 600 /opt/vk-bot/.env
```

### 4. Настроить автозапуск через systemd

```bash
cp /opt/vk-bot/deploy/vk-bot.service /etc/systemd/system/vk-bot.service
systemctl daemon-reload
systemctl enable --now vk-bot
```

Проверить, что бот работает:

```bash
systemctl status vk-bot
journalctl -u vk-bot -f
```

Теперь бот запускается автоматически при старте сервера и перезапускается сам при сбое (`Restart=on-failure`). Обновление кода после изменений:

```bash
cd /opt/vk-bot
git pull
.venv/bin/pip install -r requirements.txt
systemctl restart vk-bot
```
