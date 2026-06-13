# Coverage Matrix - Compact Submission Build

| Tutorial section | Video block | Scene file | Covered? | Notes |
|---|---|---|---|---|
| Main goals and taxonomy | Part I | `part1_g1_intro_taxonomy.py` | Yes | Intro, roadmap, data problems, attribution taxonomy. |
| Corroborative attribution | Part I | `part1_g2_corroborative.py` | Yes | Evidence finding, citation, copyright detection, similarity/search, IR, limitation. |
| Game-theoretic attribution | Part I | `part1_g3_game_theoretic.py` | Yes | Credit, coalition, marginal contribution, Shapley intuition, scale issue. |
| Predictive attribution | Part I | `part1_g4_predictive.py` | Yes | Subset indicators, datamodel, sensitivity, amortized cost, three lenses recap. |
| M-estimation and weights | Part II | `part2_core_theory.py` | Yes | Objective with weights, `w=1`, downweighting, leave-one-out. |
| Leave-one-out and influence | Part II | `part2_core_theory.py` | Yes | Exact retraining intuition, gradient/Hessian approximation, limitations implied. |
| Datamodels | Part II | `part2_core_theory.py` | Yes | Subset indicator, surrogate, linear datamodel, attribution coefficient. |
| Scaling challenges | Part III | `part3_scaling_and_evaluation.py` | Yes | Dataset/model scale, SGD noise, non-convexity, Hessian cost, brute-force limits. |
| Modern approximation methods | Part III | `part3_scaling_and_evaluation.py` | Yes | Hessian approximation, training dynamics, surrogate models, datamodel-style estimators. |
| Counterfactual evaluation | Part III | `part3_scaling_and_evaluation.py` | Yes | Predicted vs actual counterfactual behavior and evaluation takeaways. |
| Applications | Part IV | `part4_applications.py` | Yes | Debugging, dataset selection, poisoning, unlearning, valuation, citation, RAG. |
| Epilogue and credits | Recap | `part5_epilogue_recap.py` | Yes | Four-part recap, three lenses, final takeaway, ICML tutorial credit. |

## Compact Build Tradeoff

This build intentionally compresses the full 2-hour tutorial into a 40-60 minute submission target. It preserves the main conceptual arc and representative visuals, but does not attempt to reproduce every slide or every theorem-level detail from the original tutorial.

## Current Runtime Status

The current low-quality rendered scene set is about 26.9 minutes after expanding G1 and G3:

| Block | Low-render duration |
|---|---:|
| Part I G1 - Intro/taxonomy | 5.96 min |
| Part I G2 - Corroborative | 2.54 min |
| Part I G3 - Game-theoretic | 6.08 min |
| Part I G4 - Predictive | 1.57 min |
| Part II - Core theory | 2.93 min |
| Part III - Scaling/evaluation | 2.99 min |
| Part IV - Applications | 3.16 min |
| Epilogue/recap | 1.67 min |

This is a renderable compact pass with broad coverage, but it is not yet a 40-60 minute final cut. To hit the final submission target, expand the voice scripts and scene timing for G3, G4, Part II, Part III, Part IV, and the epilogue rather than only padding silent holds.
