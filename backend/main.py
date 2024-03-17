"""Main file for FastAPI server"""
from pathlib import Path
from typing import List
from fastapi import FastAPI, File, HTTPException, Request, WebSocket
from fastapi.responses import HTMLResponse
from pyaml_env import parse_config
from chat import Chat
from dir_tree import DirItem, DirTree, DirectoryNotFoundException

import model
from static_files import static_file_response
from storage import DirectoryStorage, DirectoryItem, KeyNotExists
from knowledge_base import KnowledgeBaseService


app = FastAPI()
config = parse_config('./config.yaml')
chat = Chat(config.get("workspace"))
chat.load("data/Project.json")
chat.load("data/Angular.json")
chat.load("data/Python.json")
storage = DirectoryStorage(config.get("storage"))
dirTree = DirTree(config.get("workspace"))
kbService = KnowledgeBaseService('data')

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
        state = storage.get("app_storage", model_class=model.ApplicationState) or model.ApplicationState()
        chat.params = state.parameters
        answers = chat.get_answer(question)
        state.chat_history.append(model.ChatMessage(channel="master",  text=question))
        for answer in answers:
            state.chat_history.append(model.ChatMessage(**answer))
            await websocket.send_json(answer)
        state.parameters = chat.params
        storage.put("app_storage", state, file_ext="json")

@app.get("/api/app-state",response_model_exclude_none=True)
async def get_application_state() -> model.ApplicationState:
    """Return application state"""
    state = storage.get("app_storage", model_class=model.ApplicationState) or model.ApplicationState()
    return state

@app.get("/api/dir-tree", response_model=List[DirItem])
async def get_subdirs(path: str):
    try:
        return dirTree.list_items(path)
    except DirectoryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.get("/api/files/{file_path:path}")
async def get_file(file_path: str):
    """Return file content"""
    if file_path.startswith("/"):
        file_path = file_path[1:]
    chat.params['project_name'] = ""
    project_path = chat.get_project_path()
    full_path = Path(f"{project_path}{file_path}")
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return HTMLResponse(content=full_path.read_text(), status_code=200)

@app.get("/api/kb", response_model=List[DirectoryItem])
async def get_knowledge_base_items(path: str):
    try:
        return kbService.list_items(path)
    except DirectoryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@app.get("/api/kb/content")
async def get_knowledge_base_item_content(path: str):
    try:
        return kbService.get_node(path)
    except KeyNotExists as e:
        raise HTTPException(status_code=404, detail=e.message)
    
@app.put("/api/kb/content")
async def put_kowledge_base_item_content(path: str, request: Request):
    try:
        body_bytes = await request.body()
        body_text = body_bytes.decode("utf-8")
        return kbService.put_node(path, body_text)
    except KeyNotExists as e:
        raise HTTPException(status_code=404, detail=e.message)

# Angular static files - it have to be at the end of file
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(_: Request, full_path: str):
    """Catch all for Angular routing"""
    return static_file_response("static/browser", full_path)
