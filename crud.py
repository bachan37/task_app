from sqlalchemy.orm import Session
import models, schemas
import ipdb

def get_task_by_title(db: Session, title: str):
  return db.query(models.Task).filter(models.Task.title == title).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Task).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
  return db.query(models.Task).filter(models.Task.id == task_id).first()

def create_task(db: Session, task: schemas.TaskCreate):
  db_task = models.Task(**task.model_dump())
  
  db.add(db_task)
  db.commit()
  db.refresh(db_task)
  return db_task
