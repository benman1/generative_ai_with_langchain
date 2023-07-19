"""summarization prompts.

This is inspired by https://github.com/daveshap/Quickly_Extract_Science_Papers
"""

SUMMARY = (
    "Give me a clear explanation of the objectives, core assertions, implications, "
    "and mechanics elucidated in this text - remove citations! \n"
    " {text} \n"
)

HIGH_LEVEL = (
    "Please explain the value of this text in basic terms like you're "
    "talking to a CEO. So what? What's the bottom line here?\n"
    "{text}\n"
)

ANALOGY = (
    "Please give me an analogy or metaphor that will help explain this text "
    "to a broad audience!\n"
    "{text}\n"
)
