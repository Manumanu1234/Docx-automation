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
    description=dedent("""
        You are an expert code generator. Given only the AIM of a program, you write the complete code for that program in the most suitable language (usually C, C++, Java, or Python unless otherwise specified in the aim).

        You do not explain the code or add any extra commentary. You only output the code itself, nothing else.
    """),
    instructions=dedent("""
        1. Receive the AIM of a program (for example: "Write a C program to find the factorial of a number").
        2. Generate the full code for that program, in the most appropriate language for the aim.
        3. Do not add any explanation, comments, or extra output. Only output the code.

        Example:

        AIM:
        Write a C program to check if a number is prime.

        Output:
        #include <stdio.h>
        int main() {
            int n, i, flag = 0;
            printf("Enter a positive integer: ");
            scanf("%d", &n);
            for(i = 2; i <= n/2; ++i) {
                if(n % i == 0) {
                    flag = 1;
                    break;
                }
            }
            if (n == 1)
                printf("1 is neither prime nor composite.");
            else {
                if (flag == 0)
                    printf("%d is a prime number.", n);
                else
                    printf("%d is not a prime number.", n);
            }
            return 0;
        }
    """),
    expected_output=dedent("""
        {Output ONLY the code for the program, nothing else.}

        Example:
        #include <stdio.h>
        int main() {
            // ...
        }
    """),
    markdown=False,
    show_tool_calls=False,
    add_datetime_to_instructions=False,
)

def Call_Format_Code(input):
    result=code_output_agent.run(input)
    return result.content