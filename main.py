from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
import io
from model import model_pipeline
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/')
async def page():
    return JSONResponse({"Message": "All Modules Loaded Successfully"})

@app.post('/help')
async def help(text: str, image: UploadFile = File(...)):
    try:
        content = await image.read()
        try:
            img = Image.open(io.BytesIO(content))
            img.verify()
            img = Image.open(io.BytesIO(content))
        except UnidentifiedImageError:
            return JSONResponse(status_code=400, content={"Message": "Uploaded file is not a valid image"})
        finally:
            await image.close()
        result = model_pipeline(text, img)

        return JSONResponse({"Message": result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"Message": str(e)})
