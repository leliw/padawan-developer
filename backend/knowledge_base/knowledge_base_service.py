

from knowledge_base.article import Article
from storage.base_storage import BaseStorage



class KnowledgeBaseService:

    def __init__(self, storage: BaseStorage[Article]) -> None:
        self.storage = storage
        
    def create(self, item: Article):
        return self.storage.put(item.title, item)

    def create_folder(self, path: str, name: str):
        return self.storage.create_folder(path, name)
    
    def list(self, path: str):
        return self.storage.get_nodes(path)
    
    def read(self, full_path: str):
        return self.storage.get(full_path)
    
    def update(self, article_id: str, item: Article):
        return self.storage.put(article_id, item)
    
    def delete(self, article_id: str):
        return self.storage.delete(article_id)
    
    def rename(self, old_key: str, new_key: str):
        return self.storage.rename_key(old_key, new_key)