from fastapi.responses import FileResponse
from dependencies import validate_bearer
from fastapi import APIRouter, Request
from config import LOG_ROOT
from pathlib import Path
from typing import List
import os, xattr

router = APIRouter()

@router.get('/', description='Read logs')
@router.get('/download', description='Read logs')
async def read(request:Request, file:Path=None, offset:int=0, limit:int=20):

    if file:
        file_path = os.path.join(LOG_ROOT, file)
        if os.path.isfile(file_path):
            if request.url.path=='/logs/download':
                return FileResponse(file_path, media_type='text/plain')
            return FileResponse(file_path, media_type='text/plain', stat_result=os.stat(file_path))
        else:
            return "error", {"info":f"File not found"}  
    
    log_files = list(Path(LOG_ROOT).iterdir())

    files = [
        {
            "filename": file.name, "path": file.as_posix(),
            "entries": {k:v for k,v in xattr.xattr( file.__str__() ).items() if k.lower() in ['debug','info','warning','critical','error']}
        }
        for file in log_files[offset:offset+limit] if file.is_file()
    ]  

    return {"bk_size": log_files.__len__(), "pg_size": files.__len__(), "data": files}

@router.delete('/', description='Delete log files')
async def delete(files:List[Path]):
    for file in files:
        file_path = os.path.join(LOG_ROOT, file)
        if os.path.exists(file_path):os.remove(file_path)
    return "success", {"info":f"File(s) no longer exists"}