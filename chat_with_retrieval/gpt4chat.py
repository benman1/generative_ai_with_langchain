"""GPT4 Chat interface.

Only implemented limited functionality for local models, not the API.
"""
import os
import pathlib
from typing import Dict, Optional, List, Any

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import GPT4All
from langchain.callbacks.manager import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain.chat_models.base import BaseChatModel
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage, AIMessage, ChatResult, ChatGeneration
from pydantic import root_validator, Field


class GPT4AllChat(BaseChatModel):
    model: str = Field(default="orca-mini-3b.ggmlv3.q4_0.bin", alias="model")
    # os.path.join(pathlib.Path.home(), ".cache", "gpt4all")
    model_path: str = "/Users/ben/Downloads/"
    temperature: float = 0.7
    streaming: bool = False
    max_tokens: int = 200
    top_k: int = 40
    top_p: float = 0.1
    repeat_penalty: float = 1.18
    n_threads: int = 8
    llm: Any = None  #: :meta private

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that python package exists in environment."""
        try:
            import gpt4all

        except ImportError:
            raise ValueError(
                "Could not import gpt4all python package. "
                "Please install it with `pip install gpt4all`."
            )
        return values

    def __init__(
            self,
            model: str = "/Users/ben/Downloads/orca-mini-3b.ggmlv3.q4_0.bin",
            n_threads: int = 8,
            temperature: float = 0.7,
            streaming: bool = False,
            max_tokens: int = 200,
            top_k: int = 40,
            top_p: float = 0.1,
            repeat_penalty: float = 1.18,
            **kwargs: Any
    ):
        super().__init__(**kwargs)
        """
        os.path.join(
            pathlib.Path.home(),
            ".cache", "gpt4all",
            "orca-mini-3b.ggmlv3.q4_0.bin"
        ),
        :param model:
        :param model_path:
        :param temperature:
        :param streaming:
        :param max_tokens:
        :param top_k:
        :param top_p:
        :param repeat_penalty:
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.n_threads = n_threads
        self.repeat_penalty = repeat_penalty
        self.top_p = top_p
        self.top_k = top_k
        self.max_tokens = max_tokens
        self.streaming = streaming
        self.temperature = temperature
        self.llm = GPT4All(
            model=model, n_threads=n_threads
        )

    @property
    def _default_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling JinaChat API."""
        return {
            "max_tokens": self.max_tokens,
            "streaming": self.streaming,
            "temp": self.temperature,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "repeat_penalty": self.repeat_penalty
        }

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None,
                  run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> ChatResult:
        message_dicts, params = self._create_message_dicts(messages, stop)
        params = {**params, **kwargs}
        if self.streaming:
            inner_completion = ""
            role = "assistant"
            params["stream"] = True
            function_call: Optional[dict] = None
            for stream_resp in self.completion_with_retry(
                messages=message_dicts, **params
            ):
                role = stream_resp["choices"][0]["delta"].get("role", role)
                token = stream_resp["choices"][0]["delta"].get("content") or ""
                inner_completion += token
                _function_call = stream_resp["choices"][0]["delta"].get("function_call")
                if _function_call:
                    if function_call is None:
                        function_call = _function_call
                    else:
                        function_call["arguments"] += _function_call["arguments"]
                if run_manager:
                    run_manager.on_llm_new_token(token)
            message = _convert_dict_to_message(
                {
                    "content": inner_completion,
                    "role": role,
                    "function_call": function_call,
                }
            )
            return ChatResult(generations=[ChatGeneration(message=message)])
        response = self.completion_with_retry(messages=message_dicts, **params)
        return self._create_chat_result(response)
    async def _agenerate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None,
                         run_manager: Optional[AsyncCallbackManagerForLLMRun] = None, **kwargs: Any) -> ChatResult:
        pass

    @property
    def _llm_type(self) -> str:
        return "gpt4all-chat"

    @property
    def lc_serializable(self) -> bool:
        return True


if __name__ == "__main__":
    chat_openai = ChatOpenAI()
    chat_openai.generate()
    #chat = GPT4AllChat()
    #chat.generate("What is the capital of France?")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    # Setup LLM and QA chain

    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo", temperature=0, streaming=True
    )
    # Passing in a max_tokens_limit amount automatically
    # truncates the tokens when prompting your llm!
    LLMChain(
        llm, retriever=retriever, memory=memory, verbose=True, max_tokens_limit=4000
    )
