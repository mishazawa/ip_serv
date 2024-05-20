from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

import  random, string
from pathlib import Path

IMAGE_FILE = 'img.gif'
BASE_DIR = Path(__file__).resolve().parent.parent.parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))
router = APIRouter()


@router.get("/asdasdgenerate", response_class=HTMLResponse)
def generate(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={ "id": f"/static/pictures/{randomword(57)}.gif" }
    )

@router.get("/pictures/{id}")
def pictures(id: str, request: Request):
    
    ip = request.headers.get('X-Forwarded-For', None)

    if not ip:
        return None

    print(f"new_ip: {ip} ({id})")
    def iterfile():
        with open(f"{str(Path(BASE_DIR, 'static', IMAGE_FILE))}", mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="image/gif")

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))