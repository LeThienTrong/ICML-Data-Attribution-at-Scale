from __future__ import annotations

from exact_voice_subtitles import ROOT, build_cues, write_outputs


VOICE_SCRIPT = ROOT / "docs" / "part4_applications_voice_script_elevenlabs.txt"
OUTPUT = ROOT / "subtitles" / "part4_applications_bilingual.srt"
AUDIO_FILES = [
    "p4_00.mp3",
    "p4_01.mp3",
    "p4_02.mp3",
    "p4_03.mp3",
    "p4_04.mp3",
    "p4_05.mp3",
    "p4_06.mp3",
    "p4_07.mp3",
    "p4_08.mp3",
    "p4_09.mp3",
]
PARAGRAPH_COUNTS = [11, 16, 14, 16, 18, 15, 15, 17, 15, 15]


ENGLISH_TEXT = """
In Part III, we treated data attribution as a problem of scaling and evaluation.

We asked: if we cannot retrain the model for every counterfactual, which estimator can we use? Influence function? TracIn? TRAK? Datamodels? Or a cheaper proxy?

But when we move to applications, the question changes slightly.

End users usually do not ask whether this estimator is mathematically elegant.

They ask: what does this score help me do?

Can it help debug a specific failure? Can it help select better data? Can it help detect poisoning? Can it help unlearn a dataset without breaking the model? Can it help cite sources for an answer?

So Part IV is the decision layer on top of everything we have built.

We no longer view an attribution score as a number standing alone. We view it as a signal for action.

And once we talk about action, the most important question is: what kind of relationship between data and behavior does that action need?

If we need evidence, we use one lens. If we need credit, we use another lens. If we need to predict counterfactual behavior, we need yet another lens.

This is the point that keeps the whole video from getting confused: the application decides what attribution means.

Before going into each application, let us set up a general recipe.

Step one: define the model behavior we care about.

Behavior can be a wrong output, loss on a subgroup, hallucination rate, win rate, toxicity, robustness, fairness, or accuracy on a specific benchmark.

If the behavior is not clear, the attribution score will also be vague.

Step two: define the data unit.

A unit can be a document, a paragraph, an image, a user record, a prompt-response pair, a data cluster, or an entire dataset.

The choice of unit decides whether the score can lead to action. If the unit is too small, the score is noisy. If the unit is too large, we do not know which part to fix.

Step three: define the intervention.

Will we remove data? Downweight data? Add data? Replace labels? Deduplicate? Or retrain without a forget set?

Attribution used to explain an output does not necessarily answer what removing data will do.

Step four: choose the notion of attribution.

Corroborative attribution measures evidence. Game-theoretic attribution measures credit within a utility. Predictive attribution measures the ability to predict behavior when data changes.

Step five: check with the right evaluation.

If the score ranks data for debugging, we check precision among the top examples. If the score selects data, we check the model after adding or removing data. If the score is for unlearning, we check behavior after the intervention.

This recipe may sound slow, but it prevents many mistakes.

Because without defining behavior, unit, intervention, and evaluation, a beautiful score can still answer the wrong application question.

The first application is model debugging.

We start from a bad behavior we have observed: the model misclassifies an image, answers a factual question incorrectly, hallucinates a claim, or fails on a specific user group.

A natural reaction is to ask: in the training data, which examples are related to this failure?

Here, attribution does not always need to prove full causality. Often we only need a good shortlist for humans to inspect.

For example, if the model answers wrongly because it learned the wrong pattern, attribution can pull out training examples with wrong labels, ambiguous annotations, or too many duplicates.

If the model fails on a subgroup, attribution may show that the training set has very few examples like that subgroup, or many similar examples with inconsistent labels.

Research on datamodels also gives us a broader audit: find brittle predictions, meaning predictions that change strongly when the training subset changes; and find train-test leakage, when a test example has an unusual dependence on a very nearby part of the training data.

In debugging, top-k examples are often more important than a perfect absolute score.

The engineer wants to know: which 20 examples should I inspect first?

So evaluation for debugging can be very pragmatic: among the top-k examples, how many truly help diagnose the failure? If we remove or fix them, does the failure decrease? If we add similar data, does the behavior improve?

But there is a small trap.

Data that is semantically related is not necessarily data that caused the failure.

An example that looks very similar to the test case may only be evidence, not the cause. Conversely, a data cluster that looks farther away may have made the model learn the wrong shortcut.

So debugging often needs to combine two things: similarity to find nearby evidence, and predictive or counterfactual attribution to test the effect when data changes.

The second application is dataset selection.

If debugging starts from the question "where did this error come from?", dataset selection asks: "which data should we train more on, keep, or prioritize?"

This is a very practical question.

In many pipelines, data is no longer something we simply collect as much as possible.

Data has cost: storage cost, annotation cost, training cost, moderation cost, and sometimes legal cost.

If we have a limited budget, attribution can help choose data that is expected to improve the most important behavior.

For example, we may want to improve accuracy on rare classes. We can look for examples that the estimator predicts will improve behavior on rare classes.

Or we may want to reduce hallucination for a type of question. We can prioritize data with a predicted positive effect on that metric, instead of only adding data that is embedding-similar to the query.

Here, predictive attribution is very natural.

We do not only ask which data looks like the target. We ask whether adding or upweighting this data would improve the target behavior.

Literature on data valuation, such as Data Shapley, also gives a related view. High-value data can suggest what kind of data to acquire next. Unusually low-value data can be an outlier, a corrupted example, or a label that needs checking.

However, dataset selection is also where it is easy to overfit to a metric.

If we select data only to improve one benchmark, the model may get better on that benchmark but worse elsewhere.

So a good workflow usually has three layers: select data by attribution, train or fine-tune the model, then test on held-out behaviors that were not used for selection.

In other words, data selection should not just be "sort by score and take the top."

It should be a loop: score, choose a subset, train, evaluate, then update the objective.

The third application is data valuation.

Here the question is not "which data helps debug the failure?", and not exactly "which data should be added to the model?"

The question is: if many parties contribute data, how should value or credit be allocated?

This is where game-theoretic attribution returns.

If we have a utility function, such as accuracy, revenue, win rate, or a quality metric, we can ask how much each contributor adds to that utility.

Shapley value is an elegant ideal because it averages marginal contribution across many different contexts.

In Data Shapley, this intuition is brought into machine learning: the value of a datum is measured through its contribution to predictor performance, while trying to preserve natural valuation principles such as identical data receiving identical credit, and data that does not change utility not receiving large credit.

But in practice, data valuation is extremely sensitive to the definition of utility.

A dataset may be very valuable for a medical task, but almost useless for machine translation.

A contributor may provide many examples, but if most are duplicates of data already present, the real marginal contribution can be low.

Conversely, a small contributor may provide a rare data group that strongly improves the model on an important subgroup.

So data valuation should not be understood as "what is the absolute value of this data?"

It should be understood as: for this utility, in the current data context, what is the contribution of this data?

This point also helps avoid a common misunderstanding.

Fair credit and predictive usefulness are not always the same.

An attribution method may predict behavior very well when data is removed, but it may not satisfy the fairness axioms we want for payment.

Conversely, a credit allocation that is beautiful from a fairness perspective may be too expensive or too noisy for a daily selection pipeline.

The application decides the tradeoff.

The fourth application is data poisoning and security.

In data poisoning, an attacker inserts training examples designed to make the model fail, open a backdoor, or bias it in a direction that benefits the attacker.

Some modern attacks are more dangerous because they can be clean-label: to a human, the label still looks reasonable, but the example is subtly modified so its gradient pulls the model toward a wrong target during training.

Attribution can help defense in two ways.

The first way is tracing from bad behavior back to training examples with abnormal influence.

If a small group of data has a very high score for a specific failure mode, that may be a signal to audit.

The second way is detecting outliers in influence.

A normal data point may help a little or hurt a little. But a data point with too large an effect, especially on a sensitive target behavior, deserves careful inspection.

However, this part must be said carefully.

Attribution in security is dual-use.

It can help defenders find malicious data, but it can also help attackers understand which points have large influence and optimize attacks better.

Therefore in security applications, we do not only ask whether the estimator is accurate.

We also ask: who is allowed to see the score? At what level is the score aggregated? Do we need privacy protection? Can it be used to reverse engineer training data?

In other words, security is not only a technical use case.

It is where data attribution must come with governance.

The fifth application is machine unlearning.

Suppose there is a forget set F: a user requests data deletion, a license changes, or part of the data is found to be unsuitable.

The ideal question is: if we trained the model from scratch on S without F, how would model behavior change?

That is a very natural counterfactual question.

But with large models, retraining from scratch for every unlearning request can be too expensive.

One direction such as SISA training tries to reduce this cost by splitting training into shards and slices, so that when one data point must be forgotten, only a smaller part of the system needs to be updated instead of the entire model.

Data attribution does not automatically solve machine unlearning, but it helps us estimate and test the impact of forgetting.

Predictive attribution can forecast which behaviors will change a lot if F is removed.

Influence-style methods can give a fast approximation when the assumptions are stable enough.

Datamodels can learn a map from subset or group removal to behavior, if we have enough training runs to learn the surrogate.

But in unlearning, the evaluation standard must be very clear.

We do not only need the model to "look forgotten" on a few examples.

We need to check whether utility is preserved, whether privacy or compliance is satisfied, and whether the model still remembers information from the forget set under attack probes.

So attribution here is part of the pipeline, not the final certificate.

It helps us prioritize, predict, and audit. But the unlearning decision still needs independent evaluation.

The next application is citation, RAG, and copyright-related analysis.

This is where corroborative attribution is very natural.

When a language model produces an answer, users often ask: which sources support this answer?

In RAG, the model already has a retrieval step. But retrieval does not automatically mean the citation is correct.

A document may be retrieved but not actually support the final claim.

Conversely, one claim in the output may need several sources together to provide enough evidence.

And even when a citation is correct in content, there is a harder question: is that citation faithful? Meaning, did the model actually rely on that source when generating the claim, or was the source attached afterward as a plausible explanation?

Corroborative attribution tries to connect each output, claim, or span with evidence candidates in the corpus.

This application is different from predictive attribution.

We are not asking how model behavior would change if this document were removed from training data.

We are asking whether this document supports, contradicts, or relates to the current output.

For copyright detection, it is similar: the question is usually not utility or counterfactual behavior.

The question is whether the output is too close to a source in the corpus. Is there evidence of reproduction? Which passage is the evidence for that concern?

So citation and copyright are very good examples of choosing the right lens.

If we use game-theoretic credit to explain citation, we can say the wrong thing.

If we use retrieval similarity to conclude causal influence, we can also say the wrong thing.

A good system must separate clearly: evidence for output, credit for utility, and prediction for intervention.

At this point, we can summarize the important pitfalls.

Pitfall one: confusing evidence with cause.

A source supporting a claim is not necessarily the cause that made the model generate that claim.

It may only be a document that states the same fact, or a passage retrieved after the model already tended to answer that way.

With RAG, this is the difference between citation correctness and citation faithfulness: a source may support the answer, but it may not be the source the model actually relied on.

Pitfall two: confusing similarity with value.

Data that is close to the target in embedding space can be useful for retrieval, but it does not necessarily have high marginal contribution for training.

Pitfall three: confusing fair credit with predictive effect.

A score used to divide payment needs fairness criteria. A score used to select data needs to predict improvement. These two goals may lead to different methods.

Pitfall four: forgetting that the unit of attribution changes the conclusion.

A document can have a low score, while one paragraph in that document is extremely important.

A data point can have a low score, while its whole cluster has a large effect.

Pitfall five: skipping evaluation after taking action.

If we remove data by attribution score, we need to measure the model again. If we cite a source by corroborative score, we need to check whether the claim is truly supported. If we unlearn, we need to check both utility and forgetting.

So the most practical message of Part IV is: an attribution score is not the destination. It is a proposal for action, and that action must be checked.

Let us gather Part IV together.

Model debugging uses attribution to shorten the path from a specific failure to the data that needs inspection.

It also helps audit brittle predictions and train-test leakage, as long as we do not confuse semantic similarity with the real cause.

Dataset selection uses attribution to prioritize data that may improve the target behavior, or to detect data that should be acquired, cleaned, or removed from the pipeline.

Data valuation uses attribution to allocate credit to contributors or datasets, but it always depends on the utility, the context, and the fairness criteria we choose.

Data poisoning uses attribution to audit data with abnormal harmful influence, while reminding us that the score is dual-use: a score that helps defenders can also help attackers.

Machine unlearning uses attribution to predict and test the impact of forgetting a forget set, but attribution is not itself a certificate of unlearning.

Citation, RAG, and copyright use corroborative attribution to connect outputs with evidence candidates in the corpus, while also distinguishing support from faithful reliance.

These applications are very different, but they follow one shared principle.

Do not start from the method. Start from the application question.

Do you need evidence? Do you need credit? Or do you need to predict behavior after an intervention?

Once we can answer that, we know which lens, which estimator, and which evaluation to use.

That is also the final message of the whole tutorial: data attribution at scale is not a single score.

It is a disciplined way to ask questions about the relationship between data and model behavior.

In the epilogue, we will gather this picture into a short map: three lenses, two lessons about scale, and one principle for using attribution responsibly.
"""


def main() -> int:
    cues = build_cues(
        voice_script=VOICE_SCRIPT,
        english_text=ENGLISH_TEXT,
        audio_files=AUDIO_FILES,
        paragraph_counts=PARAGRAPH_COUNTS,
    )
    write_outputs(cues, OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
