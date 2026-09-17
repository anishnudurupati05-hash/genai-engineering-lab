# GenAI Engineering Lab

Three runnable learning projects for Anish Babu Nudurupati's portfolio. Newly built with AI assistance; these are learning implementations, not claims of historical client work or production deployment.

| Project | What runs now | Optional model path |
| --- | --- | --- |
| EvidenceDesk | Word chunking, lexical ranking, source excerpts and abstention | Local Ollama synthesis with citation-ID validation |
| ContextLab | Context budgets, explicit rough estimates, configurable cost scenarios | Exact text encoding with tiktoken |
| CivicFlow | Rule-based triage, human approval gate, SQLite outbox and deduplication | Local Ollama category/summary proposals |

The portfolio's browser lab is an interactive offline baseline. It does not call an LLM. The Python model paths call only an already-running Ollama server on `127.0.0.1:11434`. No models are downloaded and no paid APIs are invoked automatically.

## Quick start

Python 3.10+; no packages needed for baseline mode. From this repository directory:

```sh
python3 evidence_desk.py "What belongs in a streetlight report?"
python3 context_lab.py "You are a helpful assistant." --context 8192 --reserve 1024
python3 civic_agent.py triage "Blocked wheelchair ramp near the library" > proposal.json
```

Read `proposal.json` before explicitly approving it:

```sh
python3 civic_agent.py approve proposal.json --approve
python3 -m unittest discover -s tests -v
```

Approval writes to a local SQLite outbox. It sends nothing to a government agency. Running approval twice for identical normalized report text creates only one record. Editing a summary does not create a new record for the same report; this prototype does not provide an update workflow.

## Local LLM mode

Install and run Ollama separately using its official documentation, then choose a model appropriate for your hardware. Replace `YOUR_INSTALLED_MODEL` with the name of a model already present:

```sh
python3 evidence_desk.py "What belongs in a streetlight report?" --model YOUR_INSTALLED_MODEL
python3 civic_agent.py triage "Broken light on Oak Avenue" --model YOUR_INSTALLED_MODEL
```

The adapter uses `/api/generate`, a separate system prompt, non-streaming JSON responses, a 90-second timeout and bounded output. CivicFlow validates model output before it reaches the review gate. Errors are reported rather than silently replaced with a fabricated model answer. Live model quality has not been benchmarked; automated tests mock model responses to test the application boundary.

## Exact text tokenization

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-optional.txt
.venv/bin/python context_lab.py "Hello, world!" --encoding cl100k_base
```

A tokenizer may download its vocabulary on first use. This counts plain text for an explicitly selected encoding, not the complete API request. The default estimate is UTF-8 bytes divided by four, rounded up. It is deliberately labeled approximate and is unreliable across languages. Supply current rates and context limits yourself; none are presented as model pricing.

## Architecture and tradeoffs

EvidenceDesk uses overlapping word chunks and a simple inverse-document-frequency weighted lexical score. This keeps retrieval explainable and dependency-free; it misses paraphrases and is not embedding search. The optional generator sees only retrieved evidence. Citation validation confirms IDs exist, not that every generated claim is supported. Evaluate entailment separately.

CivicFlow is a fixed, bounded workflow rather than an open-ended autonomous agent. The model may propose two fields, never arbitrary tool names or SQL. Approval occurs outside model control. Hash-based deduplication handles exact normalized duplicates, not reports that mean the same thing in different words. A real deployment needs authenticated reviewers, durable job handling, audit retention, municipal integration, and privacy controls.

ContextLab separates text count, manually supplied framing overhead, reserved output and price inputs. Its cost is a scenario based on the output reserve, not an invoice. Cached tokens, reasoning tokens, tools and modality-specific accounting are out of scope.

## Learning notes

The articles in `articles/` are AI-assisted editorial drafts prepared for Anish's review. They make no claims about unrecorded course exercises or measured production outcomes. The six-month course context was supplied by the portfolio owner; provider, dates and certificate details remain unspecified.

## References

- [OpenAI: token counting](https://developers.openai.com/api/docs/guides/token-counting)
- [OpenAI: text generation and message roles](https://developers.openai.com/api/docs/guides/text)
- [OpenAI: function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI: retrieval](https://developers.openai.com/api/docs/guides/retrieval)
- [Ollama: generate API](https://docs.ollama.com/api/generate)
