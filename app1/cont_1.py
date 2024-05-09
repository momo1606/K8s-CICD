from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import os
import requests

app = FastAPI()

#second_app_url = "http://app2:6001/process_csv"
second_app_url = "http://app2-service:81/process_csv"



class StoreItem(BaseModel):
    file: Optional[str] = None
    data: str = None

class CalculateItem(BaseModel):
    file: str = None
    product: str = None

@app.post("/store-file")
async def store_file(item: StoreItem):
    if item.file is None:
        return {"file": None, "error": "Invalid JSON input."}

    file_path = "/mohammed_PV_dir/" + item.file  
    try:
        with open(file_path, 'w') as f:
            f.write(item.data)
        return {"file": item.file, "message": "Success."}
    except Exception as e:
        return {"file": item.file, "error": "Error while storing the file to the storage."}


@app.post("/calculate")
async def calculate(request: Request):

    try:
        body = await request.json()
        item = CalculateItem(**body)
    except Exception as e:
        return {"file": None, "error": "Invalid JSON input."}
    
    if not item.file:
        return {"file": None, "error": "Invalid JSON input."}
    
    if not item.product:
        return {"file": None, "error": "Invalid JSON input."}
    
    if not os.path.isfile("/mohammed_PV_dir/"+item.file):
        return {"file": item.file, "error": "File not found."}
    
    try:
        response = requests.post(second_app_url, json={"file": item.file, "product": item.product})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle connection errors or unsuccessful responses
        return {"error": str(e)}

if __name__ == "__main__":
    from hypercorn.config import Config
    from hypercorn.asyncio import serve
    import asyncio

    config = Config()
    config.bind = ["0.0.0.0:6000"]
    asyncio.run(serve(app, config))
