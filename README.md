# Devman Review Bot

Бот для отслеживания статуса проверки работ на платформе [Devman](https://dvmn.org/) с уведомлениями в Telegram.

## Функционал

- Получение статуса проверки работ через long-polling API Devman
- Отправка уведомлений в Telegram-чат при изменении статуса

## Требования

- Python 3.12
- Учетные записи:
  - Devman (dvmn.org) - для получения API-токена
  - Telegram - для создания бота и получения chat_id

- [Linux](https://www.linux.org/pages/download/) или [WSL](https://learn.microsoft.com/ru-ru/windows/wsl/install) (Ctrl+C для ручного прерывания Long Polling на Windows багуется)


## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/[user_name]/[project_name].git
```
2. Установите зависимости
```bash
pip install -r requirements.txt
```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в папке проекта и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 3 переменные:
 - `AUTH_TOKEN` — токен Devman API, получаемый на вашей странице dvmn.org в разделе API
 - `TG_BOT_TOKEN` — токен Telegram-бота, создайте бота через `@BotFather` в Telegram и узнайте у него токен бота командой `/token`
 - `TG_CHAT_ID` — ID чата, в который будут отправлены сообщения, узнайте через `@userinfobot`


## Запуск
```bash
python devmanapi.py
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
