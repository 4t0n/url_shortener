### Project Description::

A test assignment for 5D HUB. This application implements an API for creating short links.

### Stack
* Python 3.12;
* FastAPI;
* Pydantic;
* SQLAlchemy;
* Aiosqlite;
* Alembic;

### Running on a Local Windows Server::

Create and activate a virtual environment:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Install dependencies from requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Run migrations:

```
alembic upgrade head
```

Start the project:

```
uvicorn main:app
```

Running Tests:

```
pytest
```

## Examples

Here are some example API requests:

-  POST /s-link/ — create a short link key. (Available domains are specified in environment variables.)
-  GET /s-link/{shorten_url_id}/ — retrieve the full URL by its key.

Example POST request:

```
{
  "original_url": "http://127.0.0.1/"
}
```
