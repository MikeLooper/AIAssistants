"""HTTP endpoints for to-do items (FastAPI)."""

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from errors import NotFoundError, ValidationError
from models import TodoItem
from todo_repository import InMemoryTodoRepository
from todo_service import TodoService

app = FastAPI(title="To-do API")
repository = InMemoryTodoRepository()
service = TodoService(repository)


class CreateTodoRequest(BaseModel):
    title: str | None = None
    priority: int = 3


class RenameTodoRequest(BaseModel):
    title: str | None = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/todos")
def list_todos(include_completed: bool = False, min_priority: int | None = None) -> list[TodoItem]:
    return service.list_todos(include_completed, min_priority)


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int) -> TodoItem:
    item = repository.find_by_id(todo_id)
    if item is None:
        raise HTTPException(status_code=404)
    return item


@app.post("/todos", status_code=201)
def create_todo(request: CreateTodoRequest) -> TodoItem:
    try:
        return service.create_todo(request.title, request.priority)
    except ValidationError as ex:
        raise HTTPException(status_code=400, detail=str(ex)) from ex


@app.put("/todos/{todo_id}/complete")
def complete_todo(todo_id: int) -> TodoItem:
    try:
        return service.complete_todo(todo_id)
    except NotFoundError as ex:
        raise HTTPException(status_code=404) from ex


@app.put("/todos/{todo_id}/title")
def rename_todo(todo_id: int, request: RenameTodoRequest) -> TodoItem:
    try:
        return service.rename_todo(todo_id, request.title)
    except ValidationError as ex:
        raise HTTPException(status_code=400, detail=str(ex)) from ex
    except NotFoundError as ex:
        raise HTTPException(status_code=404) from ex


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> Response:
    try:
        service.delete_todo(todo_id)
    except NotFoundError as ex:
        raise HTTPException(status_code=404) from ex
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8010)
