# Evaluate the stack

You need separate evidence for parser compatibility, task completion, writing quality, and action approval.
A passing unit test does not establish a model's success rate.

## Record the test conditions

Record the model identifier, provider, CLI version, tool revisions, prompt, configuration, and test date.
Keep credentials and private transcripts out of shared fixtures.
Preserve the source format when you replace transcript content with synthetic text.

## Run offline regressions

Run each repository's documented tests before comparing models.
Use temporary databases and fixture roots. Do not harvest your personal history for a public test.

| Failure | Expected check |
|---|---|
| A second project disappears from capture | Discovery lists every configured project and imports both sessions. |
| A transcript resumes | A second harvest adds new records without duplicating existing records. |
| Two providers use the same session identifier | Both records remain separately addressable. |
| A source is absent or unreadable | Coverage reports the gap. Zero imported records does not mean complete capture. |
| An old event appears in a recently modified file | Usage excludes it from the selected time window. |
| A cumulative usage snapshot repeats | Usage does not count the same tokens twice. |
| A process remains alive after a failed task | The monitor reports a process observation, not task success. |
| An agent claims it writes a file, but the file is absent | Completion remains unverified or fails the declared check. |
| A receipt is stale or the source revision changes | Completion does not pass that evidence check. |
| A request matches two domains | Routing reports ambiguity and loads no context body. |
| Fluent text contains an incorrect claim | A writing score does not become a factuality verdict. |

The ledger, monitor, skills, and Owned Record repositories contain the corresponding implementation tests.
Observer's tests cover writing rules and supported parser examples. Its README states current daemon ingestion limits.

## Compare models

1. Choose a small set of tasks with observable results.
2. Freeze the task inputs and acceptance checks before running either model.
3. Give both models equivalent tools, permissions, and relevant context.
4. Run several independent trials per task and model.
5. Preserve each trace and verify the resulting artifacts.
6. Report successes, failures, missing evidence, latency, and recorded token usage.
7. Review disagreements between automated checks and human judgment.

Record both the numerator and denominator for every reported rate.
Keep incomplete runs in the results with a stated reason.
Do not silently remove a run because a provider or tool fails.
Report cache accounting by provider. Recorded token counts do not establish billing or remaining subscription allowance.

## Calibrate your checks

A false pass accepts an outcome that fails your stated requirement.
A false block rejects an outcome that meets it.
Use human-labeled examples to estimate both. Keep the labels separate from model-written explanations.

Use deterministic checks for exact facts such as file hashes and schema fields.
Use a separate reviewer for judgments that need context, and record the review criteria.
A reviewer verdict does not establish deployment, destination acceptance, or authorization.

## Current evidence boundary

This pass provides synthetic compatibility and regression checks. It does not provide a comparative Astra/Fable model benchmark.
The local completion helper checks declared workspace artifacts. You need destination-specific adapters to verify external outcomes.
You must enforce authorization in the executing tool or service.

## References

- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Claude Code monitoring](https://code.claude.com/docs/en/monitoring-usage)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks-guide)
