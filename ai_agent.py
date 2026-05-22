import os
import math
from dotenv import load_dotenv

from langchain.tools import tool
from langchain_groq import ChatGroq

# ---------------- LOAD ENV ---------------- #

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---------------- TOOLS ---------------- #

@tool
def calculator(expression: str) -> str:
    """
    Useful for solving mathematical calculations.

    Use valid Python math expressions only.

    Examples:
    - 2 + 2
    - math.sqrt(144)
    - math.factorial(5)
    """

    try:

        expression = expression.lower().strip()

        # Handle natural language factorial
        if "factorial of" in expression:

            number = expression.replace("factorial of", "").strip()

            expression = f"math.factorial({number})"

        # Handle square root
        elif "square root of" in expression:

            number = expression.replace("square root of", "").strip()

            expression = f"math.sqrt({number})"

        # Evaluate expression safely
        result = eval(
            expression,
            {"math": math, "__builtins__": {}}
        )

        return str(result)

    except Exception as e:
        return f"Calculation Error: {e}"


@tool
def lookup_user(user_id: int) -> str:
    """
    Lookup user details from mock database.
    """

    mock_db = {
        42: "Name: Alice Johnson, Role: Senior Engineer, Access: Admin",
        85: "Name: Bob Smith, Role: Data Analyst, Access: Standard",
        100: "Name: Charlie Brown, Role: AI Intern, Access: Limited",
    }

    return mock_db.get(
        int(user_id),
        f"User ID {user_id} not found."
    )


# ---------------- LLM ---------------- #

tools = [calculator, lookup_user]

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)

# ---------------- MAIN PROGRAM ---------------- #

if __name__ == "__main__":

    print("\n🤖 Groq AI Agent Started!")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        # Exit condition
        if user_input.lower() in ["exit", "quit"]:

            print("\n👋 Goodbye!")
            break

        try:

            # Ask LLM
            response = llm_with_tools.invoke(user_input)

            # If tool is called
            if response.tool_calls:

                for tool_call in response.tool_calls:

                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]

                    # ---------------- TOOL EXECUTION ---------------- #

                    if tool_name == "calculator":

                        result = calculator.invoke(tool_args)

                    elif tool_name == "lookup_user":

                        result = lookup_user.invoke(tool_args)

                    else:

                        result = "Unknown Tool"

                    # ---------------- DISPLAY TOOL RESULT ---------------- #

                    print(f"\n🤖 Agent Used Tool: {tool_name}")
                    print(f"📌 Tool Output: {result}")

                    # ---------------- FINAL AI RESPONSE ---------------- #

                    final_response = llm.invoke(
                        f"""
                        User Question:
                        {user_input}

                        Tool Output:
                        {result}

                        Give a short professional response.
                        """
                    )

                    print(f"\n✅ Final Answer: {final_response.content}\n")

            else:

                print(f"\n🤖 Agent: {response.content}\n")

        except Exception as e:

            print(f"\n❌ Error: {e}\n")