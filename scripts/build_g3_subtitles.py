from __future__ import annotations

from pathlib import Path

from exact_voice_subtitles import ROOT, build_cues, write_outputs


VOICE_SCRIPT = ROOT / "docs" / "part1_g3_game_theoretic_voice_script_elevenlabs.txt"
OUTPUT = ROOT / "subtitles" / "part1_g3_game_theoretic_bilingual.srt"
AUDIO_FILES = [
    "g3_00.mp3",
    "g3_01.mp3",
    "g3_02.mp3",
    "g3_04.mp3",
    "g3_05.mp3",
    "g3_06.mp3",
    "g3_07.mp3",
]
PARAGRAPH_COUNTS = [4, 5, 5, 6, 7, 5, 4]


ENGLISH_TEXT = """
After corroborative attribution, we move to a different kind of question.

In the previous part, we asked: what evidence supports this output? In other words, we trace the output back to sources that can make it more trustworthy.

But there are many situations where the evidence question is not enough. If a dataset helps the model improve accuracy, if a group of data lowers the loss, or if training data creates business value, we want to ask a different question: how should that credit be divided among the data points?

This is the intuition behind game-theoretic attribution: treating data as components that jointly contribute to a shared result, then finding a principled way to allocate credit instead of relying only on intuition.

In game-theoretic attribution, each data point is treated as a player in a cooperative game.

A group of players cooperating with each other forms a coalition, denoted S.

Then we assign this coalition a value, called utility, usually written as v of S.

Utility can be accuracy on a validation set, negative loss, revenue, or any quantity that says the model is improving according to the application's criterion.

The important point is: the game does not ask how similar a data point looks to the output. It asks how much that data point contributes to the shared utility.

The credit of a data point should not be measured in isolation.

We measure it using marginal contribution: if we already have a coalition S, then add data point i, how much does utility increase?

In formula form, delta of i in context S equals v of S union i, minus v of S.

If utility increases a lot, i has a large contribution in that context. If utility barely changes, i's contribution in that context is small.

This way of thinking is very natural. A training example only has value when we know which dataset it is being added to. A rare data point can be very important in a dataset that lacks similar examples, but less important in a dataset that is already highly redundant.

This is the point that is easiest to confuse.

The same data point can be very important in one context, but almost redundant in another context.

If the current coalition still lacks the kind of example that i provides, adding i can make utility increase sharply.

But if the coalition already has many examples very similar to i, then adding i only increases utility a little, or may not increase it at all.

Therefore, credit is not a fixed label attached to a data point. Credit depends on the coalition around it.

In short: to say how valuable a data point is, we must say in which context that value is measured.

So which context should we choose to measure contribution?

The Shapley value answers with a beautiful idea: do not choose a single context.

We imagine the data point being added in many different orders. In each order, when it is i's turn to appear, we measure the marginal contribution of i at that moment.

If i appears early, it may contribute a lot because the coalition before it is still small. If i appears late, the contribution may be lower because other data has already solved a similar part of the work.

Then we average these contributions across many orders.

The result is a more symmetric credit score: if two data points play the same role, they receive the same credit; if a point never helps utility, its credit is close to zero.

That is why the Shapley value is often considered an ideal standard for dividing credit.

The problem is scale.

To compute the Shapley value exactly, ideally we have to consider many coalitions, almost every way a data point can appear before or after others.

With n data points, the number of coalitions grows as two to the n.

When n equals four, we can still inspect the whole thing. But when n is one million, brute force is impossible.

Therefore in practice, game-theoretic attribution usually needs sampling, approximation, or special estimators to estimate credit without trying every coalition.

In short, game-theoretic attribution answers the question: how should credit be allocated?

The central tool is marginal contribution. The ideal standard is often the Shapley value. But when we move to large scale, we must accept approximation.

This lens is different from corroborative attribution. It does not ask which source supports the output, but asks how much the data contributes to utility.

Next, we move to the third lens: Predictive Attribution, where the question is no longer how to divide credit, but how to predict how the model will change if the training data changes.
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
