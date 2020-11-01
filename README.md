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
    SPREAD_SHEET_ID = "NUMBER_GOOGLE_SPREAD_SHEET" # если будет использоваться google-spreadsheets
   ```
5. Запустите файл CountWorkTime_bot.py
6. Бот начинает работу либо по кнопке "Старт", либо при отправке любого сообщения
  
### Добавление сохранения результатов в Google-spreadsheets   
Если будет использоваться сохранение в google-таблицы необходимо:
1. Получите файл с ключами к сервисам Google, назовите файл credentials.json (<https://habr.com/ru/post/483302/>)
2. Положите файл credentials.json в папку с проектом ```\CountWorkTime_bot```
3. Поставьте поле в файле ```settings.py``` ```USE_GOOGLE_SPREADSHEET = True```

### Добавление автозапуска бота при старте (Windows)
1. Создайте файл с расширением *.bat 
2. В тексте файла необходимо указать следуйщий текст (первая часть - путь к интерпретатору, вторая часть - путь к скрипту):
    ```C:\_путь к папке проекта_\env\Scripts\python C:\_путь к папке проекта_\CountWorkTime_bot\CountWorkTime_bot.py```
3. Далее по инструкции <https://www.computerhope.com/issues/ch000322.htm>

### Добавление автозапуска бота при старте (Linux)
1. Создайте файл /lib/systemd/system/_имя_сервиса_.service
2. В тексте файла укажите:
    ```
    [Unit]
    Description=**название**
    After=multi-user.target
    
    [Service]
    Type=idle
    ExecStart=**путь_к_интерпретатору_env** **путь_к_файлу_скрипта**
    
    [Install]
    WantedBy=multi-user.target
    ```
3. Дайте разрешение файлу-сервиса
    ```sudo chmod 644 /lib/systemd/system/**имя_сервиса**.service```
4. Запустите сервис:
   ```
   sudo systemctl daemon-reload
   sudo systemctl enable **имя_сервиса**.service
   sudo reboot
   ```
5. Для работы с сервисом:
   ```
   sudo systemctl enable **имя_сервиса**.service  - разрешить выполнение
   sudo systemctl start **имя_сервиса**.service  - запустить
   sudo systemctl status **имя_сервиса**.service  - статус
   sudo systemctl stop **имя_сервиса**.service  - остановить
   sudo systemctl disable **имя_сервиса**.service  - запретить выполнение
   ```