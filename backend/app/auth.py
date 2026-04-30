import os
import hashlib

from fastapi import FastAPI, HTTPException, Form, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from database import get_db
from models import User, File, UserWithoutVerify, Uwv, Us
from work_wh_files import create_home_user, get_hash
from email_addr import send_confirmation_code
from typing import List


auth_user = APIRouter(tags=["AUTH"])

@auth_user.post('/register')
async def register(email: str = Form(),
                   user_name: str = Form(),
                   password: str= Form(),
                   db: Session = Depends(get_db)):
   '''Регистрация пользователя'''
   db_user = db.query(User).filter(User.user_email == email).first()
   if db_user:
      raise HTTPException(status_code=409, detail="This user already exists")
   else:
    hash_password = get_hash(password)
    code = send_confirmation_code(email)
    user = UserWithoutVerify(
      # user_id = user_id,
        user_email = email,
        user_name = user_name,
        hash_password = hash_password,
        user_code = code
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
@auth_user.get('/all_no_verify_user', response_model=List[Uwv])
async def get_uwv( db: Session = Depends(get_db)):
  return db.query(UserWithoutVerify).all()

@auth_user.get('/all__user', response_model=List[Us])
async def get_us( db: Session = Depends(get_db)):
  return db.query(User).all()


@auth_user.post('/verify')
async def verify(email: str = Form(),
                 code: str = Form(),
                  db: Session = Depends(get_db)):
  curent_user = db.query(UserWithoutVerify).filter(UserWithoutVerify.user_email == email).first()
  if curent_user:
    if code == curent_user.user_code:
     
      user = User(
        # user_id = user_id,
          user_email = curent_user.user_email,
          user_name = curent_user.user_name,
          hash_password = curent_user.hash_password
          )
      
      db.add(user)
      db.commit()
      db.refresh(user)
      create_home_user(str(user.user_id),'home')
      db.delete(curent_user)
      folder = File(
            filename = 'home',
            is_folder = True,
            parrent_dir = None,
            path = 'home',
            upload_date = None,
            size = 0,
            owner = user.user_id
            )
      db.add(folder)
      db.commit()
      db.refresh(folder)
      return user
    else:
      raise HTTPException(status_code=404, detail="Code in incorrect")
  else:
     raise HTTPException(status_code=404, detail="User does not exist")

@auth_user.post('/login')
async def login(email: str = Form(),
                password: str = Form(),
                db: Session = Depends(get_db)):
  '''Login in system'''
  current_user = db.query(User).filter(User.user_email == email).first()
  if current_user:
    if current_user.hash_password == get_hash(password):
      return current_user
    else:
       raise HTTPException(status_code=401, detail="The password is not correct")
  else:
    raise HTTPException(status_code=404, detail="User with this email is not exists")

    
    
   

#if __name__ == '__main__':
 #   import uvicorn
  #  uvicorn.run('auth:app', host="0.0.0.0", port=8000, reload = True)