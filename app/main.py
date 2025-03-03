import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from pydantic import BaseModel
from database import engine, get_db, SessionLocal
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import yt_dlp
from modules.downloader import download_audio, download_video, get_domain, sanitize_filename

app = FastAPI()
templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

class VideoRequest(BaseModel):
    url: str


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download")
async def download(request: VideoRequest):
    """ Download a video or audio based on the frontend request """
    url = request.url
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                raise HTTPException(status_code=400, detail="Could not retrieve video info")
            
            video_data = {
                "title": info.get("title"),
                "author": info.get("uploader"),
                "thumbnail": info.get("thumbnail"),
                "resolutions": sorted(set(f["format_note"] for f in info.get("formats", []) if "format_note" in f))
            }
            return video_data
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