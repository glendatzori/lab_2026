from fastapi import FastAPI

app = FastAPI()

# per ogni n point affiungiamo una finzione python
@app.get("/")  # n point, richiesta get, tra parentesi il percorso
def hello_world():
    return "Hello World!"

# 127.0.0.1 è URL del nostro computer (local host)

# @app.get("/hello")
# def hello_world():
#     return "Hello World!"