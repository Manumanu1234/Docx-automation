import asyncio
import datetime
import warnings
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_together import ChatTogether
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.prompts import PromptTemplate
# Suppress specific warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
import os
from dotenv import load_dotenv
load_dotenv()
TOGETHERAPIKEY=os.getenv("TOGETHER_API_KEY")
async def run_agent(message: str) -> None:
    mcp_tools = StdioServerParameters(
        command="uvx",
        args=["--from", "office-word-mcp-server", "word_mcp_server"]
    )

    async with stdio_client(mcp_tools) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            llm = ChatTogether(
                model="moonshotai/Kimi-K2-Instruct",
                temperature=0,
                api_key=TOGETHERAPIKEY
            )
            

            custom_prompt = PromptTemplate.from_template(
                """You are a helpful assistant that works with .docx documents using a toolset.
            Use the tools to examine, update, and finalize the Word document as instructed.

            Instructions: {input}

            {agent_scratchpad}"""
            )
            agent = AgentExecutor(
                agent=create_tool_calling_agent(llm=llm, tools=tools, prompt=custom_prompt),
                tools=tools,
                verbose=True
            )

            data = {
                "input": message
            }

            await agent.ainvoke(data)
            print("Done")
            end_time = datetime.datetime.now()
            print("End time:", end_time)

def AgentCall(input):
    try:
        # Avoid "no current event loop" deprecation warning
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(
            run_agent(
                input
            )
        )
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            print("No problem: Event loop was already closed.")
        else:
            raise
    