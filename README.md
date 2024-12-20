# note-tg-bot

note-tg-bot - это телеграм-бот для создания и управления заметками.

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone git@github.com:greengoblinalex/note-tg-bot.git
    cd note-tg-bot
    ```

2. Создайте и активируйте виртуальное окружение:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

3. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

## Настройка

1. Создайте файл `.env` в корне проекта и добавьте в него следующие переменные:
    ```env
    BOT_TOKEN=your_telegram_bot_token
    DATABASE_URL=your_database_url
    ```

## Запуск

1. Запустите бота:
    ```sh
    python main.py
    ```

## Использование

После запуска бота, вы можете взаимодействовать с ним через Telegram. Используйте команды и кнопки, чтобы создавать и управлять заметками.