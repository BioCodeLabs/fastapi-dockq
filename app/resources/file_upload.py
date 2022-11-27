from fastapi import FastAPI, File, UploadFile
from fastapi import APIRouter, Depends
from functions import calculate
import os
from schemes.payload import *
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
    results=payloadScheme(pay_01="",pay_02="",pay_03="",pay_04="",pay_05="")


    #results=calculate.calc_pdockq(file_location)

    #pdockq_results={"results":{"pay_01":results.pay_01,"pay_02":results.pay_02,"pay_03":results.pay_03}}

    table=calculate.get_interacting_residues(file_location)
    #full_response=[]
    #full_response.append(pdockq_results)
    #full_response.append(table)
    results=calculate.calc_pdockq(file_location)
    table.append(results)
    os.remove(file_location)
    print(table)
    return table
    #return full_response
    #return pdockq_results
    return results

    ##return {"message": f"Successfully uploaded {file.filename}"}
