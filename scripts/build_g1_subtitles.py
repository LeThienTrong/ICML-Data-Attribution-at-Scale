from __future__ import annotations

from exact_voice_subtitles import ROOT, build_cues, read_paragraphs, write_outputs


VOICE_SCRIPT = ROOT / "docs" / "part1_g1_intro_taxonomy_voice_script_elevenlabs.txt"
OUTPUT = ROOT / "subtitles" / "part1_g1_intro_taxonomy_bilingual.srt"
AUDIO_FILES = ["g1_full_afterfixed.mp3"]
PARAGRAPH_COUNTS = [len(read_paragraphs(VOICE_SCRIPT))]


ENGLISH_TEXT = """
In this video, we enter a very basic question, but one that is becoming more and more important in machine learning: how has the training data affected the behavior of the model?

Usually, when we look at a model, we only see the input, the model in the middle, and an output on the other side. But the truly difficult part lies in the reverse direction.

When the model answers incorrectly, when the model produces a suspicious claim, or when the model performs unexpectedly well, we want to trace backward: which part of the data is related to that behavior?

That is the spirit of data attribution: connecting the behavior of the model to the training data, not by intuition, but through scores and procedures that can be checked.

Let us separate the problem into a simple loop.

Training data enters the training process. That process creates a model. Then the model creates behavior on a test case, such as an output, an error, an accuracy value, or a specific decision.

If we only look from left to right, we are doing ordinary machine learning. But data attribution asks us to look backward.

From an observed behavior, we ask: which data points explain this behavior, which points support it, which points receive credit, and which points would change the behavior if we removed them?

This video has four goals.

First, we build intuition for data attribution: why it is not just an auxiliary technique, but a way to ask questions about the responsibility of data.

Second, we distinguish different types of attribution. A score can measure evidence, it can measure credit, or it can measure the ability to predict behavior when data changes. These three are very easy to mix together.

Third, we connect the intuition to theory: M-estimation, leave-one-out, influence functions, and datamodels.

Finally, we look at why everything becomes harder at large scale, and how these ideas are used in debugging, dataset selection, poisoning, unlearning, citation, and RAG.

The roadmap of the video will follow four parts.

Part I is taxonomy. Here we do not try to choose one single definition for data attribution. We will ask: what kind of relation between behavior and data does the application need?

Part II goes into the theoretical foundations. We view the model as the solution of a weighted optimization problem, then ask what happens if the weight of one data point changes.

Part III talks about scaling. Ideas that are beautiful on paper can become very expensive when the dataset has millions of points and the model has billions of parameters.

Part IV returns to applications. Once we have an attribution score, we use it to debug the model, select data, detect harmful data, or explain the sources supporting an output.

Data problems in ML look very different from the outside.

In debugging, we want to know which data is related to a specific error. In trust and citation, we want to know which sources support an output. In dataset selection, we want to choose data that makes the model better.

In data valuation, we want to know who should receive credit. In copyright detection, we want to know whether an output is too similar to original data. In poisoning and security, we want to find the data points that make the model drift.

But behind those problems is the same structure: we observe a behavior of the model, then try to relate that behavior to training data or to an available corpus.

The important point is that the word "relate" here does not have only one meaning.

A data point can be good evidence for an output, but that does not mean it caused the output in a causal sense.

A data point can deserve credit in a utility function, but it is not necessarily the closest passage semantically.

And a data point can strongly change behavior if we remove it, even if it does not look like the output at all.

Therefore, before using an attribution score, we must ask: what relation is this score measuring?

We will use three main lenses.

The first lens is corroborative attribution. The question is: is there any evidence in the corpus that supports this output? This is a very natural lens for citation, retrieval, and copyright detection.

The second lens is game-theoretic attribution. The question is: if we treat data as players that jointly create utility, how should credit be divided?

The third lens is predictive attribution. The question is: if the training data changes, how will the behavior of the model change? This lens leads us to datamodels and counterfactual prediction.

These three lenses are related, but they do not replace one another. Using the wrong lens can make us interpret a score incorrectly.

The stopping point of G1 is the first lens: evidence.

In the next segment, we do not need to solve the entire attribution problem yet. We focus only on a lighter question: is an output supported by data or not?

That is the doorway into corroborative attribution.

The details about corpus, score, ranking, and evidence candidates will be saved for G2, where we move from taxonomy to a concrete mechanism.
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
