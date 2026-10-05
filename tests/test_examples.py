import json
from pathlib import Path
import unittest

EXAMPLES = Path(__file__).resolve().parents[1] / 'examples'


def records(name):
    return [json.loads(line) for line in (EXAMPLES / name).read_text().splitlines() if line]


class FixtureContractTests(unittest.TestCase):
    def test_provider_collision_is_deliberate(self):
        claude = records('claude-session.jsonl')
        codex = records('codex-session.jsonl')
        self.assertEqual(claude[0]['sessionId'], codex[0]['payload']['id'])
        self.assertEqual(claude[0]['cwd'], '/workspace/demo')
        self.assertEqual(codex[0]['payload']['cwd'], '/workspace/demo')

    def test_claude_usage_preserves_cache_as_separate_fields(self):
        usage = records('claude-session.jsonl')[1]['message']['usage']
        self.assertEqual(usage, {'input_tokens': 100, 'output_tokens': 12,
                                'cache_read_input_tokens': 20, 'cache_creation_input_tokens': 0})

    def test_codex_mirror_and_tool_correlation_are_preserved(self):
        data = records('codex-session.jsonl')
        payloads = [r['payload'] for r in data]
        call = next(p for p in payloads if p.get('type') == 'function_call')
        output = next(p for p in payloads if p.get('type') == 'function_call_output')
        self.assertEqual(call['call_id'], output['call_id'])
        answer = next(p for p in payloads if p.get('type') == 'message' and p['role'] == 'assistant')
        mirror = next(p for p in payloads if p.get('type') == 'agent_message')
        self.assertEqual(answer['content'][0]['text'], mirror['message'])

    def test_codex_usage_subsets_are_not_extra_tokens(self):
        usage = records('codex-session.jsonl')[-1]['payload']['info']['total_token_usage']
        self.assertEqual((usage['input_tokens'], usage['output_tokens'], usage['total_tokens']), (80, 10, 90))
        self.assertLessEqual(usage['cached_input_tokens'], usage['input_tokens'])
        self.assertLessEqual(usage['reasoning_output_tokens'], usage['output_tokens'])


if __name__ == '__main__':
    unittest.main()
