from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates") #dobbiamo dire al motore di templating dove sono contenuti i nostri file di templates
#meccanismo che ci permette di prendere il codice che abbiamo scritto e metterlo in output si chiama TEMPLATING

"""
@app.get("/", response_class=HTMLResponse)  #formato in cui fastapi deve restituire il valore della funzione ---> statico
def home(request: Request):
    * Renders the home page. *
    return templates.TemplateResponse(
        request=request, name='home.html'  #quale file html passare al sito (in questo caso home o base)
    ) # questo pattern verrà ripetuto
"""

@app.get("/", response_class=HTMLResponse)  #formato in cui fastapi deve restituire il valore della funzione ---> statico
def home(request: Request):
    text = {
        "title" : "Home page",
        "content" : "Welcome to the home page!"
    }
    context = {
        "text" : text,
        "sequence" : ["a", "b", "c"]
    }
    return templates.TemplateResponse(
        request=request,
        name='home.html',
        context=context
    )

