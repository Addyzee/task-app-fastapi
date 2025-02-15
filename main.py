from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Union, Dict
from uuid import UUID, uuid4

app = FastAPI()

class Task(BaseModel):
    id: Union[UUID, None] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    
tasks : List[Task] = []
@app.get("/tasks/",response_model=List[Task])
async def read_tasks():
    return tasks


@app.post("/tasks/",response_model=Task)
async def create_task(task: Task):
    task.id = uuid4()
    tasks.append(task)
    return task

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(new_task: Task):
    for idx, task in enumerate(tasks):
        if task.id == new_task.id:
            updated_task = task.model_copy(update=new_task.model_dump(exclude_unset=True))
            tasks[idx] = updated_task
            return tasks[idx]
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: UUID):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(idx)
    raise HTTPException(status_code=404, detail="Task not found")


