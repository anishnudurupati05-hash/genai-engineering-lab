# Tokens are an engineering budget

Prepared for Anish Babu Nudurupati · AI-assisted editorial draft for author review · September 2026

Why I separate the text I can count from the request I actually send.

## Start with the whole request

A token budget is a design constraint. A useful assistant has to carry instructions, a user question, selected evidence, conversation history and room for an answer. I find it helpful to account for those pieces separately before choosing what to remove. A short visible question can still sit inside a large request.

## Text counts and request counts

A tokenizer maps text into model-specific units; a token is not reliably one word or one character. OpenAI distinguishes local plain-text tokenization from full-request counting. Tool schemas, files, images and message structure can change the total. Its input-token counting endpoint accepts the request structure before generation. These are different measurements, and the interface should say which one it shows.

## A small experiment worth repeating

ContextLab starts with an intentionally rough estimate: UTF-8 bytes divided by four, rounded up. Try an English paragraph, then code, then a sentence in another language. Watch the estimate change. This is a demonstration of a heuristic, not evidence of how a particular model tokenizes that text. The Python version can instead use an explicit tiktoken encoding and return actual token IDs for plain text. Comparing the two makes approximation error visible.

## Reserve output before filling the window

The lab computes remaining capacity as context limit minus estimated input, manual overhead and reserved output. For example, a hypothetical 8,192-token budget with 3,000 input tokens, 200 overhead tokens and a 1,024-token output reserve leaves 3,968 tokens. These are scenario inputs, not the advertised limits of any named model. A negative result should prompt a decision: retrieve less, shorten history, reduce the output requirement or select a suitable context limit.

## Cost is a scenario, quality needs an evaluation

The calculator multiplies input and reserved output by user-supplied rates. It does not quote current prices or predict an invoice. A smaller prompt may cost less, but it can also remove the only evidence needed to answer correctly. My proposed next experiment is to run the same question set at several evidence budgets and record answer support, abstentions and actual usage. Those results have not been collected yet; the lab is the starting point for collecting them.

## Sources

- [OpenAI: Counting tokens](https://developers.openai.com/api/docs/guides/token-counting)
