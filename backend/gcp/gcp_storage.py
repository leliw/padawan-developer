"""A simple wrapper around Google Cloud Firestore."""

from typing import Generic, Iterator, Type
from google.cloud import firestore
from pydantic import BaseModel, Field

from storage import T, BaseStorage


class Node(BaseModel):
    name: str
    path: str
    is_dir: bool = Field(..., alias="isDir")
    has_children: bool


class Storage(BaseStorage[T], Generic[T]):
    """A simple wrapper around Google Cloud Firestore."""

    def __init__(
        self,
        collection: str,
        clazz: Type[T],
        key_name: str = None,
        project: str = None,
        database: str = None,
    ):
        super().__init__(clazz, key_name)
        self._db = firestore.Client(project=project, database=database)
        self._collection = collection
        self._coll_ref = self._db.collection(self._collection)

    def put(self, key: str, data: T) -> None:
        """Put a document in the collection."""
        self._coll_ref.document(key).set(
            data.model_dump(by_alias=True, exclude_none=True)
        )

    def get(self, full_path: str) -> T:
        """Get a document from the collection."""
        parts = full_path.split("/")
        path = "/".join(parts[:-1])
        name = parts[-1]
        doc = self._get_collection(path).document(name).get()
        return self.clazz.model_validate(doc.to_dict())

    def get_all(self) -> Iterator[T]:
        """Get all documents from the collection."""
        for doc in self._coll_ref.stream():
            yield self.clazz.model_validate(doc.to_dict())

    def keys(self, path: str = None) -> Iterator[str]:
        """Return a list of keys in the collection."""
        coll = self._get_collection(path)
        for doc in coll.stream():
            yield doc.id

    def delete(self, key: str) -> None:
        """Delete a document from the collection."""
        self._coll_ref.document(key).delete()

    def drop(self) -> None:
        """Delete all documents from the collection."""
        for doc in self._coll_ref.stream():
            doc.reference.delete()

    def create_dir(self, path: str, name: str) -> None:
        parent = self._get_collection(path)
        parent.document(name).set({"is_dir": True})

    def _get_collection(self, path) -> firestore.CollectionReference:
        path = self._prepare_path(path)
        if path:
            folder = path.split("/")[-1]
            return self._coll_ref.document(path).collection(folder)
        return self._coll_ref
    
    def _prepare_path(self, path: str) -> str:
        print(path)
        if not path:
            return ""
        if path.startswith("/"):
            path = path[1:]
        parts = path.split("/")
        print(parts)
        ret = ""
        for i, p in enumerate(parts):
            if i == len(parts) - 1:
                ret += f"/{p}"
            else:
                ret += f"/{p}/{p}"
        print(ret[1:] if ret else ret)
        return ret[1:] if ret else ret


    def get_nodes(self, path: str) -> Iterator[Node]:
        parent = self._get_collection(path)
        for k in self.keys(path):
            n = parent.document(k).get(field_paths=["is_dir"]).to_dict()
            print(n)
            yield Node(name=k, path=path, isDir=n.get("is_dir", False), has_children=True)