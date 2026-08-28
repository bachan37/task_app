from fastapi import FastAPI, Depends, status, HTTPException
import ipdb
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

@app.post("/tasks/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
  db_task = crud.get_task_by_title(db=db, title=task.title)

  if db_task is not None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="A task with this title already exists."
    )

  return crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=List[schemas.TaskResponse], status_code=status.HTTP_200_OK)
async def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return crud.get_tasks(db=db, skip=skip, limit=limit)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, status_code=status.HTTP_200_OK)
async def read_task(task_id: int, db: Session = Depends(get_db)):
  db_task = crud.get_task(db=db, task_id=task_id)

  if db_task is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail="Task not found"
    )

  return db_task

