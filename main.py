from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Todo(BaseModel):
    id: int
    task: str
    owner: str

todos: List[Todo] = []

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, owner: Optional[str] = None):
    if owner:
        filtered = [todo for todo in todos if todo.owner == owner]
    else:
        filtered = todos
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": filtered,
        "owner": owner or ""
    })

@app.post("/add")
def add_todo(item: str = Form(...), owner: str = Form(...)):
    todos.append(Todo(id=len(todos) + 1, task=item, owner=owner))
    return RedirectResponse(url=f"/?owner={owner}", status_code=303)

@app.post("/delete")
def delete_todo(task: str = Form(...), owner: str = Form(...)):
    for todo in todos:
        if todo.task == task and todo.owner == owner:
            todos.remove(todo)
            break
    return RedirectResponse(url=f"/?owner={owner}", status_code=303)

@app.post("/change-owner")
def change_owner(owner: str = Form(...)):
    return RedirectResponse(url=f"/?owner={owner}", status_code=303)
