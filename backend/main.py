"""Main file for FastAPI server"""
from pathlib import Path
from typing import Union
from fastapi import FastAPI, HTTPException, Request, WebSocket
from fastapi.responses import HTMLResponse
from pyaml_env import parse_config
from chat import Chat

from static_files import static_file_response
from storage import DirectoryStorage

app = FastAPI()
config = parse_config('./config.yaml')
chat = Chat(config.get("workspace"))
chat.load("data/chat.json")
storage = DirectoryStorage(config.get("storage"))

@app.get("/api/config")
async def read_config():
    """Return config from yaml file"""
    return config

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        question = data.strip('"')
        answers = chat.get_answer(question)
        history = storage.get("chat_history") or []
        history.append({"channel": "master",  "text": question})
        for answer in answers:
            history.append(answer)
            await websocket.send_json(answer)
        storage.put("chat_history", history)

@app.get("/api/history")
async def get_chat_history():
    """Return chat history"""
    history = storage.get("chat_history") or []
    return history

@app.get("/api/files/{file_path:path}")
async def get_file(file_path: str):
    """Return file content"""
    project_path = chat.get_project_path()
    if file_path.endswith(".ts"):
        project_path += "frontend/"
    full_path = Path(f"{project_path}{file_path}")
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return HTMLResponse(content=full_path.read_text(), status_code=200)

# Angular static files - it have to be at the end of file
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(_: Request, full_path: str):
    """Catch all for Angular routing"""
    return static_file_response("static/browser", full_path)
