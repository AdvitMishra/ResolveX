# ResolveX room rules

Sample incident:
- Title: Checkout applies shipping to eligible orders
- Expected: subtotal >= INR 500 has zero shipping.
- Actual: checkout adds INR 49 even at INR 500 and above.
- Impact: incorrect displayed order total in the isolated demo service.

Workflow: human report -> @triage classifies -> @fix reproduces and investigates -> @fix proposes minimal patch and runs tests -> human approver reviews diff and exact output.

Safety: use only the isolated sample repository; never share secrets or customer data; paste actual command output; do not merge, open PRs, release or deploy without explicit human approval. Keep `auto_approve: false`.
