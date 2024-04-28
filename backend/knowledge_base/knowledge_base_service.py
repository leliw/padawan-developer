

from knowledge_base.article import Article
from storage.base_storage import BaseStorage


class KnowledgeBaseService:

    def __init__(self, storage: BaseStorage[Article]) -> None:
        self.storage = storage
        
    def create(self, item: Article):
        return self.storage.put(item.title, item)

    def list(self):
        return self.storage.get_all()
    
    def read(self, article_id: str):
        return self.storage.get(article_id)
    
    def update(self, article_id: str, item: Article):
        return self.storage.put(article_id, item)
    
    def delete(self, article_id: str):
        return self.storage.delete(article_id)
    
    def rename(self, old_key: str, new_key: str):
        return self.storage.rename_key(old_key, new_key)