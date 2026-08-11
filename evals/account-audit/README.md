# Account Audit Benchmark

`benchmark.yaml` is the first end-to-end evaluation set for the Reference Skill.

It intentionally includes:

1. Healthy account / PASS
2. Broken measurement + fragmentation / FAIL
3. Incomplete export / INSUFFICIENT_EVIDENCE
4. Contextually justified fragmentation / FALSE_POSITIVE

The benchmark is a deterministic contract test first. Model wording, explanation quality, and recommendation ranking should be evaluated in a later model-evaluation layer.
