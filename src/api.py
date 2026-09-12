from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    name: str

@app.get("/")
def home():
    return {"message": "HyperCloudAI API is running"}

@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            "Learn Python",
            "Build an API",
            "Learn FastAPI"
        ]
    }

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id != 1:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": 1,
        "name": "Learn FastAPI"
    }

@app.post("/tasks")
def create_task(task: Task):
    return {
        "message": "Task created",
        "task": task.name
    }

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return {
        "message": "Task deleted",
        "task_id": task_id
    }