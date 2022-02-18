# from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi import APIRouter
# import io
import random
import os
from starlette.responses import StreamingResponse

from app.utilities.strings import clean_filename

router = APIRouter()


def iter_file(path: str):
    with open(path, mode="rb") as file_like:
        yield from file_like


@router.get("/streaming-response/")
async def get_streaming_response() -> StreamingResponse:
    return StreamingResponse(
        iter_file("./data/records/imperial_march_60.wav"),
        media_type="audio/wave"
    )


@router.get("/file-response/")
async def get_file_response():
    return FileResponse("./data/records/imperial_march_60.wav")


@router.get("/records/{record_filename}")
async def get_record_by_file(record_filename: str):
    return FileResponse(
        # TODO: Implement clean_filename. Its still a placeholder function
        "./data/records/" + clean_filename(record_filename)
    )


@router.get("/dummies-records/")
async def get_dummies_record_by_random():
    """ Return a random audio file ("mp3", "wav") in records folder """
    listdir = os.listdir("./data/records/")
    listfiles = [item for item in listdir if item.split(".")[-1] in ["mp3", "wav"]]
    random_file = random.choice(listfiles)
    return FileResponse(
        "./data/records/" + random_file
    )
