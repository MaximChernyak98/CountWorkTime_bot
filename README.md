# CountWorkTime_bot
CountWorkTime_bot - это бот для Telegram, который умеет проводить учет рабочего времени

### Установка

1. Клонируйте репозиторий, создайте виртуальное окружение
2. Установите зависимости `pip install -r requirements.txt`
3. Запустите файл 
    ```python copy_cascades.py ``` (windows)
    ```python3 copy_cascades.py ``` (Linux/MacOs):
необходимые для работы бота файлы будут скопированны в папку cascades
4. Создайте файл config.py. В тексте укажите информацию формата:
    ```
    TOKEN = "NUMBER_TELEGRAMBOT_TOKEN"
    CHAT_ID = 0
    SPREAD_SHEET_ID = "NUMBER_GOOGLE_SPREAD_SHEET"
   ```
5. Если будет использоваться сохранение в google-таблицы необходимо:
   * Получите файл с ключами к сервисам Google, назовите файл credentials.json (<https://habr.com/ru/post/483302/>)
   * Положите файл credentials.json в папку с проектом ```\CountWorkTime_bot```
   * Поставьте поле в файле ```settings.py``` ```USE_GOOGLE_SPREADSHEET = True```
6. Запустите файл CountWorkTime_bot.py
7. Бот начинает работу либо по кнопке "Старт", либо при отправке любого сообщения
