"""LLM Webserver with Flask and Lanarky.
Adapted from https://github.com/ajndkr/lanarky/blob/main/examples/app/conversation_chain.py
"""
from fastapi import FastAPI
from lanarky.testing import mount_gradio_app
from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI

from lanarky import LangchainRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from config import set_environment

set_environment()


def create_chain():
    return ConversationChain(
        llm=ChatOpenAI(
            temperature=0,
            streaming=True,
        ),
        verbose=True,
    )


app = mount_gradio_app(FastAPI(title="ConversationChainDemo"))
templates = Jinja2Templates(directory="webserver/templates")
chain = create_chain()


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


langchain_router = LangchainRouter(
    langchain_url="/chat", langchain_object=chain, streaming_mode=1
)
langchain_router.add_langchain_api_route(
    "/chat_json", langchain_object=chain, streaming_mode=2
)
langchain_router.add_langchain_api_websocket_route("/ws", langchain_object=chain)

app.include_router(langchain_router)
