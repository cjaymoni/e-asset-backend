from fastapi import APIRouter, Depends, Query
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import Union, List
from . import schemas

router = APIRouter()

@router.post('/', description='', status_code=201, name='Permissions')
async def create(payload:int, db:Session=Depends(get_db)):
    return 