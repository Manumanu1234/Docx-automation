from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from formating_output import ProgramExec
from fastapi.responses import JSONResponse,FileResponse
from Schema import ImgGen,DocFormat
import os
app = FastAPI()
UPLOAD_FOLDER = "userFiles"
FIXED_FILENAME = "Sample_template.docx"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

@app.post("/image-generation/")
def create_item(data: ImgGen):
    output_path = "powershell_screenshot.png" 
    ProgramExec(data.program, output_path) 
    
    if os.path.exists(output_path):
        return FileResponse(output_path, media_type="image/png", filename="powershell_screenshot.png")
    else:
        return {"error": "Image generation failed"}

@app.post("/sample_docx_editing/")
async def DocAI(file: UploadFile = File(...)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return JSONResponse(status_code=400, content={"error": "Only .docx files are accepted."})
    file_path = os.path.join(UPLOAD_FOLDER, FIXED_FILENAME)
    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)
    
    return {"result": "success", "filename": file.filename}

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app=app,host="0.0.0.0",port=8000)
