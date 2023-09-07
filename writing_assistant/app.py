"""Writing assistent.

Run like this:
>> gradio writing_assistant/app.py."""
import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

from config import set_environment


set_environment()

LLM = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.,
)
MISSION = "You are a helpful assistant that can fix and improve writing in terms of" \
          " style, punctuation, grammar, vocabulary, and orthography so that it looks like something" \
          " that a native speaker would write."

PREFIX = "Give feedback on incorrect spelling, grammar, and expressions of the text" \
         " below. Check the tense consistency. Explain grammar rules and examples for" \
         " grammar rules. Give hints so the text becomes more concise and engrossing.\n" \
         "Text: {text}." \
         "" \
         "Feedback: "


def suggest_improvements(input: str, temperature: float) -> str:
    """Suggest improvements to the text."""
    messages = [
        SystemMessage(
            content=MISSION
        ),
        HumanMessage(
            content=PREFIX.format(text=input)
        ),
    ]
    output = LLM(messages, temperature=temperature).content
    return output


demo = gr.Interface(
    fn=suggest_improvements,
    inputs=["text", gr.Slider(0., 1.0, label="Temperature")],
    outputs=["text"],
)
with demo:
    gr.HTML(
        "<center>Powered by <a href='https://github.com/langchain_ai/langchain'>LangChain 🦜️🔗</a></center>"
    )

demo.launch()
