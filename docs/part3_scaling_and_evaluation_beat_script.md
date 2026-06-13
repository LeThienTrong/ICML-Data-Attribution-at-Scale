# Part 3 - Scaling and Evaluation Visual Beat Scaffold

This file is no longer the official audio script.

Use `docs/part3_scaling_and_evaluation_voice_script_elevenlabs.txt` to create the real audio files `p3_00.mp3` through `p3_11.mp3`.

The beat entries below are kept only as a Manim visual scaffold. They let the long Part 3 scene change visuals inside each long audio section, so the video does not freeze on one slide for minutes. Do not copy this file into ElevenLabs as the main voice script.

## p3_00_01 - Part III mở vấn đề scale
Audio: assets/audio/p3_00_01.mp3
Voice VI: Ở Part II, ta đã có theory khá sạch cho predictive attribution.
Subtitle EN: In Part II, we built a clean theory for predictive attribution.
Visual: Collapse Part II blocks into one small theory stack.
Must show: Part II; predictive attribution; theory

## p3_00_02 - Những khối theory cũ
Audio: assets/audio/p3_00_02.mp3
Voice VI: Ta có weights, leave-one-out, influence function, và datamodels.
Subtitle EN: We have weights, leave-one-out, influence functions, and datamodels.
Visual: Four blocks appear: weights, LOO, IF, datamodels.
Must show: weights; LOO; IF; datamodels

## p3_00_03 - Khi toy problem thành modern ML
Audio: assets/audio/p3_00_03.mp3
Voice VI: Nhưng chữ "at scale" làm mọi thứ đổi bản chất.
Subtitle EN: But the phrase "at scale" changes the nature of the problem.
Visual: Small toy dataset expands into a huge data cloud.
Must show: at scale; toy to large

## p3_00_04 - Data và model đều lớn
Audio: assets/audio/p3_00_04.mp3
Voice VI: Dataset có thể có hàng triệu examples, model có hàng tỷ parameters.
Subtitle EN: The dataset may have millions of examples, and the model billions of parameters.
Visual: Data dots and parameter bars grow dramatically.
Must show: millions of examples; billions of parameters

## p3_00_05 - Behavior không còn một số
Audio: assets/audio/p3_00_05.mp3
Voice VI: Behavior cũng không chỉ là một số, mà là rất nhiều target khác nhau.
Subtitle EN: Behavior is no longer one number, but many different targets.
Visual: One output splits into prompts, groups, metrics, and probabilities.
Must show: behavior; many targets

## p3_00_06 - Câu hỏi của Part III
Audio: assets/audio/p3_00_06.mp3
Voice VI: Part III hỏi: estimator nào còn dự đoán đúng khi mọi thứ lớn và noisy?
Subtitle EN: Part III asks which estimator still predicts well when everything is large and noisy.
Visual: A question mark connects estimator to noisy large-scale ML.
Must show: estimator; noisy; prediction

## p3_01_01 - Ba trục scale
Audio: assets/audio/p3_01_01.mp3
Voice VI: Hãy tách scaling thành ba trục: n, p, và m.
Subtitle EN: Let us split scaling into three axes: n, p, and m.
Visual: Three axes grow from the center.
Must show: n; p; m

## p3_01_02 - Trục n
Audio: assets/audio/p3_01_02.mp3
Voice VI: n là số training points, và exact leave-one-out cần n lần retraining.
Subtitle EN: n is the number of training points, and exact leave-one-out needs n retrains.
Visual: n dots each trigger a retraining loop.
Must show: n; leave-one-out; n retrains

## p3_01_03 - Mọi subset là bất khả thi
Audio: assets/audio/p3_01_03.mp3
Voice VI: Nếu xét mọi subset, số khả năng không phải n, mà là hai mũ n.
Subtitle EN: If we consider all subsets, the count is not n, but two to the n.
Visual: Subset tree explodes into 2^n leaves.
Must show: 2^n; subsets

## p3_01_04 - Trục p
Audio: assets/audio/p3_01_04.mp3
Voice VI: p là số parameters, và Hessian đầy đủ có kích thước p nhân p.
Subtitle EN: p is the number of parameters, and the full Hessian has size p by p.
Visual: Parameter vector expands into a p by p matrix.
Must show: p; Hessian; p x p

## p3_01_05 - Hessian không thể lưu
Audio: assets/audio/p3_01_05.mp3
Voice VI: Với neural network lớn, lưu và đảo Hessian đầy đủ gần như không thực tế.
Subtitle EN: For large neural networks, storing and inverting the full Hessian is unrealistic.
Visual: Hessian matrix becomes too large and compresses into HVP.
Must show: H^{-1}; HVP; memory

## p3_01_06 - Trục m
Audio: assets/audio/p3_01_06.mp3
Voice VI: m là số target behaviors: image, prompt, class, subgroup, hoặc metric.
Subtitle EN: m is the number of target behaviors: image, prompt, class, subgroup, or metric.
Visual: One model output splits into five target icons.
Must show: m; target behaviors

## p3_01_07 - Câu hỏi thực tế
Audio: assets/audio/p3_01_07.mp3
Voice VI: Câu hỏi thực tế là: behavior nào, độ phân giải nào, và compute bao nhiêu?
Subtitle EN: The practical question is which behavior, which resolution, and how much compute.
Visual: A decision board shows behavior, resolution, and compute.
Must show: behavior; resolution; compute

## p3_02_01 - Ground truth không đơn giản
Audio: assets/audio/p3_02_01.mp3
Voice VI: Trước khi chọn estimator, ta phải định nghĩa counterfactual ground truth.
Subtitle EN: Before choosing an estimator, we must define the counterfactual ground truth.
Visual: Ground truth label appears with a warning marker.
Must show: counterfactual; ground truth

## p3_02_02 - Retraining có randomness
Audio: assets/audio/p3_02_02.mp3
Voice VI: Cùng data nhưng seed, order, augmentation, hoặc checkpoint khác có thể đổi behavior.
Subtitle EN: The same data can behave differently with another seed, order, augmentation, or checkpoint.
Visual: One dataset forks into several training paths.
Must show: seed; checkpoint; randomness

## p3_02_03 - Protocol phải rõ
Audio: assets/audio/p3_02_03.mp3
Voice VI: Vì vậy evaluation phải ghi rõ retrain, fine-tune, seed, checkpoint, và metric.
Subtitle EN: So evaluation must specify retraining, fine-tuning, seed, checkpoint, and metric.
Visual: Protocol checklist fills in one item at a time.
Must show: protocol; metric

## p3_02_04 - Không cùng counterfactual là không công bằng
Audio: assets/audio/p3_02_04.mp3
Voice VI: Nếu estimator và benchmark đo hai counterfactual khác nhau, so sánh sẽ lệch.
Subtitle EN: If estimator and benchmark measure different counterfactuals, comparison is biased.
Visual: Two mismatched arrows point to different targets.
Must show: estimator; benchmark; mismatch

## p3_02_05 - Nguyên tắc nền
Audio: assets/audio/p3_02_05.mp3
Voice VI: Nguyên tắc là: định nghĩa counterfactual trước, rồi mới đánh giá estimator.
Subtitle EN: The rule is to define the counterfactual first, then evaluate the estimator.
Visual: Counterfactual definition locks before estimator scoring.
Must show: define first; evaluate second

## p3_03_01 - IF ở scale lớn
Audio: assets/audio/p3_03_01.mp3
Voice VI: Influence function hấp dẫn vì chỉ cần một trained model.
Subtitle EN: Influence functions are attractive because they need only one trained model.
Visual: One trained model emits influence arrows.
Must show: influence function; one model

## p3_03_02 - Công thức behavior influence
Audio: assets/audio/p3_03_02.mp3
Voice VI: Trực giác là gradient behavior, nhân inverse Hessian, nhân gradient sample.
Subtitle EN: The intuition is behavior gradient, inverse Hessian, and sample gradient.
Visual: Formula pieces assemble into a chain.
Must show: grad behavior; H^{-1}; grad sample

## p3_03_03 - Nút thắt Hessian
Audio: assets/audio/p3_03_03.mp3
Voice VI: Nút thắt là inverse Hessian, vì H quá lớn để materialize.
Subtitle EN: The bottleneck is the inverse Hessian, because H is too large to materialize.
Visual: H matrix grows and turns red.
Must show: inverse Hessian; bottleneck

## p3_03_04 - HVP và solver
Audio: assets/audio/p3_03_04.mp3
Voice VI: Thực tế thường dùng Hessian-vector product, conjugate gradient, hoặc LiSSA.
Subtitle EN: In practice we use Hessian-vector products, conjugate gradient, or LiSSA.
Visual: H^{-1} block becomes HVP, CG, and LiSSA chips.
Must show: HVP; CG; LiSSA

## p3_03_05 - Gradient similarity là bản rẻ hơn
Audio: assets/audio/p3_03_05.mp3
Voice VI: Nếu bỏ curvature, ta có gradient similarity: rẻ hơn nhưng thô hơn.
Subtitle EN: If we drop curvature, we get gradient similarity: cheaper but rougher.
Visual: Curvature layer fades out, leaving a gradient dot product.
Must show: gradient similarity; cheaper; rougher

## p3_03_06 - Tradeoff của IF
Audio: assets/audio/p3_03_06.mp3
Voice VI: Càng giữ nhiều geometry, càng gần theory; càng bỏ nhiều, càng cần evaluation.
Subtitle EN: More geometry means closer theory; less geometry means stronger evaluation is needed.
Visual: A slider moves between theory and evaluation.
Must show: geometry; theory; evaluation

## p3_04_01 - Training dynamics
Audio: assets/audio/p3_04_01.mp3
Voice VI: Một hướng khác là nhìn vào training dynamics, không chỉ model cuối.
Subtitle EN: Another direction is to inspect training dynamics, not just the final model.
Visual: A training trajectory appears with checkpoint dots.
Must show: training dynamics; checkpoints

## p3_04_02 - TracIn
Audio: assets/audio/p3_04_02.mp3
Voice VI: TracIn đo sample z ảnh hưởng target qua nhiều checkpoints.
Subtitle EN: TracIn measures how sample z affects the target across checkpoints.
Visual: Sample z sends signals at each checkpoint.
Must show: TracIn; z; target

## p3_04_03 - Dot product gradient
Audio: assets/audio/p3_04_03.mp3
Voice VI: Score là tổng các dot product giữa gradient target và gradient sample.
Subtitle EN: The score is a sum of dot products between target and sample gradients.
Visual: Gradient arrows meet and form dot products.
Must show: gradient dot product; sum

## p3_04_04 - Điểm mạnh của TracIn
Audio: assets/audio/p3_04_04.mp3
Voice VI: Điểm mạnh là không cần inverse Hessian, chỉ cần gradients và checkpoints.
Subtitle EN: Its strength is that it needs no inverse Hessian, only gradients and checkpoints.
Visual: H^{-1} is crossed out; checkpoints glow.
Must show: no H^{-1}; gradients; checkpoints

## p3_04_05 - Giới hạn của TracIn
Audio: assets/audio/p3_04_05.mp3
Voice VI: Nhưng kết quả phụ thuộc checkpoint, loss scale, và optimizer path.
Subtitle EN: But results depend on checkpoints, loss scale, and the optimizer path.
Visual: Three warning chips attach to the trajectory.
Must show: checkpoint; loss scale; optimizer path

## p3_05_01 - TRAK là gì
Audio: assets/audio/p3_05_01.mp3
Voice VI: TRAK là một method quan trọng cho behavior attribution at scale.
Subtitle EN: TRAK is an important method for behavior attribution at scale.
Visual: TRAK title appears over a large differentiable model.
Must show: TRAK; behavior attribution

## p3_05_02 - After-kernel
Audio: assets/audio/p3_05_02.mp3
Voice VI: Nó linearize model thành một surrogate kiểu after-kernel.
Subtitle EN: It linearizes the model into an after-kernel style surrogate.
Visual: A neural model unfolds into kernel features.
Must show: linearization; after-kernel; surrogate

## p3_05_03 - Random projection
Audio: assets/audio/p3_05_03.mp3
Voice VI: Gradient features rất lớn, nên TRAK dùng random projection để nén.
Subtitle EN: Gradient features are huge, so TRAK uses random projection to compress them.
Visual: Wide gradient vectors pass through a random projection funnel.
Must show: gradient features; random projection

## p3_05_04 - Vị trí của TRAK
Audio: assets/audio/p3_05_04.mp3
Voice VI: TRAK đứng giữa gradient baseline rẻ và datamodels rất đắt.
Subtitle EN: TRAK sits between cheap gradient baselines and expensive datamodels.
Visual: TRAK dot appears between two extremes on a cost axis.
Must show: gradient baseline; TRAK; datamodels

## p3_05_05 - Ranking hơn calibration
Audio: assets/audio/p3_05_05.mp3
Voice VI: Ở scale lớn, ranking top examples đôi khi quan trọng hơn calibration tuyệt đối.
Subtitle EN: At scale, ranking top examples can matter more than absolute calibration.
Visual: Ranked training examples reorder by score.
Must show: ranking; calibration

## p3_05_06 - TRAK vẫn là estimator
Audio: assets/audio/p3_05_06.mp3
Voice VI: Nhưng TRAK vẫn là estimator, nên phải kiểm tra bằng counterfactual.
Subtitle EN: But TRAK is still an estimator, so it must be tested by counterfactuals.
Visual: TRAK score is sent into a counterfactual test box.
Must show: estimator; counterfactual test

## p3_06_01 - Datamodels
Audio: assets/audio/p3_06_01.mp3
Voice VI: Datamodels đi gần hơn với brute force counterfactual.
Subtitle EN: Datamodels move closer to brute-force counterfactuals.
Visual: Many subsets feed into many training runs.
Must show: datamodels; subsets; training runs

## p3_06_02 - Subset to behavior
Audio: assets/audio/p3_06_02.mp3
Voice VI: Input là subset indicator, output là behavior sau khi train trên subset đó.
Subtitle EN: The input is a subset indicator; the output is behavior after training on it.
Visual: Binary mask flows into a behavior meter.
Must show: subset indicator; behavior

## p3_06_03 - Linear datamodel
Audio: assets/audio/p3_06_03.mp3
Voice VI: Với linear datamodel, behavior được dự đoán bằng tổng các coefficient.
Subtitle EN: With a linear datamodel, behavior is predicted by summing coefficients.
Visual: Linear formula appears beside coefficient bars.
Must show: linear datamodel; coefficients

## p3_06_04 - Điểm mạnh
Audio: assets/audio/p3_06_04.mp3
Voice VI: Điểm mạnh là học trực tiếp relation giữa data và behavior.
Subtitle EN: Its strength is directly learning the relation between data and behavior.
Visual: Data subsets connect directly to measured behavior.
Must show: data; behavior; direct relation

## p3_06_05 - Chi phí upfront
Audio: assets/audio/p3_06_05.mp3
Voice VI: Điểm yếu là chi phí upfront: nhiều runs, nhiều subsets, nhiều measurements.
Subtitle EN: Its weakness is upfront cost: many runs, subsets, and measurements.
Visual: Cost bar grows beside training run icons.
Must show: upfront cost; many runs

## p3_06_06 - Khi nào hợp
Audio: assets/audio/p3_06_06.mp3
Voice VI: Datamodels hợp khi ta amortize cost cho nhiều counterfactual queries.
Subtitle EN: Datamodels fit when we amortize cost across many counterfactual queries.
Visual: One expensive dataset of runs answers many future queries.
Must show: amortize; counterfactual queries

## p3_07_01 - Method landscape
Audio: assets/audio/p3_07_01.mp3
Voice VI: Vậy nên dùng method nào? Hãy nhìn landscape accuracy và cost.
Subtitle EN: So which method should we use? Look at the accuracy and cost landscape.
Visual: A two-axis landscape appears: cost and counterfactual accuracy.
Must show: accuracy; cost; landscape

## p3_07_02 - Similarity methods
Audio: assets/audio/p3_07_02.mp3
Voice VI: Similarity methods rất rẻ, nhưng thường chỉ nói data nào giống target.
Subtitle EN: Similarity methods are cheap, but often only say which data resembles the target.
Visual: Similar examples cluster near a target point.
Must show: similarity; cheap; target

## p3_07_03 - Gradient và TracIn
Audio: assets/audio/p3_07_03.mp3
Voice VI: Gradient similarity và TracIn bám vào learning hơn, nhưng vẫn là xấp xỉ.
Subtitle EN: Gradient similarity and TracIn follow learning more closely, but remain approximations.
Visual: Gradient and checkpoint dots move upward on the landscape.
Must show: gradient similarity; TracIn; approximation

## p3_07_04 - Influence functions
Audio: assets/audio/p3_07_04.mp3
Voice VI: Influence functions thêm Hessian, đẹp về theory nhưng dễ gãy với DNN.
Subtitle EN: Influence functions add the Hessian: elegant in theory, fragile for DNNs.
Visual: IF dot shows a Hessian badge and a warning icon.
Must show: IF; Hessian; DNN fragile

## p3_07_05 - TRAK ở giữa
Audio: assets/audio/p3_07_05.mp3
Voice VI: TRAK cố giữ vùng giữa: scalable hơn, nhưng vẫn nhắm behavior.
Subtitle EN: TRAK tries to occupy the middle: more scalable, still behavior-focused.
Visual: TRAK dot sits in the middle of the landscape.
Must show: TRAK; scalable; behavior

## p3_07_06 - Shapley và datamodels
Audio: assets/audio/p3_07_06.mp3
Voice VI: Shapley và datamodels gần counterfactual hơn, nhưng compute lớn hơn.
Subtitle EN: Shapley and datamodels are closer to counterfactuals, but cost more compute.
Visual: Datamodel and Shapley dots move high and right.
Must show: Shapley; datamodels; compute

## p3_07_07 - Cách chọn method
Audio: assets/audio/p3_07_07.mp3
Voice VI: Hãy chọn theo use case: ranking, magnitude, target count, và ngân sách compute.
Subtitle EN: Choose by use case: ranking, magnitude, target count, and compute budget.
Visual: A selector cycles through four decision chips.
Must show: use case; ranking; magnitude; budget

## p3_08_01 - Evaluation là trọng tâm
Audio: assets/audio/p3_08_01.mp3
Voice VI: Phần quan trọng nhất của Part III là counterfactual evaluation.
Subtitle EN: The most important part of Part III is counterfactual evaluation.
Visual: Evaluation title appears over predicted vs actual axes.
Must show: counterfactual evaluation

## p3_08_02 - Score phải dự đoán behavior
Audio: assets/audio/p3_08_02.mp3
Voice VI: Một score chỉ đáng tin khi nó dự đoán được behavior sau intervention.
Subtitle EN: A score is trustworthy only if it predicts behavior after intervention.
Visual: Score arrow predicts a post-intervention behavior meter.
Must show: score; intervention; behavior

## p3_08_03 - Bốn bước evaluation
Audio: assets/audio/p3_08_03.mp3
Voice VI: Ta chọn intervention, dự đoán delta, chạy counterfactual, rồi so sánh.
Subtitle EN: We choose an intervention, predict delta, run the counterfactual, then compare.
Visual: Four-step pipeline animates from left to right.
Must show: intervention; predicted delta; actual delta

## p3_08_04 - Calibration
Audio: assets/audio/p3_08_04.mp3
Voice VI: Nếu cần magnitude, hãy đo calibration, error, hoặc R squared.
Subtitle EN: If we need magnitude, measure calibration, error, or R squared.
Visual: Predicted vs actual scatter aligns with a diagonal.
Must show: calibration; error; R squared

## p3_08_05 - Ranking
Audio: assets/audio/p3_08_05.mp3
Voice VI: Nếu cần ranking, hãy đo Spearman, Kendall, hoặc top-k overlap.
Subtitle EN: If we need ranking, measure Spearman, Kendall, or top-k overlap.
Visual: Top-k bars reorder and overlap.
Must show: Spearman; Kendall; top-k

## p3_08_06 - Direction
Audio: assets/audio/p3_08_06.mp3
Voice VI: Nếu cần quyết định hành động, sign accuracy thường rất quan trọng.
Subtitle EN: If we need to act, sign accuracy is often crucial.
Visual: Positive and negative arrows are checked or rejected.
Must show: sign accuracy; action

## p3_08_07 - LDS trực giác
Audio: assets/audio/p3_08_07.mp3
Voice VI: LDS hỏi: tổng attribution scores có dự đoán behavior của subset không?
Subtitle EN: LDS asks whether summed attribution scores predict subset behavior.
Visual: Subset mask sums scores and predicts behavior.
Must show: LDS; sum attribution scores; subset behavior

## p3_08_08 - LDS công thức
Audio: assets/audio/p3_08_08.mp3
Voice VI: Ta so sánh y hat của subset với actual behavior trên held-out subsets.
Subtitle EN: We compare subset y-hat with actual behavior on held-out subsets.
Visual: Formula y_hat(S) versus y(S) appears with correlation.
Must show: y_hat(S); y(S); held-out subsets

## p3_08_09 - LDS có giới hạn
Audio: assets/audio/p3_08_09.mp3
Voice VI: LDS hữu ích, nhưng tuyến tính nên có thể bỏ sót interaction.
Subtitle EN: LDS is useful, but linear, so it can miss interactions.
Visual: Linear sum misses an interaction arc between two data points.
Must show: linear; interaction

## p3_09_01 - Failure modes
Audio: assets/audio/p3_09_01.mp3
Voice VI: Ở scale lớn, attribution rất dễ đẹp mắt nhưng sai.
Subtitle EN: At scale, attribution can look convincing and still be wrong.
Visual: A polished heatmap cracks into warning signs.
Must show: failure modes; warning

## p3_09_02 - Duplicates
Audio: assets/audio/p3_09_02.mp3
Voice VI: Duplicate data có thể làm single-point removal nhìn yếu hơn thực tế.
Subtitle EN: Duplicate data can make single-point removal look weaker than it really is.
Visual: Duplicate samples share the same signal.
Must show: duplicates; single-point removal

## p3_09_03 - Correlated data
Audio: assets/audio/p3_09_03.mp3
Voice VI: Correlated data khiến point-level score bỏ lỡ group-level structure.
Subtitle EN: Correlated data makes point-level scores miss group-level structure.
Visual: Points form a cluster with a group outline.
Must show: correlated data; group-level

## p3_09_04 - Target mismatch
Audio: assets/audio/p3_09_04.mp3
Voice VI: Target mismatch xảy ra khi score đo loss nhưng ứng dụng cần fairness.
Subtitle EN: Target mismatch happens when the score measures loss but the app needs fairness.
Visual: Loss target and fairness target pull in different directions.
Must show: target mismatch; loss; fairness

## p3_09_05 - Seed noise
Audio: assets/audio/p3_09_05.mp3
Voice VI: Seed noise làm actual counterfactual có variance, nhất là khi effect nhỏ.
Subtitle EN: Seed noise gives actual counterfactuals variance, especially for small effects.
Visual: Multiple retraining dots scatter around one mean.
Must show: seed noise; variance

## p3_09_06 - Hygiene
Audio: assets/audio/p3_09_06.mp3
Voice VI: Hygiene tốt là ghi rõ target, intervention, seed, và metric.
Subtitle EN: Good hygiene states the target, intervention, seed, and metric clearly.
Visual: A final checklist locks in four fields.
Must show: target; intervention; seed; metric

## p3_10_01 - Future work
Audio: assets/audio/p3_10_01.mp3
Voice VI: Data attribution at scale vẫn là một bài toán mở.
Subtitle EN: Data attribution at scale is still an open problem.
Visual: Five research doors appear.
Must show: future work; open problem

## p3_10_02 - Beyond linear
Audio: assets/audio/p3_10_02.mp3
Voice VI: Hướng thứ nhất là beyond linear, vì data không luôn cộng tuyến tính.
Subtitle EN: The first direction is beyond linear, because data is not always additive.
Visual: Linear sum bends into interaction curves.
Must show: beyond linear; interaction

## p3_10_03 - Interaction
Audio: assets/audio/p3_10_03.mp3
Voice VI: Hai examples có thể chỉ hữu ích khi đi cùng nhau.
Subtitle EN: Two examples may be useful only when they appear together.
Visual: Two data points combine to unlock a behavior.
Must show: pair interaction

## p3_10_04 - Multiple stages
Audio: assets/audio/p3_10_04.mp3
Voice VI: Hướng thứ hai là attribution cho pipeline nhiều stage.
Subtitle EN: The second direction is attribution for multi-stage pipelines.
Visual: Pretrain, filter, SFT, alignment, and RAG stages appear.
Must show: multiple stages; pipeline

## p3_10_05 - Better surrogate
Audio: assets/audio/p3_10_05.mp3
Voice VI: Hướng thứ ba là better surrogate: đủ expressive nhưng vẫn rẻ.
Subtitle EN: The third direction is a better surrogate: expressive but still cheap.
Visual: Surrogate choices line up from linear to neural.
Must show: better surrogate; expressive; cheap

## p3_10_06 - Single-model counterfactual
Audio: assets/audio/p3_10_06.mp3
Voice VI: Hướng thứ tư là dự đoán counterfactual từ một hoặc vài trained models.
Subtitle EN: The fourth direction is predicting counterfactuals from one or a few trained models.
Visual: One model predicts several data removal outcomes.
Must show: single-model counterfactual; few models

## p3_10_07 - Efficient proxies
Audio: assets/audio/p3_10_07.mp3
Voice VI: Hướng thứ năm là proxy rẻ nhưng được evaluate đúng.
Subtitle EN: The fifth direction is cheap proxies that are evaluated correctly.
Visual: A proxy filter selects candidates for deeper testing.
Must show: efficient proxies; evaluated correctly

## p3_10_08 - Mục tiêu future work
Audio: assets/audio/p3_10_08.mp3
Voice VI: Mục tiêu là approximation đủ đúng, đủ rẻ, và biết khi nào không nên tin.
Subtitle EN: The goal is an approximation that is accurate, cheap, and knows its limits.
Visual: Accuracy, cost, and trust meters balance.
Must show: accurate; cheap; limits

## p3_11_01 - Takeaway một
Audio: assets/audio/p3_11_01.mp3
Voice VI: Takeaway một: scale làm đổi bản chất bài toán.
Subtitle EN: Takeaway one: scale changes the nature of the problem.
Visual: Scale axis transforms the original problem.
Must show: scale changes problem

## p3_11_02 - Takeaway hai
Audio: assets/audio/p3_11_02.mp3
Voice VI: Takeaway hai: mọi scalable method đều là estimator.
Subtitle EN: Takeaway two: every scalable method is an estimator.
Visual: Methods collapse into one estimator label.
Must show: scalable method; estimator

## p3_11_03 - Takeaway ba
Audio: assets/audio/p3_11_03.mp3
Voice VI: Takeaway ba: score đẹp chưa đủ, phải qua counterfactual evaluation.
Subtitle EN: Takeaway three: a pretty score is not enough; it needs counterfactual evaluation.
Visual: A score passes through an evaluation gate.
Must show: score; counterfactual evaluation

## p3_11_04 - Takeaway bốn
Audio: assets/audio/p3_11_04.mp3
Voice VI: Takeaway bốn: method tốt phụ thuộc use case và compute budget.
Subtitle EN: Takeaway four: the right method depends on use case and compute budget.
Visual: Use case and compute budget select different methods.
Must show: use case; compute budget

## p3_11_05 - Chuyển sang applications
Audio: assets/audio/p3_11_05.mp3
Voice VI: Part IV sẽ hỏi: attribution giúp ta debug, chọn data, và unlearn như thế nào?
Subtitle EN: Part IV asks how attribution helps us debug, select data, and unlearn.
Visual: Arrow moves from evaluation to applications.
Must show: Part IV; debug; data selection; unlearning
