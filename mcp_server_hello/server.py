import random
import click
import anyio
import mcp.types as types
from typing import Any
from pydantic import AnyUrl
from mcp.server.lowlevel import Server
from mcp.server.lowlevel.helper_types import ReadResourceContents

# Define constants
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


# Tools
def say_hello(name: str) -> str:
    return f"Hello, {name}!"


def say_bye(name: str) -> str:
    return f"Goodbye, {name}! See you later!"


def give_compliment(name: str) -> str:
    compliment = random.choice(compliments)
    return f"Hey {name}, {compliment}"


def give_roast(name: str) -> str:
    roast = random.choice(roasts)
    return f"Hey {name}, {roast}"


# Prompts
def create_story_messages(
    genre: str | None = None, setting: str | None = None, character: str | None = None
) -> list[types.PromptMessage]:
    messages = []

    genre_part = f" {genre}" if genre else " mystery"
    setting_part = f" set in {setting}" if setting else ""
    character_part = f" featuring {character}" if character else ""

    prompt = f"Write a creative short{genre_part} story{setting_part}{character_part}. Make it engaging with vivid descriptions and an interesting plot twist."

    messages.append(
        types.PromptMessage(
            role="user", content=types.TextContent(type="text", text=prompt)
        )
    )

    return messages


def create_facts_messages(
    topic: str | None = None, style: str | None = None, count: str | None = None
) -> list[types.PromptMessage]:
    messages = []

    topic_part = f" about {topic}" if topic else ""
    count_part = f" {count}" if count else " 5"
    style_part = ""
    if style == "fun":
        style_part = " Present them in a fun and entertaining way."
    elif style == "scientific":
        style_part = " Present them with scientific accuracy and detail."
    elif style == "surprising":
        style_part = " Focus on surprising and lesser-known facts."
    else:
        style_part = " Present them in an interesting and engaging way."

    prompt = f"Provide{count_part} fascinating facts{topic_part}.{style_part} Include sources or context where relevant to make the facts more credible and interesting."

    messages.append(
        types.PromptMessage(
            role="user", content=types.TextContent(type="text", text=prompt)
        )
    )

    return messages


# Define CLI
@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse", "streamable-http"]),
    default="stdio",
    help="Transport type",
)
def main(port: int, transport: str) -> int:

    # Define server
    app = Server("mcp-server-hello")

    # Define tools
    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="hello",
                title="Hello",
                description="Says hello to a person",
                inputSchema={
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the person to greet",
                        }
                    },
                },
            ),
            types.Tool(
                name="bye",
                title="Bye",
                description="Says goodbye to a person",
                inputSchema={
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the person to say goodbye to",
                        }
                    },
                },
            ),
            types.Tool(
                name="compliment",
                title="Compliment",
                description="Gives a random compliment to a person",
                inputSchema={
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the person to compliment",
                        }
                    },
                },
            ),
            types.Tool(
                name="roast",
                title="Roast",
                description="Gives a playful roast to a person",
                inputSchema={
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the person to roast",
                        }
                    },
                },
            ),
        ]

    @app.call_tool()
    async def fetch_tool(
        name: str, arguments: dict[str, Any]
    ) -> list[types.ContentBlock]:
        if name == "hello":
            if "name" not in arguments:
                raise ValueError("Missing name")
            message = say_hello(arguments["name"])
        elif name == "bye":
            if "name" not in arguments:
                raise ValueError("Missing name")
            message = say_bye(arguments["name"])
        elif name == "compliment":
            if "name" not in arguments:
                raise ValueError("Missing name")
            message = give_compliment(arguments["name"])
        elif name == "roast":
            if "name" not in arguments:
                raise ValueError("Missing name")
            message = give_roast(arguments["name"])
        else:
            raise ValueError(f"Unknown tool: {name}")

        return [{"type": "text", "text": message}]

    # Define resources
    @app.list_resources()
    async def list_resources() -> list[types.Resource]:
        return [
            types.Resource(
                uri="jokes://random",
                name="Random Joke",
                description="Get a random joke",
                mimeType="text/plain",
            ),
            types.Resource(
                uri="jokes://all",
                name="All Jokes",
                description="Get all jokes",
                mimeType="application/json",
            ),
        ]

    @app.read_resource()
    async def read_resource(uri: AnyUrl):
        uri_str = str(uri)
        if uri_str == "jokes://random":
            return [
                ReadResourceContents(
                    content=random.choice(jokes), mime_type="text/plain"
                )
            ]
        elif uri_str == "jokes://all":
            import json

            return [
                ReadResourceContents(
                    content=json.dumps(jokes), mime_type="application/json"
                )
            ]
        else:
            raise ValueError(f"Unknown resource: {uri_str}")

    # Define prompts
    @app.list_prompts()
    async def list_prompts() -> list[types.Prompt]:
        return [
            types.Prompt(
                name="story",
                title="Creative Story Generator",
                description="Generate a creative short story with customizable genre, setting, and characters",
                arguments=[
                    types.PromptArgument(
                        name="genre",
                        description="Story genre (mystery, fantasy, sci-fi, romance, horror, etc.)",
                        required=False,
                    ),
                    types.PromptArgument(
                        name="setting",
                        description="Story setting or location",
                        required=False,
                    ),
                    types.PromptArgument(
                        name="character",
                        description="Main character description",
                        required=False,
                    ),
                ],
            ),
            types.Prompt(
                name="facts",
                title="Fascinating Facts Generator",
                description="Generate interesting facts about any topic with customizable style and count",
                arguments=[
                    types.PromptArgument(
                        name="topic",
                        description="Topic to get facts about",
                        required=False,
                    ),
                    types.PromptArgument(
                        name="style",
                        description="Presentation style (fun, scientific, surprising)",
                        required=False,
                    ),
                    types.PromptArgument(
                        name="count",
                        description="Number of facts to generate",
                        required=False,
                    ),
                ],
            ),
        ]

    @app.get_prompt()
    async def get_prompt(
        name: str, arguments: dict[str, str] | None = None
    ) -> types.GetPromptResult:
        arguments = arguments or {}

        if name == "story":
            return types.GetPromptResult(
                messages=create_story_messages(
                    genre=arguments.get("genre"),
                    setting=arguments.get("setting"),
                    character=arguments.get("character"),
                )
            )
        elif name == "facts":
            return types.GetPromptResult(
                messages=create_facts_messages(
                    topic=arguments.get("topic"),
                    style=arguments.get("style"),
                    count=arguments.get("count"),
                )
            )
        else:
            raise ValueError(f"Unknown prompt: {name}")

    # Define server transport
    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.requests import Request
        from starlette.responses import Response
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request: Request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as streams:  # type: ignore[reportPrivateUsage]
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )
            return Response()

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse, methods=["GET"]),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        uvicorn.run(starlette_app, host="127.0.0.1", port=port)
    elif transport == "streamable-http":
        from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
        from starlette.applications import Starlette
        from starlette.middleware.cors import CORSMiddleware
        import contextlib

        # Create session manager
        session_manager = StreamableHTTPSessionManager(app=app)

        # Lifespan context manager
        @contextlib.asynccontextmanager
        async def lifespan(starlette_app: Starlette):
            async with session_manager.run():
                yield

        # Create Starlette application
        starlette_app = Starlette(debug=True, lifespan=lifespan)

        # Add CORS middleware
        starlette_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Create ASGI application wrapper for session manager
        class MCPASGIApp:
            def __init__(self, session_manager):
                self.session_manager = session_manager

            async def __call__(self, scope, receive, send):
                await self.session_manager.handle_request(scope, receive, send)

        # Mount the MCP ASGI app
        mcp_app = MCPASGIApp(session_manager)
        starlette_app.mount("/mcp", mcp_app)

        import uvicorn

        uvicorn.run(starlette_app, host="127.0.0.1", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0
