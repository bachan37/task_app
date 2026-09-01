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

def update_task(
  db: Session, 
  task: models.Task, 
  task_data: schemas.TaskUpdate
):
  update_data = task_data.model_dump(exclude_unset=True)
  
  for key, value in update_data.items():
    setattr(task, key, value)
  
  db.commit()
  db.refresh(task)
  return task

def delete_task(
  db: Session,
  task_id: int
) -> bool:
  task = get_task(db, task_id)
  
  if task is None:
    return false;
  
  db.delete(task)
  db.commit()
  return true
