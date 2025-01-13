from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Pydantic модели для сущностей

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False


tasks: List[Task] = [
    Task(id=1, title="Купить молоко", description="Не забудьте 2 бутылки", completed=False),
    Task(id=2, title="Прочитать книгу", completed=True),
]


# Ручки (endpoints)

@app.get("/tasks", response_model=List[Task])
async def list_tasks():
    """Возвращает список всех задач."""
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Возвращает задачу по её ID."""
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: Task):
    """Создаёт новую задачу."""
    for t in tasks:
        if t.id == task.id:
            raise HTTPException(status_code=400, detail="Задача с таким id уже существует")
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    """Обновляет задачу по её ID."""
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """Удаляет задачу по её ID."""
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Задача не найдена")