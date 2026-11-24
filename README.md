# Coding Round Service (FastAPI)

## Run

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

The app runs at http://localhost:8000. Interactive docs are at http://localhost:8000/docs.

First-time setup on a new machine:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Layout

| File | Responsibility |
|---|---|
| `app/main.py` | App startup, logging, global error handlers |
| `app/routes.py` | HTTP layer: endpoints only, no business logic |
| `app/service.py` | Business rules |
| `app/repository.py` | In-memory storage (dict + lock) |
| `app/models.py` | Request/response models (Pydantic) |
| `app/exceptions.py` | Business errors mapped to HTTP status codes |
| `app/logging_config.py` | Console logging setup |

Errors always return `{"error": "...", "message": "..."}`:
400 for bad input (including a blank name), 404 for not found, 409 for conflicts, 500 for unexpected errors.

## Try it

### Postman (recommended)

1. In Postman, click **Import** and choose `postman_collection.json`.
2. Start the server, then open the **Coding Round Service** collection.
3. Send **Create item**. It saves the new id into the `itemId` collection variable, so **Get item** fetches that item.
4. The **Errors** folder has one request for each error case. To check them all at once, right-click the collection and choose **Run**.

`baseUrl` (default `http://localhost:8000`) is a collection variable. Change it in the collection's **Variables** tab if you use another port.

### Other options

Open `requests.http` (VS Code REST Client extension), or use curl from Git Bash.
Windows PowerShell 5.1 can mangle JSON that contains spaces when passing it to `curl.exe`.

```bash
curl -X POST http://localhost:8000/api/items -H "Content-Type: application/json" -d '{"name": "Pen", "quantity": 10, "price": 2.5}'
curl http://localhost:8000/api/items/1
```
