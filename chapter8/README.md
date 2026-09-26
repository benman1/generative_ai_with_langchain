# Chapter 8 - Evaluation and Testing

Code for chapter 8 of *Generative AI with LangChain and LangGraph*, third
edition. Targets **LangChain v1** (`langchain>=1.3`, `langgraph>=1.2`), same as
chapter 4. `langchain.evaluation` and `langchain.smith` don't exist in the base
`langchain` package anymore; both moved intact to the separate
`langchain-classic` package, which `pip install langchain` does not pull in.

## Setup

```bash
pip install -r requirements.txt
```

**No paid API key is needed for most of this.** Every notebook builds on the
Meridian corpus and evaluation set from `../chapter4` (run
`python ../chapter4/build_corpus.py` once if you haven't already), and every
retrieval, deterministic-check, and offline-math cell runs with no key set.

The RAGAS `Faithfulness` cell in `advanced_evaluation.ipynb` runs a real judge
call for free: `ollama pull LiquidAI/lfm2.5-1.2b-instruct` (under 1GB) and
`ollama serve`, and the cell finds it automatically over Ollama's
OpenAI-compatible local endpoint. It falls back to `OPENAI_API_KEY` if Ollama
isn't running, and to a plain skip message if neither is available; it never
prints an invented score. The `labeled_score_string`, `criteria`, and `cot_qa`
cells in `basic_evaluators.ipynb` still fall back to `FakeListChatModel`, a
labeled, canned stand-in, not yet wired to try Ollama the same way; the
structured-extraction cell falls back to a plain canned record instead, since
`FakeListChatModel` doesn't support `.with_structured_output()`. Set
`LANGSMITH_API_KEY` to actually create a dataset and run an evaluation rather
than see what it would have done.

## Notebooks

| Notebook | What it covers |
|---|---|
| [basic_evaluators.ipynb](basic_evaluators.ipynb) | Deterministic checks (`ExactMatchStringEvaluator`, `JsonValidityEvaluator`); hit@k vs. recall@k on the real evaluation set; the word-overlap/embedding-similarity negation experiment; the `langchain_classic.evaluation` judge evaluators (`labeled_score_string`, `criteria`, `cot_qa`); structured extraction with `.with_structured_output()`; and `pass@k` for code generation |
| [advanced_evaluation.ipynb](advanced_evaluation.ipynb) | A live check of whether `ragas` imports cleanly under this chapter's pinned `langchain-community==0.3.30` (it does, and the cell explains the version-drift bug that pin works around), a `Faithfulness` scoring call against the real Meridian baggage documents, a from-scratch reimplementation of the same faithfulness check with no RAGAS dependency at all, a bootstrapped confidence interval over judge scores, a conformal-prediction interval from a judge's own token log-probabilities (no resampling needed), the `StateGraph` wiring for chapter 4's itinerary assistant rebuilt with stand-in nodes to confirm its topology, and trajectory checks (`check_trajectory`, `check_policy`) applied to traces shaped like that graph |
| [langsmith_evaluation.ipynb](langsmith_evaluation.ipynb) | Extends chapter 4's twenty-question Meridian evaluation set with staleness and leakage trap questions, evaluates a small retrieval-and-answer function against it, uploads/runs the set through the current `langsmith` SDK (`Client.create_dataset`, `Client.evaluate`), and runs a trajectory evaluation with the same `(inputs, outputs, reference_outputs)` evaluator shape |

Every numbered listing in the chapter is a cell in one of these. All three are
committed with their outputs from a run with no API keys set, so you can read
the numbers without running anything; setting `OPENAI_API_KEY` and
`LANGSMITH_API_KEY` unlocks the gated sections across all three notebooks.

## Code from the second edition

The three notebooks previously here (`ChatMistralAI` + `ScoreStringEvalChain`,
`.bind_functions()`, `langchain.smith.run_on_dataset`) targeted LangChain 0.3
and are superseded by the ones above. They have not been removed from history;
check out the
[`second_edition`](https://github.com/benman1/generative_ai_with_langchain/tree/second_edition)
branch if you want them. They will not run on v1.
