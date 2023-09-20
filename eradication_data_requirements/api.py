from fastapi import FastAPI

api = FastAPI()


@api.get("/")
async def read_main():
    return {"msg": "Hello World"}


@api.get("/write_effort_and_captures_with_probability")
async def api_write_effort_and_captures_with_probability():
    pass
