from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.routes.borjes_extra.dungeons_and_dragons import router as dnd_route
from app.routes.borjes_extra.weather import router as weather_route
from app.routes.file_storage import router as file_storage_route

title = "Börjes File Storage"
description = """
This is my super secure API which I've built to easily retrieve my files
when I am on the run together with some extra cool things I need
"""
version = "0.1.0"

app = FastAPI(
    title=title,
    description=description,
    version=version,
    # Börje didn't want the docs to be shown.
    # Think this is becuase of security things
    redoc_url=False,
    docs_url=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dnd_route, prefix="/dnd")
app.include_router(weather_route, prefix="/weather")
app.include_router(file_storage_route, prefix="/file-storage")


@app.get("/")
async def root():
    return HTMLResponse(
        content=f"""
<html>
    <head>
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <h4>{description}</h4>
        <h5>My File Storage API is currently running version: {version}</h5>
        <p>Since I have the source code I don't need API docs</p>
    </body>
</html>
"""
    )
