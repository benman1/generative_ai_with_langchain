"""LLM Webserver with Flask and Lanarky.
Adapted from https://github.com/ajndkr/lanarky/blob/main/examples/app/conversation_chain.py
"""
from config import set_environment
from fastapi import FastAPI
from lanarky import LangchainRouter
from langchain.chains import ConversationChain
from langchain_openai.chat_models import ChatOpenAI
from starlette.requests import Request
from starlette.templating import Jinja2Templates

set_environment()

app = FastAPI()


def create_chain():
    return ConversationChain(
        llm=ChatOpenAI(
            temperature=0,
            streaming=True,
        ),
        verbose=True,
    )


templates = Jinja2Templates(directory="webserver/templates")
chain = create_chain()


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


langchain_router = LangchainRouter(langchain_url="/chat", langchain_object=chain, streaming_mode=1)
langchain_router.add_langchain_api_route("/chat_json", langchain_object=chain, streaming_mode=2)
langchain_router.add_langchain_api_websocket_route("/ws", langchain_object=chain)

app.include_router(langchain_router)
