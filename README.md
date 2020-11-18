# Quiz-Bot
 
Опрос пользователей


Примеры работы:

![alt text](https://dvmn.org/media/filer_public/e9/eb/e9ebd8aa-17dd-4e82-9f00-aad21dc2d16c/examination_tg.gif "Telegram bot")
![alt text](https://dvmn.org/media/filer_public/aa/c8/aac86f90-29b6-44bb-981e-02c8e11e69f7/examination_vk.gif "Vk bot")


[телеграм-бот](https://tlgg.ru/@hlmn_bot)  
[VK-бот](https://vk.com/club197757902)

## Как установить

Переименовать файл  `.env.example` в `.env`.  
Добавить учетный данные в файл `.env`  
* `TELEGRAM_TOKEN`  -   токен вашего бота в Telegram
* `VK_TOKEN` - токен вашего бота в VK
* `LOGGER_TELEGRAM_CHAT_ID` - чат id в который отправлять логи
* `LOGGER_TELEGRAM_TOKEN` - токен бота от имени которого отправляются логи
* `QUIZ_FOLDER` - путь к файлам с векторинами, по умолчанию папка `quizes` в корне проекта
* `REDIS_URL` - ссылка на DB
* `REDIS_PORT` - порт DB
* `REDIS_DB` - название DB
* `REDIS_PASSWORD` - пароль DB

  
Python3 должен быть уже установлен.  
Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

## Как пользоваться
Запуск ботов:
```
python telegram_bot.py
python vk_bot.py
```


## Размещение на Heroku

Создаем [новое](https://dashboard.heroku.com/new-app) приложение.  
Переходим в `Deploy`, подключаем репозиторий github.  
Нажимаем `Deploy Branch`.  
Устанавливаем и авторизовываемся в [heroku-cli](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).  
Прописываем переменные из `.env.example` в `Settings` -> `Config Vars`.  
Подключаем buildpacks через [CLI](https://elements.heroku.com/buildpacks/buyersight/heroku-google-application-credentials-buildpack) или на странице Settings, проверяем чтобы там же был `heroku/python`.  
Запускаем приложение через вкладку Resources или CLI : 

```
heroku ps:scale tg-bot=1 -a Имя_приложения
heroku ps:scale vk-bot=1 -a Имя_приложения
```
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).
