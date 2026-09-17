# From a user message to a system action

Prepared for Anish Babu Nudurupati · AI-assisted editorial draft for author review · September 2026

The model proposes. The application decides what is allowed to happen.

## Think in layers

A chat interface feels like a single conversation, but an application has several responsibilities. It assembles context, requests a model response, validates returned data, runs permitted operations and presents a result. My design question is where each responsibility belongs. A persuasive sentence from a model should not be enough to make an irreversible change.

## Roles describe where instructions come from

In OpenAI text-generation requests, developer instructions take priority over user messages, and model-generated messages have the assistant role. The documentation also notes that instructions are not automatically carried forward when continuing with previous_response_id. Application code therefore needs to manage its instruction context deliberately. A retrieved page or uploaded report is evidence to process, not a new source of application permissions.

## Tool calling is a conversation with code

The documented function-calling flow is a loop: offer tools, receive a requested call, execute application code, return the result, and request a continuation. The model’s call describes a proposed operation; the application still owns execution. A returned tool result is then more context for the model. This helps explain why “the assistant said it did something” and “the system recorded a successful action” are different claims.

## CivicFlow makes the boundary tangible

CivicFlow accepts a report, proposes a category and summary, and stops at needs_review. In baseline mode the proposal comes from simple rules. In optional local-model mode it comes from a JSON response. Both paths pass through the same application checks. Only four categories are permitted, the summary is bounded, and a separate approval command is required before writing a local outbox record. Nothing in a report can supply the approval flag.

## Test the boundary, not the tone

The tests intentionally substitute malformed model output and an unsupported category. They also check that a valid model proposal still needs review, and that approving the same report twice does not create two records. These checks establish properties of this implementation; they do not prove a language model is immune to prompt injection. For a deployed service I would add authenticated reviewers, request identity, audit storage and a clear retry policy. The current project is a bounded workflow prototype, not a municipal integration.

## Sources

- [OpenAI: Text generation](https://developers.openai.com/api/docs/guides/text)
- [OpenAI: Function calling](https://developers.openai.com/api/docs/guides/function-calling)
