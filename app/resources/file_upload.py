from fastapi import FastAPI, File, UploadFile
from fastapi import APIRouter, Depends
from functions import calculate
router = APIRouter()

@router.get("/test/")
async def test():
    return {"hello"}


@router.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        
        contents = file.file.read()
        file_location = f"pdbs/{file.filename}"
        with open(file_location, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    results=calculate.calc_pdockq(file_location)

    return {"message":results}

    ##return {"message": f"Successfully uploaded {file.filename}"}

