"""Main file for FastAPI server"""

from pathlib import Path
from typing import List
from fastapi import Body, FastAPI, HTTPException, Request, WebSocket
from fastapi.responses import HTMLResponse
from pyaml_env import parse_config
from chat import Chat
from dir_tree import DirItem, DirTree, DirectoryNotFoundException

from gcp.gcp_storage import Storage
from knowledge_base.article import Article
from knowledge_base.knowledge_base_service import KnowledgeBaseService
from static_files import static_file_response
import model
from storage import DirectoryStorage, DirectoryItem, KeyNotExists


app = FastAPI()
config = parse_config("./config.yaml")
chat = Chat(config.get("workspace"))
chat.load("data/Project.json")
chat.load("data/Angular.json")
chat.load("data/Python.json")
storage = DirectoryStorage(config.get("storage"))
dirTree = DirTree(config.get("workspace"))


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
        state = (
            storage.get("app_storage", model_class=model.ApplicationState)
            or model.ApplicationState()
        )
        chat.params = state.parameters
        answers = chat.get_answer(question)
        state.chat_history.append(model.ChatMessage(channel="master", text=question))
        for answer in answers:
            state.chat_history.append(model.ChatMessage(**answer))
            await websocket.send_json(answer)
        state.parameters = chat.params
        storage.put("app_storage", state, file_ext="json")


@app.get("/api/app-state", response_model_exclude_none=True)
async def get_application_state() -> model.ApplicationState:
    """Return application state"""
    state = (
        storage.get("app_storage", model_class=model.ApplicationState)
        or model.ApplicationState()
    )
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
    chat.params["project_name"] = ""
    project_path = chat.get_project_path()
    full_path = Path(f"{project_path}{file_path}")
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return HTMLResponse(content=full_path.read_text(), status_code=200)


knowledge_base_service = KnowledgeBaseService(Storage("knowledge_base", Article, key_name="title"))


@app.get("/api/kb", tags=["knowledge_base"], response_model=List[DirectoryItem])
async def get_knowledge_base_items(path: str):
    try:
        return [
            DirectoryItem(
                name=a.title, path=a.title, isDir=False, isLeaf=True, hasChildren=False
            )
            for a in knowledge_base_service.list()
        ]
    except DirectoryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.get("/api/kb/content", tags=["knowledge_base"])
async def get_knowledge_base_item_content(path: str):
    try:
        return knowledge_base_service.read(path).content
    except KeyNotExists as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.post("/api/knowledge-base/articles", tags=["knowledge_base"])
async def knowledge_base_create(item: Article):
    return knowledge_base_service.create(item)


@app.put("/api/kb/content", tags=["knowledge_base"])
async def put_kowledge_base_item_content(path: str, request: Request):
    try:
        body_bytes = await request.body()
        body_text = body_bytes.decode("utf-8")
        return knowledge_base_service.update(path, Article(title=path, content=body_text))
    except KeyNotExists as e:
        raise HTTPException(status_code=404, detail=e.message)


@app.patch("/api/knowledge-base/articles", tags=["knowledge_base"])
async def knowledge_base_rename(path: str, new_path: str = Body(media_type="text/plain")):
    try:
        return knowledge_base_service.rename(path, new_path)
    except KeyNotExists as e:
        raise HTTPException(status_code=404, detail=e.message)
    

@app.get("/api/knowledge-base/articles")
async def knowledge_base_list():
    return knowledge_base_service.list()


# @app.get("/api/knowledge-base/articles/{article_id}")
# async def knowledge_base_read(article_id: str):
#     return knowledge_base_service.read(article_id)


# @app.put("/api/knowledge-base/articles/{article_id}")
# async def knowledge_base_update(article_id: str, item: Article):
#     return knowledge_base_service.update(article_id, item)


# @app.delete("/api/knowledge-base/articles/{article_id}")
# async def knowledge_base_delete(article_id: str):
#     return knowledge_base_service.delete(article_id)


# Angular static files - it have to be at the end of file
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(_: Request, full_path: str):
    """Catch all for Angular routing"""
    return static_file_response("static/browser", full_path)
