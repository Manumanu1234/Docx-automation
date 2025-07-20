from pydantic import BaseModel
class ImgGen(BaseModel):
    program:str

class DocFormat(BaseModel):
    doc_base:str

class ProgramGen(BaseModel):
    program_aim:str