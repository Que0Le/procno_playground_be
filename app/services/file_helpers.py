import os 
from typing import Generator, Optional

from fastapi import HTTPException, UploadFile, status

from app.utilities import strings
from app.core.config import settings
from app.crud.crud_small import crud_record


def write_record_file_to_folder(db: Generator, file: UploadFile, file_extension: str) -> str:
    """ Return random filename if success, else empty string """
    tries = 10
    filename = ""
    while tries > 0:
        filename = strings.random_alphanumeric(length=32)
        if not os.path.isfile(f"{settings.DATA_PATH}/records/" + filename):
            record_db = crud_record.get_record_by_filename(db=db, filename=filename)
            if not record_db:
                break
    if filename != "":
        filename = filename + "." + file_extension
        with open(f"{settings.DATA_PATH}/records/{filename}", "wb+") as f:
            f.write(file.file.read())
    return filename