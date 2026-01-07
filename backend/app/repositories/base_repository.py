from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, List, Optional, Any

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, id: Any) -> Optional[T]:
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[T]:
        return self.session.query(self.model).all()

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def update(self, id: Any, **kwargs) -> Optional[T]:
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.session.commit()
            self.session.refresh(instance)
        return instance

    def delete(self, id: Any) -> bool:
        instance = self.get_by_id(id)
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        return False
