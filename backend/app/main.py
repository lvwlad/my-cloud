from fastapi import FastAPI
from auth import auth_user  
from files import files

app = FastAPI(
    title="NoCloud",
    version="1.0"
)

app.include_router(auth_user)
app.include_router(files)


@app.get("/")
def root():
    return {"message": "MM"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload = True)