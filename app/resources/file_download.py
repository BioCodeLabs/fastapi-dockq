import io
from functions.calculate import get_csv_results
from fastapi import FastAPI, File, UploadFile
from fastapi import APIRouter, Depends
from functions import calculate
import os
from schemes.payload import *
from starlette.responses import FileResponse

router = APIRouter()


@router.post("/download")
def download_results(data:List[payloadScheme]):
    csv_path=get_csv_results(data)

    
 
    return FileResponse(path=csv_path,filename=csv_path, media_type="text/csv")


@router.post("/download2", response_class=FileResponse)
async def download_results2(data:List[payloadScheme]):
    csv_path=get_csv_results(data)
    return csv_path