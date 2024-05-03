from fastapi import FastAPI, status
from fastapi.requests import Request


app = FastAPI()

@app.post("/")
async def root(request: Request):
    print(request.body())
    return status.HTTP_200_OK