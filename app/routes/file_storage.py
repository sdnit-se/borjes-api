import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/folder")
async def list_files(folder: str = None):
    """
    List all files in {folder} directory
    """
    if not folder:
        return os.listdir("/file-storage")
    try:
        # I dont think this is so smart but I fix it later
        # need to go and eat now
        return os.listdir(f"/file-storage/{folder}")
    except FileNotFoundError:
        return {"status": "error", "detail": "Folder not found"}


@router.get("/file")
async def get_file(file: str):
    """
    Get a file from the /file-storage directory
    """
    # TODO: Need to add some security here
    return HTMLResponse(open(f"/file-storage/{file}").read())
