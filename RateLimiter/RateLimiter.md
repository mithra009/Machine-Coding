# Rate Limiter: Complete Guide

**Author:** Mithravardhan P N

---

## Table of Contents
1. [What is Rate Limiting?](#what-is-rate-limiting)
2. [Why Rate Limiting is Used](#why-rate-limiting-is-used)
3. [How Rate Limiting Works (Core Flow)](#how-rate-limiting-works-core-flow)
4. [Common Design Dimensions](#common-design-dimensions)
5. [Algorithm 1: Token Bucket](#algorithm-1-token-bucket)
6. [Algorithm 2: Fixed Window](#algorithm-2-fixed-window)
7. [Algorithm 3: Sliding Window Log](#algorithm-3-sliding-window-log)
8. [Algorithm 4: Sliding Window Counter](#algorithm-4-sliding-window-counter)
9. [Comparison of All 4 Algorithms](#comparison-of-all-4-algorithms)
10. [Class Diagram Explanation](#class-diagram-explanation)
11. [Implementation Plan Based on the Diagram](#implementation-plan-based-on-the-diagram)
12. [Scalability, Correctness, and Production Notes](#scalability-correctness-and-production-notes)
13. [Execution Details](#execution-details)

---

## What is Rate Limiting?

Rate limiting controls how many requests a client can perform in a period of time.

In simple terms:
- A client can be a user, API key, IP address, tenant, or service account.
- A limit can be "N requests per T seconds".
- Every incoming request is checked.
- The result is either:
  - **Allowed** (pass through), or
  - **Rejected/Throttled** (typically HTTP 429).

Example:
- "100 requests per minute per user"
- "1000 requests per minute for free tier, 10000 for premium tier"

---

## Why Rate Limiting is Used

Rate limiting is not just about blocking abuse. It is a core control for reliability, fairness, and cost.

### 1) Protect system stability
- Prevent sudden traffic spikes from overloading CPU, memory, DB connections, and downstream services.
- Avoid cascading failures in microservices.

### 2) Fair usage across users
- Ensure one noisy client does not starve everyone else.
- Keep latency more predictable for normal users.

### 3) Abuse and bot mitigation
- Slow brute-force login attempts.
- Reduce scraping, spam bursts, credential stuffing, and API misuse.

### 4) Cost control
- Bound usage of expensive operations (LLM calls, payment gateways, external APIs).
- Protect paid infrastructure from accidental overuse.

### 5) Product and tier enforcement
- Enforce plan constraints (Free vs Premium vs Enterprise).
- Enable upsell by safely defining clear rate boundaries.

### 6) Better SLO/SLA outcomes
- Keep throughput within a known safe operating range.
- Preserve error budgets by rejecting excess load early.

---

## How Rate Limiting Works (Core Flow)

At runtime, the rate limiter follows a repeated decision process:

1. Identify the subject key.
	- Example: `userId`, `apiKey`, or `ip`.

2. Load policy for that subject.
	- Example: free tier gets 100/min, premium gets 1000/min.

3. Read current algorithm state for that key.
	- Depends on algorithm: tokens, counters, logs, etc.

4. Compute allow/deny.
	- If within limit: allow and update state.
	- If over limit: deny and optionally return retry hint.

5. Persist updated state.
	- In-memory for single process.
	- Redis/DB for distributed deployments.

### Typical response metadata
- HTTP status: `200` or `429 Too Many Requests`
- Headers often include:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`
  - `Retry-After`

---

## Common Design Dimensions

When selecting a rate limiting algorithm, evaluate:

1. **Accuracy near boundaries**
- Does it allow bursts around time window edges?

2. **Memory footprint**
- Per user state size can be tiny (counter) or large (timestamp logs).

3. **CPU overhead**
- Some algorithms are O(1), others require cleanup or scans.

4. **Burst handling behavior**
- Does it support controlled bursts or strict smoothness?

5. **Distributed compatibility**
- Can updates be done atomically in Redis/Lua or equivalent?

6. **Operational simplicity**
- Easier algorithms are often more reliable under pressure.

---

## Algorithm 1: Token Bucket

### Intuition
Think of each user as owning a bucket of tokens.
- Bucket capacity = maximum burst.
- Tokens refill over time at a fixed rate.
- Each request consumes one token.
- If no token is available, reject.

### State per user
- `tokens` (current available)
- `last_refill_timestamp`
- global/static config:
  - `capacity`
  - `refill_rate_per_second`

### Decision logic
For a request at time `now`:
1. Compute elapsed: $\Delta t = now - lastRefill$.
2. Add refilled tokens:
	$$tokens = \min(capacity, tokens + \Delta t \times refillRate)$$
3. If `tokens >= 1`, allow and decrement by 1.
4. Else reject.
5. Save updated `tokens` and `last_refill_timestamp`.

### Strengths
- Excellent for allowing controlled bursts.
- Smooth average rate over time.
- O(1) state and operations per request.
- Very common in API gateways.

### Weaknesses
- More math/state than fixed window.
- Precision can be tricky (floating-point vs integer token math).

### Example
Config: capacity = 10, refill = 5 tokens/sec.
- A user can burst up to 10 immediate requests.
- If emptied, they regain 5 tokens after 1 second.

### Best fit
- Public APIs requiring burst tolerance with long-term fairness.

---

## Algorithm 2: Fixed Window

### Intuition
Time is divided into fixed windows (e.g., each minute).
- Keep request count for current window.
- If count exceeds limit, reject.

### State per user
- `window_start_timestamp`
- `request_count`
- config:
  - `max_requests`
  - `window_seconds`

### Decision logic
At request time `now`:
1. Determine current window.
2. If `now` moved beyond current window, reset count to 0 and update window start.
3. If `count < max_requests`, allow and increment.
4. Else reject.

### Strengths
- Very simple to implement and reason about.
- O(1) memory and CPU per key.
- Easy to deploy in Redis with key expiry.

### Weaknesses
- Boundary burst problem:
  - User can send max requests at end of one window and again at start of next.
  - Effective short-term burst can be ~2x limit.

### Example
Limit: 100/min.
- 100 requests at 12:00:59.9 and 100 at 12:01:00.1 can pass.

### Best fit
- Systems where simplicity is top priority and boundary bursts are acceptable.

---

## Algorithm 3: Sliding Window Log

### Intuition
Store exact timestamps of recent requests per user.
- On each request, drop timestamps older than window.
- Count remaining timestamps.
- Allow only if count is below limit.

### State per user
- Ordered list/deque of request timestamps.
- config:
  - `max_requests`
  - `window_seconds`

### Decision logic
At request time `now`:
1. Evict timestamps where `timestamp <= now - window_seconds`.
2. Let current size be `k`.
3. If `k < max_requests`, allow and append `now`.
4. Else reject.

### Strengths
- High accuracy: true rolling window.
- No fixed-window boundary spike artifact.
- Easy to explain from a correctness point of view.

### Weaknesses
- Memory-heavy at high traffic (stores many timestamps).
- Cleanup cost can be non-trivial.
- Worst-case per-request work may grow with burst size.

### Example
Limit: 3 requests per 10s.
- If requests happened at [1, 3, 9], then at time 10 only timestamp 1 may expire depending on boundary rule.

### Best fit
- Lower/medium request rates where strict fairness/accuracy is essential.

---

## Algorithm 4: Sliding Window Counter

### Intuition
Approximate sliding log with two adjacent fixed windows:
- Current window count
- Previous window count
- Weighted interpolation based on how much of current window elapsed

This gives near-sliding behavior with much lower memory.

### State per user
- `current_window_start`
- `current_count`
- `previous_count`
- config:
  - `max_requests`
  - `window_seconds`

### Effective count formula
Let:
- $elapsed = now - currentWindowStart$
- $weight = (windowSeconds - elapsed) / windowSeconds$

Estimated rolling count:
$$effectiveCount = previousCount \times weight + currentCount$$

Decision:
- If `effectiveCount < max_requests`, allow and increment current count.
- Else reject.

### Strengths
- Much more memory efficient than sliding log.
- Smoother and fairer than fixed window.
- O(1) storage and O(1) computation.

### Weaknesses
- Approximation, not exact timestamp-level precision.
- Slightly more complex to implement than fixed window.

### Best fit
- High-scale APIs needing balanced accuracy/performance.

---

## Comparison of All 4 Algorithms

| Algorithm | Accuracy | Memory per key | CPU per request | Burst Handling | Complexity |
|---|---|---|---|---|---|
| Token Bucket | High for average rate | O(1) | O(1) | Excellent (controlled burst) | Medium |
| Fixed Window | Medium (boundary issue) | O(1) | O(1) | Can over-burst at boundaries | Low |
| Sliding Window Log | Very High (exact) | O(n in window) | O(1)-O(n cleanup) | Strict and fair | Medium-High |
| Sliding Window Counter | High (approximate) | O(1) | O(1) | Good, smoother than fixed | Medium |

Rule of thumb:
- Choose **Token Bucket** for burst-friendly API limits.
- Choose **Fixed Window** for easiest implementation.
- Choose **Sliding Window Log** for strongest precision.
- Choose **Sliding Window Counter** for scale + near-precision.

---

## Class Diagram Explanation

Your diagram represents a clean extensible OOP design with strategy-style polymorphism.

### 1) `UserTier` (Enum)
- Values: `FREE`, `PREMIUM`.
- Purpose: classify users by plan.
- Benefit: deterministic policy selection.

### 2) `User`
- Fields: `userId: String`, `tier: UserTier`.
- Purpose: request identity + plan metadata.

### 3) `RateLimiterService`
- Field: `rateLimiters: Map<UserTier, RateLimiter>`.
- Method: `allowRequest(user): boolean`.
- Responsibility:
  - Entry point used by API/controller layer.
  - Chooses limiter by `user.tier`.
  - Delegates request decision to selected limiter.

### 4) `RateLimiter` (Abstract Base Class)
- Fields:
  - `config: RateLimitConfig`
  - `bucketMap` or equivalent per-user state map.
- Methods:
  - `setRateLimitConfig(...)`
  - `allowRequest(userId): boolean` (abstract/overridable)
- Responsibility:
  - Shared contracts and common behavior.
  - Concrete algorithms override decision logic.

### 5) Concrete limiter implementations
- `TokenBucket`
- `FixedWindow`
- `SlidingWindowLogs`
- `SlidingWindowCounter`

Each class implements algorithm-specific state transitions while exposing the same interface (`allowRequest`).

### 6) `RateLimitType` (Enum)
- Values include the four algorithm names.
- Purpose: select limiter type at construction time.

### 7) `RateLimitConfig`
- Fields like `maxRequests`, `windowSeconds`.
- For token bucket, you can extend with:
  - `bucketCapacity`
  - `refillRatePerSecond`
- Purpose: parameter object for policy.

### 8) `RateLimiterFactory`
- Method: `createRateLimiter(config, type)`.
- Responsibility:
  - Encapsulate object creation.
  - Keep service code clean.
  - Support easy switch/addition of algorithms.

### Relationship summary
- `RateLimiterService` depends on abstraction (`RateLimiter`), not concrete classes.
- Factory creates concrete limiter instances.
- Service stores instances per tier.
- User request flows into chosen limiter.

---

## Implementation Plan Based on the Diagram

This is a practical plan to implement in a clean, testable, production-friendly way.

### Phase 1: Define contracts and models
1. Create enums:
	- `UserTier`
	- `RateLimitType`
2. Create data classes:
	- `User`
	- `RateLimitConfig`
3. Define abstract base class `RateLimiter`:
	- constructor with config
	- `allowRequest(userId)` abstract
	- optional hooks for cleanup/metrics

### Phase 2: Implement four algorithms
1. `TokenBucketRateLimiter`
	- map userId -> token state
	- refill + consume logic
2. `FixedWindowRateLimiter`
	- map userId -> (windowStart, count)
3. `SlidingWindowLogRateLimiter`
	- map userId -> deque[timestamps]
	- prune expired timestamps each request
4. `SlidingWindowCounterRateLimiter`
	- map userId -> (prevCount, currCount, currWindowStart)
	- weighted effective count calculation

### Phase 3: Factory and service wiring
1. Build `RateLimiterFactory.createRateLimiter(config, type)`.
2. In `RateLimiterService`:
	- create limiter instances for each `UserTier`
	- store in `Map<UserTier, RateLimiter>`
3. Implement `allowRequest(user)`:
	- resolve limiter by `user.tier`
	- call limiter with `user.userId`
	- return decision

### Phase 4: Thread-safety and storage strategy
1. Single-process version:
	- use in-memory dictionaries/maps + locks
2. Distributed version:
	- move state to Redis
	- use atomic Lua scripts or transactions
3. Add TTL/eviction to remove idle user state.

### Phase 5: API integration
1. Middleware/interceptor calls `RateLimiterService.allowRequest(user)`.
2. On deny:
	- return HTTP 429
	- include retry metadata headers.
3. On allow:
	- continue request pipeline.

### Phase 6: Testing strategy
1. Unit tests per algorithm:
	- below-limit, at-limit, over-limit
	- exact boundary timestamps
	- burst scenarios
2. Concurrency tests:
	- multi-thread request simulation
3. Property/perf tests:
	- monotonic behavior
	- state growth checks

### Phase 7: Observability and tuning
1. Metrics:
	- allowed count
	- denied count
	- limiter latency
2. Logs:
	- throttled key + tier + reason
3. Config externalization:
	- tune limits without code changes

---

## Scalability, Correctness, and Production Notes

### 1) Time synchronization
- In distributed systems, clock drift affects time-based algorithms.
- Prefer monotonic clocks where possible.

### 2) Memory control
- Keep per-user map bounded with TTL eviction.
- Sliding log needs special care for high-cardinality traffic.

### 3) Idempotency and retries
- Decide whether retries count as new requests.
- Be consistent to avoid surprising clients.

### 4) Multi-dimensional limits
- Often combine:
  - per-user
  - per-IP
  - global service cap

### 5) Graceful degradation
- During limiter store outage, define policy:
  - fail-open (availability first), or
  - fail-closed (protection first).

### 6) Security
- Hash/normalize keys if user IDs are sensitive.
- Avoid leaking internal policy details in error responses.

---

## Suggested Default Choices

For most API products:
- Start with **Token Bucket** or **Sliding Window Counter**.
- Use **Fixed Window** for very simple internal systems.
- Use **Sliding Window Log** only when strict precision is required and traffic/cardinality are manageable.

---

Why this design ?:
- **Policy selection** (`RateLimiterService` + tier map)
- **Algorithm behavior** (four concrete limiters)
- **Construction logic** (`RateLimiterFactory`)
- **Configuration** (`RateLimitConfig`)

That separation keeps the system easy to extend, test, and scale.

---

# Execution Details

### Prerequisites
- Python 3.7 or higher

### Run Commands

Option 1: Run from inside the RateLimiter folder

cd RateLimiter
python main.py

Option 2: Run from repository root

python -m RateLimiter.main

### CLI Menu Flow
1. Add user
2. Login using user ID
3. Send request using currently logged-in user
4. Get user details
5. Change user tier
6. Remove user
7. Logout
8. Exit

### Expected Usage Sequence
1. Create a user from menu option 1.
2. Copy the generated user ID.
3. Login from menu option 2 using that ID.
4. Use menu option 3 repeatedly to send requests without entering user ID each time.
5. Observe allow or block decisions from the fixed window limiter.

### Notes
- Current implemented limiter type is FIXED_WINDOW.
- Free and premium limits are configured through UserTier in main.py.
- Login state is session-based and resets when the CLI process exits.
