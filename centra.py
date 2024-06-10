from fastapi.responses import JSONResponse
from jose import jwt
import requests
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users, RefreshToken
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta, date
from jose import jwt, JWTError
from typing import Optional
import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel
import schemas
import crud

from auth import role_access, get_db, get_current_user
from models import Users
from roles_enum import RoleEnum

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

@router.post("/new_wet_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_wet_leaves(wet_leaves: schemas.WetLeavesRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_wet = crud.create_wet_leaves(db=db, wet_leaves=wet_leaves, user=current_user)
    crud.create_centra_notifications(db=db, message=f"New wet leaves added - Wet#{db_wet.id}", id=current_user.centra_unit)
    return JSONResponse(content={"detail": "Wet leaves record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/new_collection", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_collection(collection: schemas.CollectionRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_collection = crud.create_collection(db=db, collection=collection, user=current_user)
    crud.create_centra_notifications(db=db, message=f"New collection added - Collection#{db_collection.id}", id=current_user.centra_unit)
    return JSONResponse(content={"detail": "Collection record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/new_dry_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_dry_leaves(dry_leaves: schemas.DryLeavesRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_dry = crud.create_dry_leaves(db=db, dry_leaves=dry_leaves, user=current_user)
    crud.create_centra_notifications(db=db, message=f"New dry added - Dry#{db_dry.id}", id=current_user.centra_unit)
    return JSONResponse(content={"detail": "Dry leaves record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.post("/new_flour", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_flour(flour: schemas.FlourRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    db_flour = crud.create_flour(db=db, flour=flour, user=current_user)
    crud.create_centra_notifications(db=db, message=f"New flour added - Flour#{db_flour.id}", id=current_user.centra_unit)
    return JSONResponse(content={"detail": "Flour record added successfully"}, status_code=status.HTTP_201_CREATED)

@router.get("/collection", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_collection(db: db_dependecy):
    db_collection = crud.get_collection(db=db)
    return db_collection

@router.get("/wet_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_wet_leaves(db: db_dependecy):
    db_wet_leaves = crud.get_wet_leaves(db=db)
    return db_wet_leaves

@router.get("/dry_leaves", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_dry_leaves(db: db_dependecy):
    db_dry_leaves = crud.get_dry_leaves(db=db)
    return db_dry_leaves

@router.get("/dry_leaves_mobile", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_dry_leaves_mobile(date: date, interval: str, db: db_dependecy):
    db_dry_leaves = crud.get_dry_leaves_mobile(db=db, date_origin=date, interval=interval)
    return db_dry_leaves

@router.get("/flour", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_flour(db: db_dependecy):
    db_flour = crud.get_flour(db=db)
    return db_flour

@router.get("/packages", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_packages(db: db_dependecy):
    db_packages = crud.get_packages(db=db)
    return db_packages

@router.get("/notification", dependencies=[Depends(role_access(RoleEnum.centra))])
def get_packages(db: db_dependecy):
    db_packages = crud.get_centra_notifications(db=db)
    return db_packages

@router.put("/wash_wet_leaves/{id}", dependencies=[Depends(role_access(RoleEnum.centra))])
def wash_wet_leaves(id:int, date:schemas.DatetimeRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    query = crud.wash_wet_leaves(db=db, id=id, date=date)
    crud.create_centra_notifications(db=db, message=f"Washing Wet#{id}", id=current_user.centra_unit)
    return 

@router.put("/dry_wet_leaves/{id}", dependencies=[Depends(role_access(RoleEnum.centra))])
def dry_wet_leaves(id:int, date:schemas.DatetimeRecord, db: db_dependecy, current_user: Users = Depends(get_current_user)):
    query = crud.dry_wet_leaves(db=db, id=id, date=date)
    crud.create_centra_notifications(db=db, message=f"Drying Wet#{id}", id=current_user.centra_unit)
    return

@router.put("/flour_dry_leaves/{id}", dependencies=[Depends(role_access(RoleEnum.centra))])
def flour_dry_leaves(id:int, date:schemas.DatetimeRecord, db: db_dependecy):
    query = crud.flour_dry_leaves(db=db, id=id, date=date)
    crud.create_centra_notifications(db=db, message=f"Flouring Dry#{id}")
    return 

@router.post("/add_package", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_package(record:schemas.PackageCreate, db:db_dependecy, current_user: Users = Depends(get_current_user)):
    query = crud.create_package(db=db, package=record)
    crud.create_centra_notifications(db=db, message=f"New package added - Package#{query.id}", id=current_user.centra_unit)

@router.post("/add_shipping", dependencies=[Depends(role_access(RoleEnum.centra))])
def add_shipping_info(shipping:schemas.ShippingInfoRecord, db:db_dependecy):
    db_shipping = crud.create_shipping(db=db, shipping=shipping)
    for id in shipping.packages:
        crud.update_package_shipping_detail(db=db, id=id, shipping_id=db_shipping.id, )
    crud.create_centra_notifications(db=db, message=f"New shipping added - Shipping#{db_shipping.id}")
