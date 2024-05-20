from fastapi import FastAPI, APIRouter, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import re, base64, random, string

from .api.v1.router import router as trackers

app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory='/app/src/templates') # container path

app.include_router(trackers, prefix="/static")

fake_headers = {
    "X-Powered-By": "PHP 8.1.1",
    "Set-Cookie": "PHPSESSID=aWxvdmV5b3U=",
    "Content-Type": "text/html",
}

@router.get("/asdasdgenerate", response_class=HTMLResponse)
def generate(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={ "id": f"/static/pictures/{randomword(57)}.gif" }
    )

@router.get("/{_:path}", response_class=HTMLResponse)
def index():
    return HTMLResponse(
        headers=fake_headers,
        content="<body><h1>Not found</h1></body>",
        media_type="text/html",
        status_code=404
    )

app.include_router(router)


@app.middleware("http")
async def filter_bots(request: Request, call_next):
    ua = request.headers.get('User-Agent', None)

    if is_ua_in_blocklist(ua):
        return Response(
            headers=fake_headers,
            status_code=403,
        )

    return await call_next(request)

UA_TG = re.compile('telegram', re.IGNORECASE)
UA_BOT = re.compile('bot', re.IGNORECASE)

def is_ua_in_blocklist(ua):
    if not ua:
        return True
    if UA_TG.search(ua):
       return True 
    if UA_BOT.search(ua):
        return True
    return False

def randomword(length):
   letters = string.ascii_lowercase
   return base64.b64encode(bytes(''.join(random.choice(letters) for i in range(length)), 'utf-8')).decode("utf-8")