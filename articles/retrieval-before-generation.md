# Retrieval before generation

Prepared for Anish Babu Nudurupati · AI-assisted editorial draft for author review · September 2026

A citation is a starting point for verification, not a guarantee of correctness.

## Make evidence inspectable

For a document assistant, I want to see the evidence before judging the prose. If the relevant passage never reaches the model, a better-sounding answer is not a reliable improvement. EvidenceDesk begins with retrieval, source identifiers and an explicit no-match response. The browser demo exposes that first step instead of disguising a lookup as a live model conversation.

## Choose an honest baseline

The implementation splits documents into overlapping word chunks and ranks them using weighted word matches. It is lexical retrieval, not a vector database. OpenAI’s retrieval documentation describes semantic search using embeddings, which can surface relevant passages even with few shared words. That distinction matters: the baseline is easy to inspect and run, but can miss paraphrases. I would compare it against a semantic retriever on the same evaluation questions before claiming one is better for this dataset.

## Separate search from synthesis

Without a model, EvidenceDesk returns matching excerpts with source IDs. With a locally installed model, it constructs a prompt containing only the selected evidence and asks for citations. The answer is then checked for citation IDs absent from the evidence set. A made-up ID is an observable failure. A valid ID attached to an unsupported claim can still pass, so the UI does not equate citation validity with factual correctness.

## An evaluation I can explain

The current automated tests cover relevant-source selection, empty questions, chunk coverage, no-match abstention and unknown citation detection. Model outputs are mocked in boundary tests; these are not model-quality benchmarks. A useful next dataset would contain answerable questions, paraphrases, ambiguous questions and questions absent from the documents. I would label the expected source for each answerable question and separately review whether the generated answer follows from it.

## Small datasets expose tradeoffs

Try “streetlight pole intersection” in the lab, then ask about an unrelated subject. The first should surface the report-details passage; the second should abstain. Now try an indirect paraphrase and observe where word matching becomes fragile. That failure is useful because it points to a specific next experiment. Before calling this a production RAG service, I would need access-aware retrieval, document freshness handling, broader evaluation and live-model evidence. Today it is a reproducible learning project with visible limits.

## Sources

- [OpenAI: Retrieval](https://developers.openai.com/api/docs/guides/retrieval)
