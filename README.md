### Описание проекта:

Тестовое задание для 5D HUB
Данное приложение реализует API для создания коротких ссылок.

### Stack
* Python 3.12;
* FastAPI;
* Pydantic;
* SQLAlchemy;
* Aiosqlite;
* Alembic;

### Для запуска на локальном сервере Windows:

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
alembic upgrade head
```

Запустить проект:

```
uvicorn main:app
```

Для запуска тестов:

```
pytest
```

## Примеры

Вот несколько примеров запросов к API:

-  POST /s-link/ — создать ключ для ссылки. (Доступные домены указываются в переменных окружения.)
-  GET /s-link/{shorten_url_id}/ — получить получить полную ссылку по ключу.

Пример POST запроса:

```
{
  "original_url": "http://127.0.0.1/"
}
```
