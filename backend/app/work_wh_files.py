import os, pathlib, hashlib
from pathlib import Path




storage_dir = "storage"
script_dir = Path(__file__).resolve().parents[1]
STORAGE_DIR = os.path.join(script_dir, storage_dir)


def path_for_dotenv():
     return Path(__file__).resolve().parents[1] / ".env"

def create_home_user(user:str, path = '/' ):
     '''Создание домашнего каталога для пользователя'''
     #full_path = root + user + path
     #print(full_path)
    
     user_home = os.path.join(STORAGE_DIR, user, path)
     os.makedirs(user_home, exist_ok=True)
     #os.mkdir(user_home)

def create_dir(user:str, path ):
     '''Создание папки'''
     directory = os.path.join(STORAGE_DIR, user, path)
     try:
          os.mkdir(directory)
     except FileNotFoundError:
          return 'No such directory'
     else:
          return directory
def make_dir_path(user: str, path: str, filename: str = ''):
     return os.path.join(user, path, filename)


def make_file_path(dir_path: str, filename: str):
     return dir_path + '/' +filename

def touch_file(path):
     path = Path(STORAGE_DIR + '/' + path)
     path.touch()
     return path


def get_absolute_path(user_id: str, path: str):
       path = Path(STORAGE_DIR + '/' + user_id + '/' +path)
       return path

def get_hash(password: str):
     '''Получение хэша строки'''
     hash_passsword = hashlib.sha256()
     hash_passsword.update(password.encode('utf-8'))
     hash_passsword = hash_passsword.hexdigest()
     return hash_passsword

if __name__ == '__main__':

    print(path_for_dotenv())


