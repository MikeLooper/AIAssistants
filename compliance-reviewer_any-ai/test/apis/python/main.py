import logging
import traceback

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel

from config import API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("todo-api")

app = FastAPI(title="Todo API", debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

todos = []
next_id = 1


class TodoItem(BaseModel):
    id: int = 0
    title: str | None = None
    is_complete: bool = False


@app.exception_handler(Exception)
async def handle_error(request: Request, exc: Exception):
    return PlainTextResponse("".join(traceback.format_exception(exc)), status_code=500)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/todos")
def list_todos():
    return todos


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for item in todos:
        if item.id == todo_id:
            return item
    return {"error": "Todo " + str(todo_id) + " not found"}


@app.post("/todos")
def create_todo(item: TodoItem):
    global next_id
    item.title = item.title.strip()
    logger.info("Creating todo: " + item.title)
    item.id = next_id
    next_id += 1
    todos.append(item)
    return item


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, data: TodoItem):
    for item in todos:
        if item.id == todo_id:
            item.title = data.title.strip()
            item.is_complete = data.is_complete
            logger.info("Updated todo " + str(todo_id) + ": " + item.title)
            return item
    return {"error": "Todo " + str(todo_id) + " not found"}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, key: str | None = None):
    logger.info("Delete requested for todo " + str(todo_id) + " with key " + str(key))
    if key != API_KEY:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    for item in todos:
        if item.id == todo_id:
            todos.remove(item)
            return {"deleted": todo_id}
    return {"error": "Todo " + str(todo_id) + " not found"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
