import os
import hashlib

from fastapi import  HTTPException, Query, Form, Depends, APIRouter, UploadFile, File as FastAPIFile

from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from database import get_db
from models import User, File, Dirs
from work_wh_files import create_home_user, get_hash, make_dir_path, touch_file, make_file_path, create_dir, get_absolute_path
from pathlib import Path
import work_wh_files as wwf
from typing import List

files = APIRouter(prefix="/files", tags=["FILES"])


@files.get('/files/all',response_model=List[Dirs])
async def get_all_files(user_id: str = Query(),
                      db: Session = Depends(get_db)):
    files = db.query(File).filter(File.owner == user_id).all()
    return files

@files.get('',response_model=List[Dirs])
async def get_files(user_id: str = Query(),
                      dir: str = Query(),
                      db: Session = Depends(get_db)):
    files = db.query(File).filter(File.owner == user_id, File.parrent_dir == dir).all()
    return files


@files.post('/folder/')
async def create_folder(user_id: str = Form(),
                        current_dir: str = Query(),     
                             folder_name: str = Form(...),
                              db: Session = Depends(get_db)
                             ):
    veri_dir = db.query(File).filter(File.owner == user_id, File.is_folder == True, File.path == current_dir).first()
    if veri_dir:
        time = db.query(func.now()).scalar()
        folder = File(
            filename = folder_name,
            is_folder = True,
            parrent_dir = current_dir,
            path = make_dir_path(current_dir, folder_name),
            upload_date = time,
            size = 0,
            owner = user_id
            )
        
        create_dir(str(user_id), folder.path)
        db.add(folder)
        db.commit()
        db.refresh(folder)
        return folder
    else:
          raise HTTPException(status_code=404, detail="ERROR: parrent directory did not find")
    

@files.post('folders')
async def open_folder(user_id: str = Form(),
                       current_dir: str = Query(),
                        folder_name: str = Form(),
                              db: Session = Depends(get_db) 
                              ):
    folder = db.query(File).filter(File.owner == user_id, File.parrent_dir == current_dir, File.is_folder == True, File.filename == folder_name).first()
    if folder:
        return folder
    else:
        raise HTTPException(404, 'НЕЛЬЗЯ ААААААА 67')

        

@files.post("/upload/")
async def create_upload_file(   user_id: str = Form(),     
                             current_dir: str = Query(),
                             file: UploadFile = FastAPIFile(...),
                              db: Session = Depends(get_db)    
                             ):
    content = await file.read()
    upload_path = make_dir_path(user_id, path = current_dir, filename=file.filename)
    data_path = make_file_path(current_dir, file.filename)
    path = touch_file(upload_path)
    with open(path, 'wb') as f:
       f.write(content)
    time = db.query(func.now()).scalar()
    add_file = File(
        filename =  file.filename,
        is_folder = False,
        parrent_dir = current_dir,
        path = data_path,
        upload_date =  time,
        size = file.size,
        owner = int(user_id)
    )
    db.add(add_file)
    db.commit()
    db.refresh(add_file)

    return add_file




@files.post("/download")
async def download_file(     user_id: str = Form(),
                             current_dir: str = Query(),
                             filename: str = Form(...),
                              db: Session = Depends(get_db)
                              ):
     dow_file = db.query(File).filter(File.owner == user_id, File.path == make_file_path(current_dir, filename)).first()
     if dow_file:
        filepath = get_absolute_path(user_id, make_file_path(current_dir, filename) )
        return FileResponse(
            path=filepath, 
            filename=filename, # Это заставляет браузер скачивать файл
            media_type='application/octet-stream' # Универсальный тип для бинарных данных
        )
     else:
        raise HTTPException(status_code=404, detail="ERROR: file is not founded")


@files.get('/{user_id}/file')
async def get_files_in_dir(user_id: str,
                        dir_path: str = Query(...),
                        db: Session = Depends(get_db)
                        ):
    return db.query(File).filter(File.path == dir_path, File.owner == int(user_id)).all()



              