import docx2txt
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from pydantic import Field, create_model
from pydantic import BaseModel, Field
import docx2txt
import re
from pydantic import create_model
import os
from dotenv import load_dotenv
load_dotenv()
from mcp_server import AgentCall
GROQAPIKEY=os.getenv("GROQ_API_KEY")
llm=ChatGroq(api_key=GROQAPIKEY,
             model_name="gemma2-9b-it",temperature=0)  

def DocumentProcessing(filename):
    class ExtractReleventDocuments(BaseModel):
        arr: list[str] = Field(
            description="""
            You are an intelligent document parser.

            TASK:
            - Extract all lines or fields from the document that begin with `//`.
            - Do NOT include any line that doesn't start with `//`.

            OUTPUT FORMAT:
            A list of strings, where each string is a comment from the document that starts with `//`.

            EXAMPLE:
            ['//experiment name', '//dataset used', '//paste output']
            """
        )

    text_content = docx2txt.process(filename)

    llm_str = llm.with_structured_output(ExtractReleventDocuments)

    prompt = f"""
        You are a smart document analyzer.

        TASK:
        - Analyze the document text below.
        - Extract and return ONLY the lines that begin with `//`.
        - Return them as a list of strings.
        - Do NOT include any other text or lines.

        ### Document Text:
        {text_content}
        """

    template = PromptTemplate.from_template(prompt)
    chain = template | llm_str
    data = chain.invoke({"topic": text_content})
    print(data)
    return data.arr


global response
def MappingFun(result):
    global response
    my_dict={}
    for val in result:
        match = re.search(r'\b(output|Output|OUTPUT)\b', val)
        if match:
            my_dict[val]='image'
        else:
            my_dict[val]=""
    fields = {
        key: (str, Field(description=f"Generate an apt name for {key} for example //paste experiment name  it should Experiment Name that means just avoid the //paste"))
        for key in my_dict
    }
    GenerateExtractValue = create_model("GenerateExtractValue", **fields)
    llm_struct=llm.with_structured_output(GenerateExtractValue)
    response=llm_struct.invoke("""
                    You are given a set of field comments taken from a document. Each field comment starts with '//' and includes filler words like 'paste', 'enter', or similar. Your task is to generate a clean, human-readable field name by removing such filler words and formatting the rest appropriately (capitalize each major word).
                        For example:
                        - '//paste experiment name' → 'Experiment Name'
                        - '// enter compiler name' → 'Compiler Name'
                        - '//paste aim of the program' → 'Aim of the Program'

                        Generate appropriate values for each field based on this transformation logic.                 
                    """)
    my_dict2={}
    for field_name, value in response:
        my_dict2[value]=''
    return my_dict2
        
def DataFilling(my_dict2):
    final_dict={}
    for key,val in my_dict2.items():
        for field_name, value in response:
            if key==value:
                final_dict[field_name]=val    
    print(final_dict)
    return final_dict
        
def Promptifying(final_dict):
    prompt_for_agent = f"""
                You are provided with a `.docx` file located at:

                D:/Collage Automation Project/agent-automation/userFiles/Sample_template.docx

                **IMPORTANT INSTRUCTIONS — FOLLOW STRICTLY**
                - Do **NOT** create a new file. Work on the provided file only.
                - Use only the tools given to you.
                - Do **NOT** alter formatting, layout, or styles.
                - Do **NOT** save a copy. Simply overwrite/save the current file.
                - If you instruct to add image user add_picture tool to add image in the document.
                ---

                **TASKS TO PERFORM**

                1. Analyze the structure of the .docx file.
                2. Locate all comments in the document.
                3. Replace each comment with its corresponding value from the dictionary below:
                4. if the value is output or paste output then add the image in the document using add_picture tool .
                {chr(10).join([f"{k} with  {v}" for k, v in final_dict.items()])}

                5. Once all replacements are done, save the file and stop the process.
                ---

                **NOTES**
                - Replace only the **comments** (not regular text) with the appropriate values.
                - Ensure values are inserted in the correct location based on the comment label.
                - Do not add or remove any other content.

            """
    return prompt_for_agent
def MainAnalysis(filename:str):
    result=DocumentProcessing(filename=filename)
    result2=MappingFun(result)
    #new endpoint
    # final_dict=DataFilling(result2)
    # prompt=Promptifying(final_dict)
    # AgentCall(prompt)
    return result2