from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import Annotated
from starlette import status

from database import db

from time import sleep

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def serSideRend(request, en, fi, expl):
	db.addTranslation(en, fi, expl)
	
	trans = db.getTranslations()
	print()
	rend = templates.get_template(
		name="index.html"
		).render({"request": request, "translations": trans})
	with open("./static/index.html", "w") as ff:
		ff.write(rend)

@app.get("/")
async def root(request: Request):
	cont = None
	with open("./static/index.html", "r") as ff:
		cont = ff.read()

	return HTMLResponse(content=cont, status_code=200 if not (cont is None) else 500)


@app.post("/")
async def sendTrans(request: Request, en: Annotated[str, Form()], fi: Annotated[str, Form()], expl: Annotated[str, Form()], bgTask: BackgroundTasks):
	bgTask.add_task(serSideRend, request, en, fi, expl)
	return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
