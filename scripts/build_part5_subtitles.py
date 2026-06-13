from __future__ import annotations

from exact_voice_subtitles import ROOT, build_cues, write_outputs


VOICE_SCRIPT = ROOT / "docs" / "part5_epilogue_recap_voice_script_elevenlabs.txt"
OUTPUT = ROOT / "subtitles" / "part5_epilogue_recap_bilingual.srt"
AUDIO_FILES = [
    "p5_00.mp3",
    "p5_01.mp3",
    "p5_02.mp3",
    "p5_03.mp3",
    "p5_04.mp3",
    "p5_05.mp3",
]
PARAGRAPH_COUNTS = [9, 11, 13, 11, 13, 12]


ENGLISH_TEXT = """
By now, we have gone through almost the whole main picture of data attribution at scale.

This epilogue will not add a new method.

It does just one thing: gather everything into a map short enough to carry with you after the video ends.

In one sentence, data attribution is not about finding a magical number for each training example.

It is a disciplined way to ask about the relationship between training data and model behavior.

We do not ask vaguely: which data is most important?

We ask more specifically: important for which behavior? Under which intervention? With which data unit? And how will that score be checked by evaluation?

Asked this way, data attribution looks less like a mysterious ranking, and more like a tool for thinking clearly.

In this final part, keep three things: three lenses, two lessons about scale, and one principle for using attribution responsibly.

We started in Part I with the taxonomy.

Corroborative attribution asks: what evidence supports this output?

Game-theoretic attribution asks: if many data points create one utility together, how should credit be divided?

Predictive attribution asks: if the training data changes, how will model behavior change?

These three questions can sound similar if we simply call all of them attribution, but they are different in nature.

In Part II, we moved into the theoretical foundation.

We viewed data weight like a knob: increase, decrease, or remove one data point, then observe how the optimum and behavior change. Leave-one-out is a clean but expensive counterfactual; influence function is an approximation based on gradient and Hessian; datamodels learn a surrogate from subset indicators to behavior.

In Part III, we faced scale.

Modern ML is not only more data; it also means larger models, noisier training, more target behaviors, and higher retraining cost. So every estimator at scale is a tradeoff between cost, assumption, and accuracy.

And in Part IV, we saw that attribution only becomes meaningful inside applications: debugging, dataset selection, data valuation, poisoning, unlearning, citation, RAG, and copyright-related analysis.

These four parts are connected by one idea: the application decides the attribution question.

The first lens is evidence.

This is the lens of corroborative attribution.

When we ask which source supports an answer, whether a citation is correct, or whether an output is too close to a document in the corpus, we are asking about evidence. But evidence is not automatically cause.

The second lens is credit.

This is the lens of game-theoretic attribution.

When we ask how much credit a contributor, a dataset, or a data point should receive for a utility, we must define the utility first. Credit is not the absolute value of data in every situation; it is contribution in a specific context.

The third lens is prediction.

This is the lens of predictive attribution.

When we ask how behavior would change if we remove a subset, add a data group, or upweight a cluster, we are asking about counterfactual prediction. Here, a score is trustworthy only when it predicts behavior correctly outside the data used to fit the estimator.

If you need to remember it in three lines, remember this.

Evidence answers: what supports the output?

Credit answers: how should utility be divided?

Prediction answers: how will a data intervention change behavior?

The first lesson about scale is: clean counterfactuals are often expensive.

Leave-one-out sounds very natural: remove one data point, retrain the model, and measure behavior. But if there are millions of data points, we cannot retrain millions of times. Shapley value is also elegant, but the number of coalitions grows exponentially.

So at large scale, almost every method is a form of approximation.

Influence function linearizes around the optimum. TracIn looks at the training trajectory. TRAK uses projection to scale behavior attribution. Datamodels pay an upfront cost with many training runs to predict counterfactuals faster.

No method is free.

Each method buys speed with an assumption, a proxy, or a kind of evaluation that must be checked.

The second lesson is: evaluation is not an appendix.

Evaluation is part of the method definition.

If a score is used for debugging, we check whether the top-k examples help diagnose the failure. If it is used for data selection, we check the model after training on the chosen subset. If it is used for unlearning, we check utility, forgetting, and privacy. If it is used for citation, we check support and faithfulness.

A plausible-looking attribution score is not enough.

At scale, the question is not "does this score look elegant?", but "does this score predict or support the right decision in the setting we care about?"

The final principle is: do not start from the method; start from the application question.

Before choosing influence function, TRAK, datamodels, Shapley value, or retrieval similarity, write the question clearly.

One: which behavior is being explained or predicted?

Two: what is the data unit? Document, paragraph, image, user record, prompt-response pair, cluster, or whole dataset?

Three: what is the intervention? Remove, downweight, add, relabel, deduplicate, or retrain without a forget set?

Four: what is the notion of attribution? Evidence, credit, or prediction?

Five: who is allowed to see the score, and can the score be misused?

This is especially important in security, privacy, copyright, and data governance.

A score strong enough to help a defender find poisoning can also help an attacker optimize an attack. A citation score can create false certainty if the claim is not checked. An unlearning score used for triage should not be presented as proof that the model has forgotten.

Six: what evaluation will decide that this score is usable?

Without answers to these six questions, attribution can easily become a number that looks scientific but does not lead to the right decision.

Responsible attribution does not mean refusing to use scores.

It means using scores with the right lens, the right limits, the right audience, and the right evaluation.

So if you keep only three sentences after this video, keep these three.

Evidence is not cause.

Credit is utility-dependent.

Prediction must be evaluated counterfactually.

Those three sentences sound simple, but they prevent many mistakes when using data attribution in practice.

When debugging hallucination, ask whether the document is evidence, a cause, or only a neighbor in embedding space. When allocating credit to data contributors, ask what the utility, context, and fairness criteria are. When removing, selecting, or unlearning data, ask whether the counterfactual behavior is predicted correctly.

That is the spirit of data attribution at scale.

Not a magic score, and not a final ranking. It is a way to make the relationship between training data and model behavior clearer, more testable, and more responsible.

This video is based on the ICML 2024 Tutorial: Data Attribution at Scale, along with major ideas about influence functions, data valuation, datamodels, scalable attribution, counterfactual evaluation, and applications in modern ML.

If Part I gave us the language, Part II gave us the foundation, Part III gave us the scale problem, and Part IV gave us the applications, then Part V is here to repeat one thing:

Before asking which data is important, ask important in what sense.

And that is where data attribution truly begins.
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
