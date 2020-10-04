from pathlib import Path
from pprint import pprint
from typing import Optional

from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseSettings


class Settings(BaseSettings):
    mount_path: str = "/mnt/openapi"

    @property
    def openapi_url(self):
        return f"{self.mount_path}/openapi.json"


settings = Settings()

app = FastAPI(openapi_url=settings.openapi_url)
handler = Mangum(app)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/ls")
def ls():
    mount_path = Path(settings.mount_path)
    print(f"contents of mount path:")
    mount_path_contents = list(mount_path.iterdir())
    pprint(mount_path_contents)
    some_file = Path(mount_path, "foo")
    some_file.touch(exist_ok=True)
    some_file.write_text(some_file.read_text() + " wtf")
    return {
        "mount path contents": list(mount_path.iterdir()),
        "file_body": some_file.read_text(),
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
