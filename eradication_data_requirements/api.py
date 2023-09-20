from eradication_data_requirements.cli import (
    write_effort_and_captures_with_probability,
    write_progress_probability_figure,
)
from fastapi import FastAPI

api = FastAPI()


@api.get("/")
async def read_main():
    return {"msg": "Hello World"}


@api.get("/write_effort_and_captures_with_probability")
async def api_write_effort_and_captures_with_probability(
    input_path: str, bootstrapping_number: int, output_path: str
):
    write_effort_and_captures_with_probability(input_path, bootstrapping_number, output_path)


@api.get("/write_probability_figure")
async def api_write_probability_figure(input_path: str, output_path: str):
    write_progress_probability_figure(input_path, output_path)
