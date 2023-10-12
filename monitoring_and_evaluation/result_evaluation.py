"""Evaluate a result from an agent execution.

by calculating the embedding distance to an expected output (a reference).
"""
from langchain.evaluation import load_evaluator
from config import set_environment

set_environment()
# evaluator = load_evaluator("embedding_distance")
#
# print(evaluator.evaluate_strings(prediction="I shall go", reference="I shan't go"))
#
#
# evaluator = load_evaluator("labeled_pairwise_string")
#
# print(evaluator.evaluate_string_pairs(
#     prediction="there are three dogs",
#     prediction_b="4",
#     input="how many dogs are in the park?",
#     reference="four",
# ))

custom_criteria = {
    "simplicity": "Is the language straightforward and unpretentious?",
    "clarity": "Are the sentences clear and easy to understand?",
    "precision": "Is the writing precise, with no unnecessary words or details?",
    "truthfulness": "Does the writing feel honest and sincere?",
    "subtext": "Does the writing suggest deeper meanings or themes?",
}
evaluator = load_evaluator("pairwise_string", criteria=custom_criteria)

print(evaluator.evaluate_string_pairs(
    prediction="Every cheerful household shares a similar rhythm of joy; but sorrow, in each household, plays a unique, haunting melody.",
    prediction_b="Where one finds a symphony of joy, every domicile of happiness resounds in harmonious,"
    " identical notes; yet, every abode of despair conducts a dissonant orchestra, each"
    " playing an elegy of grief that is peculiar and profound to its own existence.",
    input="Write some prose about families.",
))






if __name__ == "__main__":
    pass

