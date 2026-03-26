from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name="static")
templates = Jinja2Templates(directory="templates") #dobbiamo dire al motore di templating dove sono contenuti i nostri file di templates
#meccanismo che ci permette di prendere il codice che abbiamo scritto e metterlo in output si chiama TEMPLATING
product_list = [
    { "name":"notebook DELL", "price": 2999.99, "location": "Cagliari"},
    { "name":"smartphone Xiaomi", "price": 999.99, "location": "Napoli"},
    { "name":"notebook ASUS", "price": 1599.99, "location": "Bari"}
]
@app.get("/", response_class=HTMLResponse)  #formato in cui fastapi deve restituire il valore della funzione ---> statico
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name='home.html',
        context={"text": "Welcome to the store"}
    )
@app.get("/products", response_class=HTMLResponse)
def products(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='products.html',
        context={"product_list": product_list}
    )

"""
@app.get("/ciao")
def pippo
url_for('pippo') ->"/ciao"
"""