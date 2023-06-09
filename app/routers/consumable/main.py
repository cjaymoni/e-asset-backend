from fastapi import APIRouter, Depends, File, UploadFile
from dependencies import get_db, validate_bearer
from routers.activity.crud import add_activity
from cls import ContentQueryChecker
from sqlalchemy.orm import Session
from typing import Union, List
from . import crud, schemas
from utils import r_fields

router = APIRouter()

@router.post('/', response_model=schemas.Consumable, status_code=201, name='Consumable')
async def create(payload=Depends(schemas.CreateConsumable.as_form), image:UploadFile=File(None), db:Session=Depends(get_db)):
    activity = [{'func': add_activity, 'args':('consumable.transfer', {'inventory':'inventory.title', 'inventory_id':'inventory.id', 'datetime':'created'})}]
    return await crud.consumable.create(payload, db, thumbnail=image, activity=activity)

@router.get('/', response_model=schemas.ConsumableList, name='Consumable')
@ContentQueryChecker(crud.consumable.model.c(), None)
async def read(db:Session=Depends(get_db), **params):
    return await crud.consumable.read(params, db)

@router.get('/{id}', response_model=Union[schemas.Consumable, dict], name='Consumable')
async def read_by_id(id:int, fields:List[str]=r_fields(crud.consumable.model), db:Session=Depends(get_db)):
    return await crud.consumable.read_by_id(id, db, fields)

@router.patch('/{id}', response_model=schemas.Consumable, name='Consumable')
async def update(id:int, payload:schemas.UpdateConsumable, db:Session=Depends(get_db)):
    activity = []
    if payload.inventory_id:
        activity.append({'func': add_activity, 'args':('consumable.transfer', {'inventory':'inventory.title', 'inventory_id':'inventory.id', 'datetime':'updated'})})
    return await crud.consumable.update_2(id, payload, db, activity=activity)

@router.delete('/{id}', name='Consumable', status_code=204)
async def delete(id:int, db:Session=Depends(get_db)):
    await crud.consumable.delete(id, db)