from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


load_dotenv()

@tool
def calculator(a:float,b:float)-> str:
    '''Useful for performing some basic arithmetic operations'''
    print("Calculator Tool is utilized")
    return f"The sum is {a+b}"

@tool
def convert_units(value:float,from_unit:str,to_unit:str)-> str:
    '''Useful for unit convertions'''
    from pint import UnitRegistry
    print("Tool Trigger")
    ureg = UnitRegistry()
    try:
        res = (value * ureg(from_unit)).to(to_unit)
        return f"{value} {from_unit} is {res}"
    except Exception as e:
        return f"conversion error: {e}"

@tool
def solve_math(expression:str) -> str:
    '''Useful for solving mathematical expressions'''
    import sympy as sp
    print("Tool Trigger")
    try:
        expr = sp.sympify(expression)
        symbols = expr.free_symbols
        if symbols:
            sols = sp.solve(expr)
            if not sols:
                return "No algebraic solutions found."
            # Format solutions (numeric if possible)
            formatted = []
            for s in sols:
                try:
                    formatted.append(str(sp.N(s)))
                except Exception:
                    formatted.append(str(s))
            return f"Solutions: {', '.join(formatted)}"
        else:
            # Pure numeric expression; evaluate
            val = sp.N(expr)
            return f"Result: {val}"
    except Exception as e:
        return f"math error: {e}"

@tool
def recent_news():
    '''Useful for recent news articles'''
    import requests
    try:
        api_key = os.getenv("NEWS_API_KEY")
        url = ('https://newsapi.org/v2/everything?'
               'q=Apple&'
               'from=2025-06-10&'
               'sortBy=popularity&'
               'apiKey={}'.format(api_key))
        response = requests.get(url)
        headlines = [article["title"] for article in response["articles"][:3]]
        print("Tool Trigger")
        return f"Top Headlines are {headlines}"
    except Exception as e:
        return f"recent news error: {e}"

def agent(user_input):
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=5,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    tools = [calculator, convert_units, solve_math, recent_news]
    agent_excecutor = create_react_agent(model,tools)

    res = ""
    for chunk in agent_excecutor.stream(
            {"messages" : [HumanMessage(content = user_input)]}
    ):
        if "agent" in chunk and "messages" in chunk["agent"]:
            for message in chunk["agent"]["messages"]:
                res += message.content
    return res


