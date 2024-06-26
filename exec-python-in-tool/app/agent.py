
import os
from langchain_core.tools import tool
from datetime import datetime, timedelta, timezone
from langchain_google_genai import GoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime, timedelta, timezone
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from tools import get_now, create_and_edit_file, execute_python_file, poetry_command
from langgraph.graph import MessageGraph
from langgraph.prebuilt import ToolNode, tools_condition

# llm = GoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=os.environ["GOOGLE_API_KEY"])
llm = ChatAnthropic(model="claude-3-haiku-20240307")
# llm = ChatOpenAI(model="gpt-4o")
tools = [get_now, create_and_edit_file, execute_python_file, poetry_command]

graph_builder = MessageGraph()
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_node("chatbot", llm.bind_tools(tools))
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.set_entry_point("chatbot")

exec_graph = graph_builder.compile()

# 実行したいPythonコードを文字列として定義
code = """
task: googleのホームページには何が書いてありますか？

toolを使って、必要ならばファイルを作成し、実行しながらタスクを達成してください。
"""
    
if __name__ == "__main__":
    for steps in exec_graph.stream(code, stream_mode="values"):
        # print("___________________________________")
        steps[-1].pretty_print()
        # print(steps[-1])
        # print("___________________________________")
        # if isinstance(message, tuple):
        #     print(message)
        # else:
        #     message.pretty_print() 