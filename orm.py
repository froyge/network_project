from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DB_FILENAME


engine = create_engine(f'sqlite:///{DB_FILENAME}', echo=True)
Base = declarative_base()

map_priority = {
    0: "Зеленый", 
    1: "Желтый",
    2: "Красный"
}

class Task(Base):
    __tablename__ = "tasks"
    id_ = Column(Integer, primary_key=True)
    date = Column(Date)
    task = Column(String)
    priority = Column(Integer)


    def __repr__(self):
        return f"Когда: {self.date}\nЧе делаем: {self.task}\nПриоритет: {map_priority[self.priority]}"


class MediaIds(Base):
    __tablename__ = 'Media ids'
    id = Column(Integer, primary_key=True)
    file_id = Column(String(255))
    filename = Column(String(255))


Base.metadata.create_all(engine)