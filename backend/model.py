"""Data models for the application."""
from typing import Optional, List
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Chat message model."""
    channel: str
    text: Optional[str] = None
    files: Optional[List[str]] = None


class ApplicationState(BaseModel):
    """Application state"""
    chat_history: List[ChatMessage] = []
    parameters: dict[str, str] = {}
    open_files: List[str] = []
