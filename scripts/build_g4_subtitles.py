from __future__ import annotations

from exact_voice_subtitles import ROOT, build_cues, write_outputs


VOICE_SCRIPT = ROOT / "docs" / "part1_g4_predictive_voice_script_elevenlabs.txt"
OUTPUT = ROOT / "subtitles" / "part1_g4_predictive_bilingual.srt"
AUDIO_FILES = [
    "g4_00.mp3",
    "g4_01.mp3",
    "g4_02.mp3",
    "g4_03.mp3",
    "g4_04.mp3",
    "g4_05.mp3",
    "g4_06.mp3",
]
PARAGRAPH_COUNTS = [6, 5, 6, 7, 6, 6, 6]


ENGLISH_TEXT = """
In game-theoretic attribution, we asked: if many data points together create one utility, how should credit be divided?

Now we switch lenses one more time.

Predictive Attribution does not begin with the question of who deserves credit. It begins with a more practical question:

If the training data changes, how will model behavior change?

For example, if we remove a group of data from the training set, will accuracy drop sharply, increase slightly, or remain almost unchanged? If we add a new type of data, will the model hallucinate less, and will it become fairer?

In short, predictive attribution treats data like a control knob. When that knob is turned on, turned off, or reweighted, we want to predict how the model behavior will shift.

The key word here is counterfactual.

We do not only look at the current model and explain it with a score that sounds reasonable. We ask about another possible world: if the training data were not the same as before, what would happen?

Ideally, we could retrain the model many times. Once with the data unchanged. Once without data point i. Once without an entire subset. Once with a group of data upweighted. Then we compare behavior across those training runs.

But with modern machine learning, this approach is too expensive. Retraining a large model just to answer one small question is almost infeasible.

Therefore predictive attribution needs another idea: learn an auxiliary model that can predict counterfactual behavior without retraining the main model every time.

The most intuitive approach is to create many training subsets.

For each subset, we train or fine-tune the model, then measure its behavior on a validation set, a benchmark, or an important group of prompts.

Each subset is represented by a subset indicator: a vector of zeros and ones. A data point that is kept has a one in the corresponding position. A data point that is removed has a zero in that position.

Then each experiment creates a new data pair: the subset indicator as input, and model behavior as output.

For example, this vector may lead to accuracy 0.82. Another vector may lead to accuracy 0.76. A third vector may reduce loss, but make performance on edge cases worse.

We are learning a map: how the structure of the training subset relates to the behavior of the model.

That map is often called a datamodel.

The datamodel is not the main model we deploy. It is a surrogate: an auxiliary model that learns the relationship between training data and the behavior of the main model.

The input to the datamodel is the subset indicator. The output is the behavior we predict the main model would have if it were trained on that subset.

If the datamodel learns well, we can ask counterfactual questions much faster.

Instead of actually retraining the main model when removing data point i, we feed a new vector into the datamodel: the same as the original vector, but with the position of i turned off.

The datamodel predicts the new behavior. The difference between behavior before and after turning off i gives us an attribution signal.

This is why predictive attribution is not just "assigning scores to data." It is a prediction problem: predicting how the model will react when the data changes.

Once we have a datamodel, attribution can be understood as sensitivity.

If changing one data point changes the datamodel's prediction a lot, that data point has a large influence on the behavior being measured.

If turning that data point on or off barely changes the prediction, its attribution is small.

With a simple datamodel, for example a linear model, sensitivity can look like the coefficient of each data point.

But the meaning of the score always depends on the behavior we choose to measure. One data point may improve overall accuracy, but make performance worse on a sensitive group. Another data point may not improve accuracy much, but may be important for robustness.

Therefore in predictive attribution, the first question is always: which behavior are we trying to predict?

The strength of predictive attribution is that it can amortize cost.

We pay a large upfront cost to create many training subsets, measure behavior, and then learn the datamodel. After that, when we have many new questions, we do not necessarily have to retrain the main model from scratch. We use the datamodel to predict faster.

In return, predictive attribution has a very clear requirement: we must test its ability to predict counterfactuals.

If the datamodel says that removing a subset will reduce accuracy by five percent, but actual retraining shows that accuracy is almost unchanged, then attribution from that datamodel is not reliable yet.

In other words, with the predictive lens, a nice-looking score is not enough. The score must help predict behavior correctly in unseen situations.

This point connects directly to the later parts: theory, datamodels, scaling, and evaluation.

At this point, we have three main lenses for data attribution.

Corroborative attribution asks: what evidence supports this output?

Game-theoretic attribution asks: how should shared utility be credited to data points?

Predictive attribution asks: if the training data changes, how will model behavior change?

These three lenses do not compete with each other. They answer three different kinds of questions: evidence, credit, and counterfactual prediction.

The next part will go deeper into the foundations: M-estimation, leave-one-out, influence functions, and datamodels. That is where we start turning these intuitions into tools that can be computed at large scale.
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
