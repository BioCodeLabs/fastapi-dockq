from functions.calculate import get_csv_results
from fastapi import FastAPI, File, UploadFile
from fastapi import APIRouter, Depends
from functions import calculate
import os
from schemes.payload import *


router = APIRouter()


@router.get("/download")
def download_results(payload:payloadScheme):

    get_csv_results(payload)
