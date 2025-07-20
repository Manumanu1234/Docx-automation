from fastapi import FastAPI, UploadFile, File,Request
from fastapi.middleware.cors import CORSMiddleware
from formating_output import ProgramExec
from fastapi.responses import JSONResponse,FileResponse
from Schema import ImgGen,DocFormat,ProgramGen
from data_manupulation import MainAnalysis
from data_manupulation import DataFilling,Promptifying
from mcp_server import AgentCall
from formating_code import Call_Format_Code
from formating_output import ProgramExec
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
    filename = "userFiles/Sample_template.docx"
    result=MainAnalysis(filename)
    print("---------------------------------------------------------------")
    print(result)
    return {"result": "success", "details": result}
@app.post("/final-submission/")
async def SubmitFinal(request: Request):
    import base64
    data = await request.json()
    # Save output image if present
    output_key = None
    img_path = None
    for k in data:
        if k.lower() == "output":
            output_key = k
            break
    if output_key and data[output_key]:
        img_data = data[output_key]
        if img_data.startswith("data:image"):
            header, b64data = img_data.split(",", 1)
            img_bytes = base64.b64decode(b64data)
            img_path = os.path.join(UPLOAD_FOLDER, "output_image.png")
            try:
                with open(img_path, "wb") as f:
                    f.write(img_bytes)
                # Only update the value if save succeeded
                data[output_key] =" Add this image in this path : D:/Collage Automation Project/agent-automation/userFiles/output_image.png with width 5"
                print(f"Image saved to {img_path}")
            except Exception as e:
                print(f"Failed to save image: {e}")
    res = DataFilling(data)
    prompt = Promptifying(res)
    await AgentCall(prompt)
    file_path = os.path.abspath("userFiles/Sample_template.docx")
    if os.path.exists(file_path):
        # Return the file directly as a response
        return FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="Sample_template.docx",
            headers={"result": "success"}
        )
    else:
        return JSONResponse(content={"error": "File not found."}, status_code=404)
    
@app.post("/ai-code-generation/")
def ai_code_generation(request: ProgramGen):
    import base64
    data = request.program_aim
    response=Call_Format_Code(data)
    return {"result": "success", "code": response}

@app.post("/ai-image-generation/")
def ai_image_generation(request: ProgramGen):
    data = request.program_aim
    ProgramExec(data)
    img_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, "output_image.png"))
    if os.path.exists(img_path):
        return FileResponse(
            img_path,
            media_type="image/png",
            filename="output_image.png"
        )
    else:
        return JSONResponse(content={"error": "Image not found."}, status_code=404)

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app=app,host="0.0.0.0",port=8000)
