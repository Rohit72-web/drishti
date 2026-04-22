from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Optional
import tempfile, os
from modules.output_engine import run_drishti

app = FastAPI(title="DRISHTI API")

@app.post("/analyse")
async def analyse_store(
    images: List[UploadFile] = File(...),
    lat: float = Form(...),
    lng: float = Form(...),
    pincode: str = Form(...),
    shop_size: Optional[float] = Form(None),
    rent: Optional[float] = Form(None),
    years: Optional[float] = Form(None)
):
    tmp_paths = []
    for img in images:
        content = await img.read()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        tmp.write(content)
        tmp_paths.append(tmp.name)

    result = run_drishti(tmp_paths, lat, lng, pincode,
                          shop_size, rent, years)

    for p in tmp_paths:
        os.unlink(p)

    return result