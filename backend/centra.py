from fastapi.responses import JSONResponse
from jose import jwt
import requests
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users, RefreshToken
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel
import schemas
import crud


router = APIRouter(
    prefix="/centra",
    tags=["centra"]
)
SECRET_KEY = '194679e3j938492938382883dej3ioms998323ftu933@jd7233!'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# auth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependecy = Annotated[Session, Depends(get_db)]

logger = logging.getLogger(__name__)

@router.post("/new_wet_leaves")
def add_wet_leaves(wet_leaves: schemas.WetLeavesRecord, db: db_dependecy):
    db_collection = crud.create_wet_leaves(db=db, wet_leaves=wet_leaves)
    db.add(db_collection)
    db.commit()
    db.refresh()

@router.post("/new_dry_leaves")
def add_wet_leaves(dry_leaves: schemas.DryLeavesRecord, db: db_dependecy):
    db_dry = crud.create_dry_leaves(db=db, dry_leaves=dry_leaves)
    db.add(db_dry)
    db.commit()
    db.refresh()

@router.post("/new_flour")
def add_wet_leaves(flour: schemas.FlourRecord, db: db_dependecy):
    db_dry = crud.create_flour(db=db, flour=flour)
    db.add(db_dry)
    db.commit()
    db.refresh()

#TODO: Create function that validates the centra role
def validate_user():
    pass