from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Temporary storage for todos (in-memory)
todos: List[str] = []

class Todo(BaseModel):
    id: int
    task: str
    owner: str

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.get("/todos/{owner}", response_class=HTMLResponse)
def get_todos_by_owner(request: Request, owner: str):
    owner_todos = [todo for todo in todos if todo.owner == owner]
    return templates.TemplateResponse("todos.html", {
        "request": request,
        "owner": owner,
        "todos": owner_todos,
    })

@app.post("/todos/{owner}")
async def add_todo(owner: str, item: str = Form(...)):
    todo_id = len(todos) + 1
    todos.append(Todo(id=todo_id, task=item, owner=owner))
    return RedirectResponse(url=f"/todos/{owner}", status_code=303)

@app.post("/create-todo")
def create_todo(item: str = Form(...), owner: str = Form(...)):
    todos.append(Todo(id=len(todos) + 1, task=item, owner=owner))
    return RedirectResponse("/", status_code=303)

@app.post("/delete-todo")
def delete_todo(item: str = Form(...)):
    if item in todos:
        todos.remove(item)
    return RedirectResponse("/", status_code=303)

@app.post("/edit-todo")
def edit_todo(old_item: str = Form(...), new_item: str = Form(...)):
    if old_item in todos:
        index = todos.index(old_item)
        todos[index] = new_item
    return RedirectResponse("/", status_code=303)