import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from pydantic import BaseModel
from database import engine, get_db
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.gzip import GZipMiddleware
from modules.downloader import download_video, download_audio

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=6)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


models.Base.metadata.create_all(bind=engine)

class VideoRequest(BaseModel):
    url: str
    resolution: str
    format_type: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download")
async def download(request: VideoRequest):
    """ Download a video or audio based on the frontend request """
    
    try:
        video = await download_video(request.url, request.resolution)
        print(video)
        return FileResponse(path=f"{video}", media_type="video/mp4" )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}/",response_model=schemas.User)
def get_user(user_id:int, db:Session=Depends(get_db)):
    db_user = crud.get_user(db,user_id =user_id )
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, updated_user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)