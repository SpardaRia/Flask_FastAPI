from random import choice
from fastapi import FastAPI, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int = Field(default=None)
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=100)
    status: str


tasks = []
for i in range(1, 21):
    task = Task(id=i,
                title=f'Заголовок {i}',
                description='Описание',
                status=f'{choice(["задача", "выполнение", "завершение"])}')
    tasks.append(task)

app = FastAPI()
templates = Jinja2Templates(directory='шаблон')


@app.get('/')
async def root():
    return {'message': 'HW_05'}


@app.get('/tasks/', response_class=HTMLResponse)
async def get_tasks(request: Request):
    return templates.TemplateResponse('main.html', {'request': request, 'tasks': tasks, 'title': 'Tasks'})


@app.get('/tasks/{task_id}', response_model=Task)
async def get_task(task_id: int = Path(..., ge=1, le=len(tasks))):
    for task in tasks:
        if task.id == task_id:
            return task


@app.post('/tasks/', response_model=Task)
async def create_task(new_task: Task):
    new_task.id = len(tasks) + 1
    tasks.append(new_task)
    return new_task


@app.put('/tasks/{task_id}', response_model=Task)
async def update_task(new_task: Task, task_id: int = Path(..., ge=1, le=len(tasks))):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            new_task.id = task_id
            tasks[idx] = new_task
            return new_task


@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int = Path(..., ge=1, le=len(tasks))):
    tasks.pop(task_id - 1)
    return {'message': f'Задача с id {task_id} удалена'}


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)