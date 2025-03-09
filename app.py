import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="www/static"),
    name="static",
)
templates = Jinja2Templates(directory="www/templates")

config = uvicorn.Config(
    app,
    host="0.0.0.0",
    port=8000,
    log_level="warning",
)
server = uvicorn.Server(config)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )
