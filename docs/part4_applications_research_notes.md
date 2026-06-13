# Part 4 - Applications Research Notes

These notes ground the Part 4 script in primary sources and nearby research. They are not meant to be copied into ElevenLabs.

## Core Framing

Part 4 should not present applications as a loose list. The defensible framing is:

1. Define the behavior of interest.
2. Define the data unit.
3. Define the intervention or attribution question.
4. Choose the attribution lens: evidence, credit, or counterfactual prediction.
5. Evaluate against the downstream decision.

This framing follows from the split built earlier in the video:

- `corroborative attribution`: evidence/support for an output or claim.
- `game-theoretic attribution`: credit assignment against a utility.
- `predictive attribution`: predicting model behavior under data interventions.

## Sources and Implications

### Influence Functions

Source: Koh and Liang, "Understanding Black-box Predictions via Influence Functions", ICML 2017.  
URL: https://arxiv.org/abs/1703.04730

Relevant claims:

- Influence functions trace predictions through the learning algorithm back to training data.
- The paper explicitly demonstrates uses for model behavior understanding, debugging, dataset error detection, and training-set attacks.
- The method relies on gradient and Hessian-vector computations for scaling, but theory is cleaner in differentiable/convex-like settings than in arbitrary DNN training.

Script implication:

- It is fair to say influence-style attribution can help produce a shortlist for debugging or identify suspicious influential training points.
- It is also fair to flag dual-use risk: methods that reveal influential points can inform attacks.

### Data Shapley and Data Valuation

Source: Ghorbani and Zou, "Data Shapley: Equitable Valuation of Data for Machine Learning", 2019.  
URL: https://arxiv.org/abs/1904.02868

Relevant claims:

- Data Shapley quantifies each training datum's value to predictor performance.
- It is motivated by equitable valuation and compensation.
- Experiments show low Shapley value can capture outliers/corruptions, and high Shapley value can inform what data to acquire.

Related source: Kwon and Zou, "Beta Shapley", 2021.  
URL: https://arxiv.org/abs/2110.14049

Relevant claims:

- Data valuation methods can help detect mislabeled data, support learning with subsamples, and identify helpful/harmful points.

Script implication:

- Data valuation should be presented as utility-dependent, not absolute.
- Dataset selection and data cleaning can be linked to valuation, but fairness/payment and predictive usefulness are distinct objectives.

### Datamodels

Source: Ilyas et al., "Datamodels: Predicting Predictions from Training Data", 2022.  
URL: https://arxiv.org/abs/2202.00622

Relevant claims:

- A datamodel maps a training subset indicator to a target behavior/prediction.
- Simple linear datamodels can predict model outputs surprisingly well.
- Applications include predicting dataset counterfactuals, identifying brittle predictions, finding semantically similar examples, quantifying train-test leakage, and embedding data.

Script implication:

- Predictive attribution should be framed as behavior prediction under data changes, not merely assigning a score.
- Part 4 should include train-test leakage/brittle predictions as application-adjacent examples, especially under debugging/audit.

### TRAK

Source: Park et al., "TRAK: Attributing Model Behavior at Scale", 2023.  
URL: https://arxiv.org/abs/2303.14186

Relevant claims:

- TRAK targets the tradeoff between tractability and effectiveness for large-scale differentiable models.
- It traces model behavior to training data and was evaluated across image, vision-language, and language models.

Script implication:

- When discussing scalable applications, avoid implying that one method is universally best.
- TRAK is a strong example of a scalable predictive attribution estimator, but still needs counterfactual evaluation for the use case.

### Data Poisoning

Source: Geiping et al., "Witches' Brew: Industrial Scale Data Poisoning via Gradient Matching", 2020.  
URL: https://arxiv.org/abs/2009.02276

Relevant claims:

- Poisoning can be targeted, clean-label, and effective against modern deep networks trained from scratch.
- Gradient matching is a practical mechanism for constructing attacks.

Script implication:

- Data attribution/security should be described as dual-use.
- Attribution can support audit and triage of suspicious data, but exposing influence information may also help attackers.

### Machine Unlearning

Source: Bourtoule et al., "Machine Unlearning", 2019/2021.  
URL: https://arxiv.org/abs/1912.03817

Relevant claims:

- Unlearning aims to reduce the cost of removing data influence compared with full retraining.
- SISA training limits a data point's influence by sharding/slicing training.
- Unlearning is motivated by privacy/data governance and has accuracy/compute tradeoffs.

Script implication:

- Attribution can help estimate or audit the impact of forgetting, but it is not itself a certificate of unlearning.
- The gold-standard question remains counterfactual: how would the model behave if trained without the forget set?

### RAG, Citation, and Faithfulness

Source: Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", 2020.  
URL: https://arxiv.org/abs/2005.11401

Relevant claims:

- RAG combines parametric model memory with non-parametric retrieved memory.
- Provenance and updating world knowledge are part of the motivation.

Source: Wallat et al., "Correctness is not Faithfulness in RAG Attributions", 2024.  
URL: https://arxiv.org/abs/2412.18004

Relevant claims:

- Citation correctness and citation faithfulness are distinct.
- A cited document may support the statement but not be what the model actually relied on.
- The paper reports substantial post-rationalization risk in attributed answers.

Script implication:

- Citation/RAG should be framed as corroborative attribution: support/evidence for a claim.
- The script should explicitly distinguish citation correctness from actual reliance/faithfulness.

## Script Corrections From Research

- Add `train-test leakage` and `brittle predictions` as audit/debugging examples from datamodels.
- Strengthen warning that citation support is not causal influence.
- Strengthen warning that attribution for unlearning is only triage/audit unless paired with unlearning-specific evaluation.
- Keep data valuation tied to a utility function and context.
- Avoid overclaiming that attribution alone solves poisoning, unlearning, copyright, or RAG faithfulness.
