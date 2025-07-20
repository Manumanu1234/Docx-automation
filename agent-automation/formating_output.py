from textwrap import dedent
from agno.agent import Agent
from agno.models.groq import Groq
from clear import ClearFun
from GenScreen import ScreenShotGeneration
from dotenv import load_dotenv
import os
load_dotenv()
GROQ=os.getenv("GROQ_API_KEY")
code_output_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ),
    tools=[], 
    description=dedent("""\
        You are a precise and minimal code execution simulator. 
        You read code and generate only the output as if the code was executed in a terminal or console.

        You do not explain the code or add any extra commentary.
        You simulate input/output interactions faithfully and show only the output generated.
        Every line of output must be returned using the Python format: print("...").
    """),
    instructions=dedent("""\
        1. Receive the code (any language like Python, Java, C, etc.)
        2. Simulate the code execution as if it ran in an interpreter or terminal
        3. Output each line in this format: print("...")
        4. If the code requires input, simulate a realistic value and reflect both the prompt and input
        5. Do not show the original code or any explanation

        Example:

        Input Code:
        print("Enter a value")
        x = int(input())
        if x % 2 == 0:
            print("It is even")
        else:
            print("It is odd")

        Output:
        print("Enter a value: 10")
        print("It is even")
    """),
    expected_output=dedent("""\
        {Each output line must be wrapped in print("...")}

        Example:
        print("Enter a value: 7")
        print("It is odd")
    """),
    markdown=False,
    show_tool_calls=False,
    add_datetime_to_instructions=False,
)
def ProgramExec(input):
    ClearFun("code_execute.py")
    res = code_output_agent.run(input)
    final_val=res.content
    with open("code_execute.py", "w") as f:
        f.write(final_val)
    ScreenShotGeneration()
