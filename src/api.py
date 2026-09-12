from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.core.agent import askAgent
from src.core.event_stream import EventStream
from src.state.thread import Thread

import json
import threading


app = FastAPI()


class Task(BaseModel):
    name: str


class ChatRequest(BaseModel):
    message: str


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


@app.post("/chat/stream")
def chatStream(request: ChatRequest):
    thread = Thread()

    thread.addMessage(
        "user",
        request.message
    )

    eventStream = EventStream()

    def runAgent():
        try:
            askAgent(
                thread,
                eventStream
            )
        finally:
            eventStream.close()

    threadRunner = threading.Thread(
        target=runAgent
    )

    threadRunner.start()

    def generateEvents():
        while True:

            event = eventStream.getNext()

            if event is None:
                break

            yield f"data: {json.dumps(event.toDict())}\n\n"

        threadRunner.join()

    return StreamingResponse(
        generateEvents(),
        media_type="text/event-stream"
    )