---
name: ai-product-building-heller
description: Guide for building successful AI startups based on Jake Heller's Casetext journey ($650M exit). Use when users need help with- (1) Selecting AI startup ideas by identifying jobs people pay humans to do, (2) Building reliable AI products through systematic evaluation and prompt iteration, (3) Pricing AI products based on value delivered, (4) Marketing AI products through product quality rather than sales tactics, (5) Understanding the assistance/replacement/unthinkable framework for AI opportunities, (6) Creating evaluation frameworks for AI prompts, or (7) Bridging the trust gap with enterprise customers for AI products.
---

# AI Startup Building Framework

Build successful AI startups by picking ideas based on existing paid work, iterating obsessively on evaluation, and letting product quality drive growth.

## Core Principles

### Job-as-Market Framework

Instead of inventing what people might want, identify what people currently pay other people to do. This eliminates product-market fit risk.

**Key insight**: AI has made finding product-market fit easier—we already know what people want because they're paying humans to do it.

### TAM Expansion

Traditional SaaS: `TAM = software seats × subscription price`

AI products: `TAM = combined salaries of all workers doing the job being replaced/assisted`

This means 10-1000x larger markets than traditional SaaS.

## Idea Selection Workflow

### Step 1: Identify Target Jobs

Look for jobs people are already outsourcing or paying humans to do:

- Customer support representatives
- Insurance adjusters
- Paralegals and legal researchers
- Personal trainers
- Executive assistants
- Data entry clerks
- Content moderators

**Best signal**: Jobs being outsourced to other countries indicate price sensitivity and clear task definition—prime AI targets.

### Step 2: Categorize the Opportunity

Classify your idea into one of three categories:

| Category | Description | Example | Complexity |
|----------|-------------|---------|------------|
| **Assistance** | Help professionals do tasks faster | AI legal research for lawyers | Medium |
| **Replacement** | Become the service provider directly | AI-powered customer support | High |
| **Previously Unthinkable** | Tasks too expensive for humans at scale | Personalized tutoring for every student | Highest |

**Decision guidance**:
- Start with assistance if entering a regulated industry (law, medicine, finance)
- Consider replacement for commoditized services with clear quality metrics
- Pursue unthinkable only with strong technical differentiation

### Step 3: Validate Domain Expertise

You must understand how professionals actually do the work. Ask:

- What are the specific steps in this workflow?
- Where do humans make judgment calls?
- What does "good" look like to an expert?
- What mistakes would be unacceptable?

If you cannot answer these questions, partner with domain experts or spend time learning the profession deeply.

## Building Reliable AI Products

### Workflow Decomposition

Break professional tasks into specific steps. For each step, decide:

```
Is this step deterministic?
├── Yes → Implement as code (no LLM needed)
└── No → Does it require judgment?
    ├── Yes → Create a prompt with evaluation
    └── No → Can it be rule-based?
        ├── Yes → Implement as code
        └── No → Create a prompt with evaluation
```

**Mental model**: Each prompt represents injecting human-level intelligence at a specific decision point.

### Best Expert Framework

Design AI workflows by asking: "How would the best person in this field approach this task if they had unlimited time and 1000 AI instances working simultaneously?"

This reframes constraints—you're not limited by human availability or time pressure.

## Evaluation Framework

### The Eval-Driven Development Process

Most AI products fail because builders stop at 60-70% accuracy demos. Follow this process instead:

#### Phase 1: Initial Development (12 evals per prompt)

1. Write initial prompt
2. Create 12 diverse test cases covering:
   - Common scenarios (6 cases)
   - Edge cases (3 cases)
   - Adversarial inputs (3 cases)
3. Run evaluations
4. Iterate until all 12 pass

#### Phase 2: Expansion (reach 100 evals)

1. Add 10 more test cases after achieving 100% on initial set
2. Identify failure patterns
3. Iterate on prompt until new tests pass
4. Repeat until you have 100 evaluations per prompt

#### Phase 3: Holdout Validation

1. Keep 20% of evaluations as a holdout set
2. Never look at holdout results during development
3. Use holdout only for final validation
4. If holdout fails, return to Phase 2

### Evaluation Criteria

For each test case, define:

```yaml
test_case:
  input: "The specific input to test"
  expected_behavior: "What the output should contain/do"
  failure_conditions:
    - "Specific failure mode 1"
    - "Specific failure mode 2"
  pass_threshold: 0.97  # 97% minimum for production
```

### The Two-Week Grind

**Critical insight**: The willingness to spend two weeks sleeplessly iterating on a single prompt separates successful products from demos.

When accuracy matters (finance, medicine, law):
- Block two weeks for prompt refinement
- Accept no compromises below 97% accuracy
- Document every iteration and why it failed

### Converting Complaints to Tests

Post-beta launch workflow:

1. Receive customer complaint
2. Reproduce the issue
3. Create new test case capturing the failure
4. Add to evaluation suite
5. Iterate until test passes
6. Verify no regression on existing tests

Real user behavior is your best evaluation source.

## Pricing AI Products

### Value-Based Pricing

Price based on value delivered, not SaaS conventions:

```
AI Product Price = (Human cost for equivalent work) × (0.1 to 0.5)
```

**Example**: If a paralegal costs $50/hour and takes 4 hours for research ($200 total), price AI at $20-100 per equivalent task.

### Discovery Process

Ask customers directly: "How would you like to pay for this?"

Common models:
- Per-task pricing (for discrete, measurable outputs)
- Seat-based (for ongoing assistance tools)
- Usage-based (for variable consumption patterns)
- Outcome-based (for replacement products)

### Avoiding PRR Trap

**Pilot Recurring Revenue (PRR)**: Revenue from pilot programs that may not convert to real ARR.

Warning signs:
- Pilots that keep extending without conversion
- Usage metrics that don't match payment
- Customers who praise but don't deploy

Focus on actual customer adoption and usage, not pilot revenue.

## Marketing and Sales

### Product-is-Everything Principle

Your product isn't just pixels on screen—it includes:
- Customer support quality
- Onboarding experience
- Training materials
- Customer success interactions
- Founder involvement in early deals

Great products generate word-of-mouth. Product quality drives marketing success more than marketing investment.

### Bridging the Trust Gap

Enterprise buyers face uncertainty moving from controllable humans (trainable, fireable) to unknown AI.

**Trust-building tactics**:

1. **Side-by-side comparisons**: Offer head-to-head tests against existing human services during pilots
2. **Controlled pilots**: Let customers test with real work in controlled environment
3. **Published studies**: Create case studies with measurable outcomes
4. **Gradual rollout**: Start with low-risk tasks, expand as trust builds

### Forward Deployed Engineers

For enterprise customers, place engineers who sit with customers to:
- Ensure products work in their specific environment
- Gather real feedback on failure modes
- Build relationship and trust
- Identify expansion opportunities

## Building Defensibility

Defensibility comes from accumulated iteration complexity, not proprietary models.

Sources of defensibility:
- Thousands of evaluations refined over years
- Deep understanding of domain-specific edge cases
- Integrated workflows that are painful to switch
- Brand trust built through consistent quality
- Data flywheel from customer usage

## Common Mistakes to Avoid

| Mistake | Why It Fails | Better Approach |
|---------|--------------|-----------------|
| Stopping at 70% accuracy | Unusable for professional work | Iterate until 97%+ |
| Using agent frameworks without understanding | Adds complexity without reliability | Build simple, testable pipelines |
| Over-investing in sales vs. product | Unsustainable growth | Let product quality drive growth |
| Pricing like SaaS | Leaves value on table | Price based on human cost replacement |
| Ignoring domain expertise | Miss critical failure modes | Partner with or become domain experts |
| Counting PRR as real revenue | Inflates metrics, hides problems | Track actual deployment and usage |

## Quick Reference: Evaluation Tools

**Promptfoo** (open source, command line):
- Run batch evaluations
- Compare prompt versions
- Track regression over time

Basic usage pattern:
```bash
promptfoo eval --config eval_config.yaml
```

Structure evaluations in YAML with inputs, expected outputs, and grading criteria.