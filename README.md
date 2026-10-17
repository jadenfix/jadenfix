<a href="https://jadenfix.github.io"><img src="assets/blackhole.webp" width="100%" alt="Jaden Fix. A ray-traced black hole drifting in deep space."></a>

Software engineer on the Platform & Applied AI team at [AfterQuery](https://www.afterquery.com), building the post-training data and RL environments frontier models learn from. Before that I built agents at [Scale AI](https://scale.com), and before that I was a founding engineer at [Roe](https://www.roe-ai.com) (YC), where I led agent engineering and shipped agents to banks and Fortune 500 risk teams.

&nbsp;

<img src="assets/constellation.webp" width="100%" alt="An agent's episode drawn as a constellation. Outcome-only credit lights the orbit that went nowhere as brightly as the winning path; branch-aware credit turns it red.">

**Your agent's training pipeline is teaching it to stall.** Outcome-only RL pays every step of a winning episode the same, so a step that does nothing earns as much as the step that wins. Doing nothing never fails, so that's what the agent learns. Trained this way, agents end up worse than untrained ones: 0.24 vs. 0.79 success. Score each step by what it actually changed and success hits 1.00.

<sub>*Branch-Aware Hindsight Credit Assignment for LLM Agents* · [Paper](https://github.com/jadenfix/CreditAssignment/blob/main/paper/main.pdf) · [Code](https://github.com/jadenfix/CreditAssignment)</sub>

<sub>Also: [Critique-Transport Smoothing](https://github.com/jadenfix/CreditAssignment-LongHorizon), optimal transport for long-horizon credit assignment (in progress) · [Predictive Stochastic Modeling for Financial Markets](https://github.com/jadenfix/Predictive-Stochastic-Modeling-for-Financial-Markets-/blob/main/Predictive_Stochastic_Modeling_for_Financial_Markets.pdf), winner of the Adam Smith Award</sub>

&nbsp;

| | |
|:--|:--|
| [**rusty**](https://github.com/jadenfix/rusty) | A coding agent in one static Rust binary. It doesn't get to say "done" without proof. |
| [**FullStack-Bench**](https://github.com/jadenfix/FullStack-Bench) | Can an agent ship a full-stack change without paging anyone? A benchmark that finds out. |
| [**tempo**](https://github.com/jadenfix/tempo) | A browser built for models, not people. |
| [**Palette**](https://github.com/jadenfix/palette) | Evals and a CI gate that blocks changes that don't generalize. |
| [**cradle**](https://github.com/jadenfix/cradle) · [**remi**](https://github.com/jadenfix/remi) · [**tempOS**](https://github.com/jadenfix/tempOS) · [**temp.js**](https://github.com/jadenfix/temp.js) · [**Arrha**](https://github.com/jadenfix/arrha) | The rest of my agent platform: sandbox, memory, OS, runtime, and payments. All Rust. |
| [**Spacewind**](https://github.com/jadenfix/space-simulation-engine) | A physics engine for sailing on sunlight. The black hole above runs on the same math, [ray-traced](scripts/blackhole.py). |

<details>
<summary><sub>Commits I like</sub></summary>
<br>

[`40210c7`](https://github.com/jadenfix/arrha/commit/40210c7) Batch-verify BLS signatures with blst multi-pairing<br>
[`8618e7a`](https://github.com/jadenfix/arrha/commit/8618e7a) Constant-time audit of the VRF and KES code<br>
[`e07d8a7`](https://github.com/jadenfix/palette/commit/e07d8a7) A CI gate that's allowed to say *inconclusive*<br>
[`2df8415`](https://github.com/jadenfix/rusty/commit/2df8415) Editing the test guard to pass is a fail, not a pass<br>
[`ad8e6d7`](https://github.com/jadenfix/space-simulation-engine/commit/ad8e6d7) Fix the plasma solve where the electric field crosses zero

</details>

<sub>[jadenfix.github.io](https://jadenfix.github.io) · [LinkedIn](https://linkedin.com/in/jadenfix)</sub>
