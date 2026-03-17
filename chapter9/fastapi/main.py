"""FastAPI webapp."""
import asyncio
import logging
import json
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from langchain_classic.callbacks import AsyncIteratorCallbackHandler
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from config import set_environment
set_environment()

# Initialize FastAPI app
app = FastAPI()

# Setup templates and static files
templates = Jinja2Templates(directory="chapter9/fastapi/templates")
app.mount("/static", StaticFiles(directory="chapter9/fastapi/static"), name="static")

# Initialize a non-streaming LLM for the regular API endpoints
regular_llm = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    temperature=0
)

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chat endpoint
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    if not user_message:
        return {"response": "No message provided"}

    # Create the messages for the LLM
    messages = [HumanMessage(content=user_message)]
    response = regular_llm.invoke(messages)
    return {"response": response.content}

# WebSocket for streaming responses
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Create a new callback handler for each request
            callback_handler = AsyncIteratorCallbackHandler()

            # Receive message from client
            data = await websocket.receive_text()
            logger.info(f"Received WebSocket data: {repr(data)}")

            # Extract user message
            try:
                parsed_data = json.loads(data)
                user_message = parsed_data.get("message", "")
            except json.JSONDecodeError:
                user_message = data

            if not user_message:
                await websocket.send_json({
                    "sender": "bot",
                    "message_type": "error",
                    "message": "No message provided"
                })
                continue

            # Start notification
            await websocket.send_json({
                "sender": "bot",
                "message_type": "start"
            })

            # Create a streaming model instance with the callback handler for this specific request
            streaming_llm = ChatAnthropic(
                model="claude-sonnet-4-6",
                temperature=0,
                callbacks=[callback_handler],
                streaming=True,
            )

            # Start generation in a background task
            async def generate_response():
                messages = [HumanMessage(content=user_message)]
                await streaming_llm.ainvoke(messages)

            task = asyncio.create_task(generate_response())

            # Stream the response pieces as they become available
            async for token in callback_handler.aiter():
                await websocket.send_json({
                    "sender": "bot",
                    "message_type": "stream",
                    "message": token
                })

            # Ensure the task is complete
            await task

            # Send completion notification
            await websocket.send_json({
                "sender": "bot",
                "message_type": "end"
            })

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error in WebSocket: {str(e)}", exc_info=True)
        await websocket.send_json({
            "sender": "bot",
            "message_type": "error",
            "message": f"Error: {str(e)}"
        })

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)