from sqlalchemy import String, Integer, JSON, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

from Controller.core.config import config

engine = create_engine(config.db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    file_path: Mapped[str] = mapped_column(String, index=True)
    frameRange: Mapped[tuple[int, int]] = mapped_column(JSON)
    bookMark: Mapped[int] = mapped_column(Integer)
    frames: Mapped[list["Frames"]] = relationship("Frames", back_populates="project")

class Frames(Base):
    __tablename__ = "frames"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(Integer)
    project_id: Mapped[Project] = mapped_column(ForeignKey("project.id",ondelete="CASCADE"))
    project: Mapped["Project"] = relationship("Project", back_populates="frames")

class Worker(Base):
    __tablename__ = "worker"

    id:Mapped[int] = mapped_column(primary_key=True,index=True)
    email:Mapped[String] = mapped_column(String,unique=True,index=True)