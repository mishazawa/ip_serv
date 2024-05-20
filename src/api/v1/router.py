from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse

IMAGE = '/app/src/static/img.gif'

router = APIRouter()

@router.get("/pictures/{id}")
def pictures(id: str, request: Request):
    ip = request.headers.get('X-Forwarded-For', None)

    if not ip:
        raise HTTPException(status_code=404, detail="Item not found")

    print(f"new_ip: {ip} ({id})")
    def iterfile():
        with open(IMAGE, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="image/gif")

