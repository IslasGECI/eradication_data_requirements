from fastapi import FastAPI

api = FastAPI()


@api.get("/")
async def read_main():
    return {"msg": "Hello World"}
