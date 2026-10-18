<a href="https://jadenfix.github.io"><img src="assets/blackhole.webp" width="100%" alt="Jaden Fix. A ray-traced black hole drifting in deep space."></a>

### About

I'm a software engineer in San Francisco. I'm on the Platform & Applied AI team at [AfterQuery](https://www.afterquery.com), building the post-training data and RL environments frontier models learn from. Before that I built agents on the Enterprise AI team at [Scale AI](https://scale.com), and before that I was a founding engineer at [Roe](https://www.roe-ai.com) (YC), where I ended up leading agent engineering: production agents for ERP, fraud and compliance work, deployed at banks and Fortune 500 companies, in the cloud and on-prem.

I came to software through economics and statistics, with an M.S. from Cal Poly and an undergrad thesis on forecasting bear markets that won the Adam Smith Award. It still shapes how I build: if a claim can be measured, measure it, and write down what it doesn't show.

&nbsp;

### Research

<img src="assets/constellation.webp" width="100%" alt="An agent's episode drawn as a constellation. Outcome-only credit lights the orbit that went nowhere as brightly as the winning path; branch-aware credit turns it red.">

**Your agent's training pipeline may be teaching it to stall.** Outcome-only credit pays every step of a winning episode the same, so a step that does nothing earns as much as the step that wins, and doing nothing never fails. I call this loop-action bias. On a controlled benchmark, policies trained this way did worse than the prompted baseline (0.24 vs. 0.79 success); scoring each step by what it actually changed brought success to 1.00. On real ALFWorld, branch-aware scoring separates 2.6 to 9.4 times more states than outcome-only, and the gap is widest for the weaker model.

<sub>*Branch-Aware Hindsight Credit Assignment for LLM Agents* · [Paper](https://github.com/jadenfix/CreditAssignment/blob/main/paper/main.pdf) · [Code](https://github.com/jadenfix/CreditAssignment)</sub><br>
<sub>Also: [Critique-Transport Smoothing](https://github.com/jadenfix/CreditAssignment-LongHorizon), optimal transport for long-horizon credit assignment (in progress) · [Predictive Stochastic Modeling for Financial Markets](https://github.com/jadenfix/Predictive-Stochastic-Modeling-for-Financial-Markets-/blob/main/Predictive_Stochastic_Modeling_for_Financial_Markets.pdf), winner of the Adam Smith Award</sub>

&nbsp;

### Tempera

An agent platform I'm building on my own time, mostly in Rust. The idea: agents that act in the real world should do it under explicit authority, inside a sandbox, with memory they can cite and a receipt for everything consequential. Every product exposes one OpenAPI contract, and the SDKs, CLIs and MCP tools are generated from it, so nothing drifts.

| | | |
|:--|:--|:--|
| **See and act** | [tempo](https://github.com/jadenfix/tempo) | A browser built for models, not people. Ranked, stable-ID, diff-able page state instead of screenshots, and anything derived from a page is tainted and pushed into the sandbox. About 99k lines of Rust across 29 crates. |
| **Run safely** | [cradle](https://github.com/jadenfix/cradle) · [tempOS](https://github.com/jadenfix/tempOS) · [temp.js](https://github.com/jadenfix/temp.js) | A capability sandbox where every unproven lane fails closed. Authority, policy and hash-chained receipts at the OS layer. V8 and CPython embedded in one Rust host. |
| **Remember and improve** | [remi](https://github.com/jadenfix/remi) · [Palette](https://github.com/jadenfix/palette) | Bitemporal memory that answers with provenance and flags contradictions. An eval gate with its own statistics engine (BCa bootstrap, CUPED, exact McNemar, confidence sequences) that answers pass, fail, or *inconclusive*. |
| **Connect** | MCP · workflows · LLM gateway · auth | A typed Rust MCP framework and gateway benchmarked on 44k-tool retrieval, a deterministic workflow engine, an LLM gateway that reserves budget before every call, and one OAuth 2.1 issuer across the platform. |
| **Settle** | [Arrha](https://github.com/jadenfix/arrha) · payments | A Rust L1 with HotStuff and VRF consensus, BLS batch verification, KZG and a TLA+ spec, about 1,600 tests. Payment orchestration on a double-entry journal. |
| **Reach** | [SDK](https://github.com/tempera-dev/tempera-sdk) · iOS · Android | 616 typed operations across 20 products, generated into SDKs for 7 languages. Native iOS and Android apps. |
| **Domains** | math · bio · CAD · materials · risk | Domain packs on the same stack, including math results checked in Lean 4. |

<sub>Linked repos are public; the rest is private for now.</sub>

&nbsp;

### Also built

| | |
|:--|:--|
| [**FullStack-Bench**](https://github.com/jadenfix/FullStack-Bench) | Can an agent ship a full-stack change without paging anyone? Agents work on SimCloud, a simulated cloud with synthetic users on prod and a hash-chained incident log. Of 83 graded runs, 64 passed the usual final-state check, and 38 of those were not a safe success once the whole episode was graded. |
| [**rusty**](https://github.com/jadenfix/rusty) | A coding agent in one static Rust binary, with about 400 tests. A goal only closes when a pinned check passes, and its permission classifier reads what `npm run`, heredocs and `ssh` will actually execute before deciding to ask. |
| [**Spacewind**](https://github.com/jadenfix/space-simulation-engine) | A dependency-free C11 physics engine for sailing on sunlight: Kerr geodesics, solar wind, 3D electromagnetic particle-in-cell. Its assurance run passes about 233,000 checks with zero failures, and every claim file lists what it does *not* show. The black hole above is the same physics, [ray-traced](scripts/blackhole.py). |
| [**ReplayKit**](https://github.com/jadenfix/ReplayKit) | Time-travel debugging for agent runs. Fork any step, patch it, replay only what's downstream, and diff. |
| [**DRL4MM**](https://github.com/jadenfix/DRL4MM) | A TD3 market-making agent trading against a FIFO limit order book. |

&nbsp;

### Open source

Merged upstream in [wild](https://github.com/wild-linker/wild/pull/2679) (Mach-O `LC_RPATH`), [Gymnasium](https://github.com/Farama-Foundation/Gymnasium/pull/1753), [Minigrid](https://github.com/Farama-Foundation/Minigrid/pull/525), [SkyRL](https://github.com/NovaSky-AI/SkyRL/pull/2425) and [Harbor](https://github.com/harbor-framework/harbor/pull/3494). I also wrote Roe's [Go SDK](https://github.com/roe-ai/roe-golang/pull/1).

<details>
<summary><sub>Commits I like</sub></summary>
<br>

[`40210c7`](https://github.com/jadenfix/arrha/commit/40210c7) Batch-verify BLS signatures with blst multi-pairing<br>
[`8618e7a`](https://github.com/jadenfix/arrha/commit/8618e7a) Constant-time audit of the VRF and KES code<br>
[`e07d8a7`](https://github.com/jadenfix/palette/commit/e07d8a7) A CI gate that's allowed to say *inconclusive*, and how many more cases it needs<br>
[`2df8415`](https://github.com/jadenfix/rusty/commit/2df8415) Editing the test guard to pass is a fail, not a pass<br>
[`ad8e6d7`](https://github.com/jadenfix/space-simulation-engine/commit/ad8e6d7) Fix the plasma solve where the electric field crosses zero

</details>

<sub>[jadenfix.github.io](https://jadenfix.github.io) · [LinkedIn](https://linkedin.com/in/jadenfix)</sub>
