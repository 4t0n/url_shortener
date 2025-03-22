### Project Description::

A test assignment for 5D HUB. This application implements an API for creating short links.

### Stack
* Python 3.12;
* FastAPI;
* Pydantic;
* SQLAlchemy;
* Aiosqlite;
* Alembic;

## Installation and Startup Order

1. **Prepare your environment**
   - Make sure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on Windows.
   - Clone the repository and navigate to the project root directory.
   - Configure Environment Variables in `.env`.

2. **Running the Project using Docker Compose**
   - Open a terminal in the project root directory.
   - Run the following command:
     ```
     docker-compose up --build
     ```

3. **Stopping and Removing Running Containers**
   - Open a terminal in the project root directory.
   - Run the following command:
     ```
     docker-compose down
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
