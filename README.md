# audio_api
Решение второй тестовой задачи на позицию Junior-разработчика

Использованные технологии:
- Python (FastAPI, SQLAlchemy, pydub)
- PostgreSQL
- Docker

## Описание проекта

Сервис позволяет создавать новых пользователей, генерировать для них уникальный ```id``` и ```token```
и использовать эти данные для загрузки аудиофайла в формате ```*.wav```,
далее сервис конвертирует аудиофайл в формат ```*.mp3```, затем сохраняет файл и информацию о нём в базу данных,
после чего формируется ссылка, по которой можно скачать конвертированный аудиофайл.

**Таблица users**

| column         | type      |
|----------------|-----------|
| id             | integer   |
| token          | UUID      |
| username       | varchar   |

**Таблица audiofiles**

| column         | type      |
|----------------|-----------|
| id             | UUID      |
| audiofile      | varchar   |

### Создание нового пользователя

Для начала работы с сервисом необходимо отправить POST запрос на адрес http://127.0.0.1:8000/user
(Сервис должен быть установлен и запущен. Подробнее в разделе ["Установка и запуск"](https://github.com/AvaNdreyWeb/audio_api/tree/main#установка-и-запуск))

Тело запроса должно содержать JSON вида
```json
{
  "username": "Andrey"
}
```
Примечание: ```username``` может быть не уникальным.

Ответ который вы получите на данный запрос будет иметь вид
```json
{
  "id": 1,
  "token": "26647e56-f093-417f-a4db-26326dc89a55",
}
```
Примечание: эти данные необходимо использовать для загрузки аудиофайла.

### Загрузка аудиофайла

Для загрузки нa аудиофайла в формате ```*.wav``` необходимо отправить POST запрос на адрес http://127.0.0.1:8000/upload

**ВНИМАНИЕ!** поскольку в данном POST запросе мы будем прикреплять файл, то ```Content-Type``` в данном случае будет ```multipart/form-data```.

Тело запроса должно содержать 3 обязательных поля:
- ```user_id``` типа ```integer```
- ```token``` типа ```string```
- ```file``` типа ```string($binary)```
Примечание: ```token``` должен соответствовать пользователю с ```id = user_id```, а аудиофайл должен иметь формат ```*.wav```.

Ответ который вы получите на данный запрос будет иметь вид
```json
{
  "link": "http://127.0.0.1:8000/?id=9ddb0cb6-8495-40f2-9995-51e03d65f819&user=1"
}
```
Примечание: перейдя по данной ссылке вы сможете скачать свой файл в формате ```*.mp3```. 
Query параметр ```id``` содержит уникальный идентификатор конвертированного аудиофайла,
друго Query параметр ```user``` содержит уникальный идентификатор пользователя, который загрузил файл.

## Установка и запуск
Для запуска приложения необходимо скачать и установить Docker. Скачать версию для вашей платформы можно с оффициального сайта https://www.docker.com/.

Необходимо клонировать репозиторий на своё устройство и перейти в директорию проекта
```bash
git clone https://github.com/AvaNdreyWeb/audio_api.git
```
```bash
cd audio_api
```
Затем выполнить команду для сборки и запуска проекта в фоновом режиме
```bash
docker-compose up --build -d
```
Примечание: если после выполнения данной команды сервис оказался недоступен, запустите комманду повторно.

Для начала работы с приложением перейдите по адресу http://127.0.0.1:8000/docs
