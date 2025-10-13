import random
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mcp-server-hello")

jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "What do you call fake spaghetti? An impasta!",
]

compliments = [
    "You're doing an amazing job!",
    "You have a great sense of humor!",
    "You're incredibly talented!",
]

roasts = [
    "Your code runs... eventually.",
    "I've seen turtles debug faster.",
    "Did you just console.log a secret? Bold move.",
]

@mcp.tool("hello")
def say_hello(name: str) -> str:
    """
    Greet the user
    Args:
        name (str): The name of the user
    Returns:
        str: A greeting message
    """
    return f"Hello, {name}!"

@mcp.tool("compliment")
def give_compliment(name: str) -> str:
    """
    Give a random compliment to the user
    Args:
        name (str): The name of the user
    Returns:
        str: A compliment message
    """
    compliment = random.choice(compliments)
    return f"Hey {name}, {compliment}"

@mcp.tool("roast")
def give_roast(name: str) -> str:
    """
    Give a playful roast to the user
    Args:
        name (str): The name of the user
    Returns:
        str: A roast message
    """
    roast = random.choice(roasts)
    return f"Hey {name}, {roast}"

@mcp.resource("jokes://random")
def get_joke() -> str:
    """
    Get a random joke
    Returns:
        str: A random joke
    """
    return random.choice(jokes)

@mcp.resource("jokes://all")
def get_all_jokes() -> list[str]:
    """
    Get all jokes
    Returns:
        list[str]: A list of jokes
    """
    return jokes

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')