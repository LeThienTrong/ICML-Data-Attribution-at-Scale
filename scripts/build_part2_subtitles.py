from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOICE_SCRIPT = ROOT / "docs" / "part2_core_theory_voice_script.md"
ENGLISH_LINES = ROOT / "subtitles" / "part2_core_theory_english_lines.txt"
MAX_VI_CHARS = 92

SEGMENT_DURATIONS = [
    71.419,
    102.217,
    78.106,
    69.982,
    62.119,
    64.183,
    65.437,
    113.868,
    92.918,
    98.900,
    72.986,
    99.709,
    107.128,
]

SEGMENTS = [
    [
        ("Ở Part I, ta đã có ba lens để nhìn data attribution.", "In Part I, we had three lenses for data attribution."),
        ("Corroborative hỏi: output này được hỗ trợ bởi evidence nào?", "Corroborative asks: what evidence supports this output?"),
        ("Game-theoretic hỏi: utility nên được chia credit ra sao?", "Game-theoretic asks: how should utility be credited?"),
        ("Predictive hỏi: nếu training data đổi, model behavior đổi thế nào?", "Predictive asks: if training data changes, how does behavior change?"),
        ("Part II bắt đầu từ chính câu hỏi thứ ba này.", "Part II starts from this third question."),
        ("Nếu không có theory, attribution score dễ chỉ là một con số nghe hợp lý.", "Without theory, an attribution score can sound plausible but be hard to check."),
        ("Ta có thể nói một data point quan trọng, nhưng quan trọng theo nghĩa nào?", "We may call a data point important, but important in what sense?"),
        ("Nó làm loss giảm, đổi nhãn test example, hay chỉ giúp một group nhỏ?", "Does it reduce loss, flip a test label, or help only a small group?"),
        ("Nếu thật sự bỏ nó khỏi training set, dự đoán đó có xảy ra không?", "If we actually remove it from training, does that prediction happen?"),
        ("Trong phần này, ta biến trực giác thành một bài toán rõ hơn.", "Here, we turn intuition into a clearer problem."),
        ("Training data đi vào learning algorithm như thế nào?", "How does training data enter the learning algorithm?"),
        ("Thay đổi data nghĩa là gì, và counterfactual behavior đổi ra sao?", "What does changing data mean, and how does behavior change?"),
        ("Mục tiêu là dự đoán behavior mà không train lại model quá nhiều lần.", "The goal is predicting behavior without retraining too many times."),
    ],
    [
        ("Điểm đáng chú ý là theory này không bắt đầu từ deep learning.", "The notable point is that this theory did not start with deep learning."),
        ("Nó có một statistical analog khá lâu đời.", "It has an older statistical analog."),
        ("Trong statistics, người ta hỏi: dataset đổi một chút thì estimator đổi thế nào?", "In statistics, people asked how estimators change when data changes slightly."),
        ("Nếu bỏ một observation khỏi regression, coefficient có đổi nhiều không?", "If one observation is removed from regression, do coefficients move much?"),
        ("Nếu tăng weight của một sample, estimate có dịch đáng kể không?", "If a sample is upweighted, does the estimate shift noticeably?"),
        ("Nếu một điểm là outlier, nó có kéo lệch kết luận thống kê không?", "If a point is an outlier, does it skew the statistical conclusion?"),
        ("Các câu hỏi đó dẫn tới leave-one-out diagnostics.", "These questions led to leave-one-out diagnostics."),
        ("Chúng cũng dẫn tới infinitesimal jackknife và influence functions.", "They also led to infinitesimal jackknife and influence functions."),
        ("Nhưng có một khác biệt quan trọng khi sang machine learning.", "But there is an important shift when moving to machine learning."),
        ("Trong statistical analog cổ điển, target thường là parameter prediction.", "In classical statistics, the target is often parameter prediction."),
        ("Tức là ta dự đoán parameter của estimator thay đổi ra sao.", "That means predicting how estimator parameters change."),
        ("Trong data attribution cho ML, target thường là behavior prediction.", "In ML data attribution, the target is often behavior prediction."),
        ("Behavior có thể là output, loss, accuracy, robustness, hoặc fairness.", "Behavior can mean output, loss, accuracy, robustness, or fairness."),
        ("Parameter vẫn quan trọng, nhưng nó chỉ là tầng trung gian.", "Parameters still matter, but they are only an intermediate layer."),
        ("Parameter đổi nhiều mà behavior không đổi, user có thể không quan tâm.", "If parameters move but behavior does not, users may not care."),
        ("Một đổi nhỏ trong parameter nhưng làm prediction đổi mạnh lại rất quan trọng.", "A small parameter shift can still be crucial if predictions change a lot."),
        ("Vì vậy công thức có thể bắt đầu trong parameter space.", "So the math may start in parameter space."),
        ("Nhưng mục tiêu cuối cùng của video này là model behavior.", "But the final target of this video is model behavior."),
    ],
    [
        ("Framework đầu tiên là M-estimation.", "The first framework is M-estimation."),
        ("Tên nghe khô, nhưng ý tưởng rất tự nhiên.", "The name sounds dry, but the idea is natural."),
        ("Ta xem model như nghiệm của một bài toán tối ưu.", "We view the model as the solution of an optimization problem."),
        ("Mỗi training sample tạo ra một loss riêng.", "Each training sample creates its own loss."),
        ("Nếu sample được dùng đầy đủ, weight của nó là một.", "If a sample is fully used, its weight is one."),
        ("Nếu sample bị bỏ ra, weight của nó là không.", "If it is removed, its weight is zero."),
        ("Nếu ta giảm ảnh hưởng của nó, weight nằm giữa không và một.", "If we reduce its effect, the weight lies between zero and one."),
        ("Nếu upweight một nhóm dữ liệu, weight có thể lớn hơn một.", "If a group is upweighted, its weight can be larger than one."),
        ("Thay vì training set cố định, ta gắn với nó một weight vector w.", "Instead of a fixed dataset, we attach a weight vector w."),
        ("Khi w đổi, bài toán tối ưu đổi.", "When w changes, the optimization problem changes."),
        ("Khi bài toán đổi, nghiệm theta star của w cũng đổi.", "When the problem changes, the solution theta star of w changes."),
        ("Đây là bước làm attribution trở nên rõ ràng hơn.", "This is where attribution becomes more precise."),
        ("Ta hỏi: nếu weight vector đổi, parameter và behavior đổi thế nào?", "We ask: if the weight vector changes, how do parameters and behavior change?"),
    ],
    [
        ("Trường hợp đơn giản nhất của weight vector là leave-one-out.", "The simplest case of a weight vector is leave-one-out."),
        ("Ta thường viết tắt là LOO.", "We often abbreviate it as LOO."),
        ("Ta train model trên toàn bộ dataset.", "We train the model on the full dataset."),
        ("Sau đó bỏ một data point, ví dụ z j, rồi train lại model.", "Then we remove one data point, say z j, and retrain."),
        ("Cuối cùng ta so sánh behavior trước và sau khi bỏ z j.", "Finally, we compare behavior before and after removing z j."),
        ("Nếu behavior đổi mạnh, z j có influence lớn với behavior đang xét.", "If behavior changes a lot, z j has large influence on that behavior."),
        ("Nếu model gần như không đổi, influence của z j là nhỏ.", "If the model barely changes, z j has small influence."),
        ("Điểm hay của LOO là nó rất rõ ràng.", "The nice thing about LOO is that it is very clear."),
        ("Nó hỏi một counterfactual cụ thể: nếu thiếu z j thì model ra sao?", "It asks a concrete counterfactual: what if z j were missing?"),
        ("Nhưng điểm dở cũng rõ: nó quá đắt.", "But the downside is also clear: it is too expensive."),
        ("Một triệu điểm nghĩa là gần một triệu lần retrain.", "A million points means almost a million retraining runs."),
        ("Với deep learning và foundation models, điều này gần như không thể.", "For deep learning and foundation models, this is nearly impossible."),
        ("Vì vậy LOO là mục tiêu vàng: đúng định nghĩa, nhưng quá tốn.", "So LOO is a gold target: clean by definition, but too costly."),
        ("Các phương pháp theory chủ yếu là cách xấp xỉ mục tiêu này.", "The theory methods are mainly ways to approximate this target."),
    ],
    [
        ("Để thấy theory có ích, ta bắt đầu với linear regression.", "To see why theory helps, we start with linear regression."),
        ("Ta có các điểm dữ liệu x và y.", "We have data points x and y."),
        ("Model là một đường thẳng, hoặc tổng quát hơn là linear predictor.", "The model is a line, or more generally a linear predictor."),
        ("Loss là squared error: dự đoán lệch y bao nhiêu thì bị phạt bình phương.", "The loss is squared error: prediction errors are squared."),
        ("Trong trường hợp này, nghiệm tối ưu có công thức đóng.", "In this case, the optimum has a closed form."),
        ("Ta không cần xem training như một hộp đen hoàn toàn.", "Training does not need to be a complete black box."),
        ("Theta star có thể viết trực tiếp bằng ma trận của dữ liệu.", "Theta star can be written directly using data matrices."),
        ("Khi bỏ một điểm, ta cũng không cần train lại từ đầu.", "When one point is removed, we still do not need full retraining."),
        ("Sherman-Morrison xem việc xóa điểm như một cập nhật hạng một.", "Sherman-Morrison treats removal as a rank-one update."),
        ("Đại số có thể nặng, nhưng trực giác rất đẹp.", "The algebra can be heavy, but the intuition is beautiful."),
        ("Nếu bài toán có cấu trúc, influence có thể tính từ nghiệm hiện tại.", "If the problem has structure, influence can be computed from the current solution."),
        ("Nó cũng phụ thuộc vào geometry của dữ liệu.", "It also depends on the geometry of the data."),
    ],
    [
        ("Trong linear regression, LOO cho hai mảnh trực giác quan trọng.", "In linear regression, LOO gives two key intuitions."),
        ("Mảnh thứ nhất là residual.", "The first piece is residual."),
        ("Residual là lỗi còn lại của data point đó.", "Residual is the remaining error of that data point."),
        ("Nếu model dự đoán rất sai ở z j, z j đang kéo đường fit về phía nó.", "If the model is very wrong on z j, z j pulls the fit toward itself."),
        ("Nhưng residual lớn thôi chưa đủ.", "But a large residual alone is not enough."),
        ("Ta còn cần leverage.", "We also need leverage."),
        ("Leverage nói điểm đó nằm ở vị trí hình học nhạy cảm đến đâu.", "Leverage measures how geometrically sensitive that point is."),
        ("Một điểm giữa đám đông có thể không làm đường fit đổi nhiều.", "A point inside a dense cluster may not move the fit much."),
        ("Một điểm ở rìa phân phối có thể kéo đường fit mạnh hơn.", "A point on the edge of the distribution can pull much harder."),
        ("Vì vậy influence không chỉ là loss cao.", "So influence is not just high loss."),
        ("Influence kết hợp lỗi cục bộ với hình học toàn cục.", "Influence combines local error with global geometry."),
        ("Gradient là hướng sample muốn kéo model.", "The gradient is the direction a sample pulls the model."),
        ("Hessian là độ cong, hay độ cứng, của loss landscape.", "The Hessian is the curvature, or stiffness, of the loss landscape."),
    ],
    [
        ("Linear regression quá đẹp vì có công thức đóng.", "Linear regression is unusually nice because it has a closed form."),
        ("Nhưng nhiều model khác, như logistic regression, không may như vậy.", "But many models, such as logistic regression, are not so lucky."),
        ("Model vẫn có thể tuyến tính theo feature.", "The model may still be linear in the features."),
        ("Nhưng loss không còn là một quadratic đơn giản.", "But the loss is no longer a simple quadratic."),
        ("Ta thường phải dùng optimization để tìm nghiệm.", "We usually need optimization to find the solution."),
        ("Ý tưởng tiếp theo là tạo một quadratic approximation.", "The next idea is to build a quadratic approximation."),
        ("Ta xấp xỉ loss quanh nghiệm hiện tại.", "We approximate the loss around the current solution."),
        ("Hãy tưởng tượng loss landscape như một bề mặt cong.", "Imagine the loss landscape as a curved surface."),
        ("Gần điểm tối ưu, ta phóng to bề mặt đó.", "Near the optimum, we zoom into that surface."),
        ("Trong một vùng nhỏ, nó giống một cái bát parabol.", "In a small region, it looks like a parabolic bowl."),
        ("Khi bỏ một sample, đáy thật của loss mới có thể dịch đi.", "When a sample is removed, the true bottom may shift."),
        ("Ta không tìm đáy mới bằng retraining.", "We do not find the new bottom by retraining."),
        ("Ta dùng local geometry để dự đoán đáy mới nằm ở đâu.", "We use local geometry to predict where the new bottom is."),
    ],
    [
        ("Bây giờ ta đi từ linear model sang M-estimation tổng quát hơn.", "Now we move from linear models to general M-estimation."),
        ("Ở nghiệm tối ưu, tổng gradient có trọng số bằng không.", "At the optimum, the weighted sum of gradients is zero."),
        ("Đó là optimality condition.", "That is the optimality condition."),
        ("Nếu model ở đáy loss, các lực kéo từ dữ liệu cân bằng nhau.", "At the bottom of the loss, pulls from data balance out."),
        ("Ta hỏi: nếu tăng nhẹ weight của sample j thì theta dịch hướng nào?", "We ask: if sample j is upweighted slightly, where does theta move?"),
        ("Để trả lời, ta đạo hàm optimality condition theo w j.", "To answer, we differentiate the optimality condition with respect to w j."),
        ("Kết quả là công thức influence function.", "The result is the influence function formula."),
        ("Lúc này, các giả định toán học bắt đầu quan trọng.", "At this point, mathematical assumptions start to matter."),
        ("Loss nên đủ trơn để gradient và Hessian có nghĩa.", "The loss should be smooth enough for gradients and Hessians."),
        ("Nghiệm tối ưu thường cần là duy nhất.", "The optimum often needs to be unique."),
        ("Quanh nghiệm đó, loss landscape cần có độ cong ổn định.", "Around that optimum, the loss landscape needs stable curvature."),
        ("Nói cách khác: strong convexity, unique minimizer, và Hessian khả nghịch.", "In other words: strong convexity, a unique minimizer, and invertible Hessian."),
        ("Các điều kiện này làm map từ data weights sang parameter ổn định.", "These conditions make the map from weights to parameters stable."),
        ("Công thức trực giác là: ảnh hưởng bằng âm inverse Hessian nhân gradient.", "Intuitively, influence is negative inverse Hessian times the gradient."),
        ("Gradient là hướng sample kéo model.", "The gradient is the direction the sample pulls the model."),
        ("Hessian cho biết loss chống lại hướng đó mạnh hay yếu.", "The Hessian says how strongly the loss resists that direction."),
        ("Đó là lý do influence function hấp dẫn.", "That is why influence functions are attractive."),
        ("Chỉ cần một model đã train, ta ước lượng influence của nhiều points.", "With one trained model, we can estimate influence for many points."),
        ("Nhưng đến đây ta mới dự đoán parameter change, chưa phải toàn bộ attribution.", "But so far we predict parameter change, not full attribution."),
    ],
    [
        ("Đây là chỗ cần phân biệt parameter prediction và behavior prediction.", "This is where we separate parameter prediction from behavior prediction."),
        ("Influence function cổ điển thường bắt đầu bằng parameter prediction.", "Classical influence functions usually start with parameter prediction."),
        ("Nếu weight của sample j đổi, theta sẽ dịch bao nhiêu?", "If sample j's weight changes, how much does theta move?"),
        ("Nhưng data attribution thường không chỉ quan tâm parameter.", "But data attribution usually cares about more than parameters."),
        ("Người dùng không nhìn trực tiếp vào hàng triệu parameter.", "Users do not directly inspect millions of parameters."),
        ("Họ quan tâm behavior: prediction, loss, accuracy, hoặc output probability.", "They care about behavior: prediction, loss, accuracy, or output probability."),
        ("Vì vậy ta cần thêm một bước chain rule.", "So we need one more chain-rule step."),
        ("Sample j kéo parameter theo một hướng.", "Sample j moves parameters in one direction."),
        ("Behavior nhạy với hướng parameter đó đến mức nào?", "How sensitive is the behavior to that parameter direction?"),
        ("Ghép hai phần lại, ta có influence lên behavior.", "Combine the two parts, and we get influence on behavior."),
        ("Koh và Liang dùng influence functions theo đúng tinh thần này.", "Koh and Liang used influence functions in this spirit."),
        ("Họ trace một prediction ngược qua learning algorithm.", "They traced a prediction backward through the learning algorithm."),
        ("Rồi tìm training examples có trách nhiệm lớn nhất.", "Then they found the most responsible training examples."),
        ("Vì vậy hãy luôn hỏi: method dự đoán parameter change hay behavior change?", "So always ask: does the method predict parameter change or behavior change?"),
        ("Nếu chỉ có parameter change, behavior ta quan tâm có đổi đúng không?", "If it only has parameter change, does the behavior really change as claimed?"),
    ],
    [
        ("Influence function rất đẹp, nhưng không phải cây đũa thần.", "Influence functions are elegant, but they are not magic."),
        ("Nó dựa trên một số giả định mạnh.", "They rely on several strong assumptions."),
        ("Thứ nhất, loss nên đủ trơn.", "First, the loss should be smooth."),
        ("Như vậy gradient và Hessian mới có ý nghĩa.", "Then gradients and Hessians are meaningful."),
        ("Thứ hai, phân tích thường nằm trong setting convex hoặc strongly convex.", "Second, the analysis often assumes convex or strongly convex settings."),
        ("Ở đó nghiệm tối ưu là duy nhất, tức có unique minimizer.", "There, the optimum is unique: a unique minimizer."),
        ("Hessian cũng cần khả nghịch hoặc đủ ổn định.", "The Hessian also needs to be invertible or stable enough."),
        ("Thứ ba, model được giả định đã train gần nghiệm tối ưu.", "Third, the model is assumed to be trained near an optimum."),
        ("Thứ tư, perturbation nên nhỏ.", "Fourth, the perturbation should be small."),
        ("Upweight nhẹ một điểm hợp với Taylor approximation hơn.", "A small upweighting fits Taylor approximation better."),
        ("Bỏ hẳn một điểm là thay đổi lớn hơn, nên xấp xỉ có thể sai.", "Removing a point entirely is larger, so the approximation may fail."),
        ("Modern deep learning phá nhiều giả định trong số đó.", "Modern deep learning breaks many of these assumptions."),
        ("Loss không convex, training có randomness, và nghiệm không duy nhất.", "The loss is nonconvex, training is random, and optima are not unique."),
        ("Hessian có thể suy biến hoặc cực kỳ khó xử lý.", "The Hessian can be degenerate or extremely hard to handle."),
        ("Vì vậy với DNN, không nên mặc định rằng IF reliable.", "So for DNNs, we should not assume IF is reliable by default."),
        ("Nếu thiếu convexity, convergence, hoặc Hessian ổn định, phải kiểm chứng.", "Without convexity, convergence, or stable Hessian, we must validate."),
        ("IF cho ta ngôn ngữ và baseline mạnh, không phải bằng chứng cuối cùng.", "IF gives a strong language and baseline, not final proof."),
        ("Đó là lý do Part III phải nói về scaling và evaluation.", "That is why Part III must discuss scaling and evaluation."),
    ],
    [
        ("Datamodels đi theo một hướng khác.", "Datamodels take a different route."),
        ("Thay vì local geometry của một model đã train, ta học cả learning process.", "Instead of local geometry, we learn the whole learning process."),
        ("Input là subset indicator.", "The input is a subset indicator."),
        ("Data point nào có mặt thì vị trí tương ứng là một.", "A present data point has a one in its position."),
        ("Data point nào bị loại thì vị trí đó là không.", "A removed data point has a zero."),
        ("Output là behavior đo được sau khi train model trên subset đó.", "The output is behavior measured after training on that subset."),
        ("Behavior có thể là loss, accuracy, class probability, hoặc một score cụ thể.", "Behavior can be loss, accuracy, class probability, or a specific score."),
        ("Để học datamodel, ta tạo nhiều training subsets.", "To learn a datamodel, we create many training subsets."),
        ("Với mỗi subset, ta chạy learning algorithm và đo behavior.", "For each subset, we run the learning algorithm and measure behavior."),
        ("Ta lưu lại một cặp: subset indicator và behavior.", "We store a pair: subset indicator and behavior."),
        ("Sau đó train một surrogate để dự đoán behavior từ indicator.", "Then we train a surrogate to predict behavior from the indicator."),
        ("Nếu surrogate học tốt, ta hỏi counterfactual nhanh hơn nhiều.", "If the surrogate learns well, counterfactual queries become much faster."),
        ("Datamodel không thay thế model chính.", "The datamodel does not replace the main model."),
        ("Nó mô hình hóa quan hệ giữa data và behavior của model chính.", "It models the relation between data and the main model's behavior."),
        ("Nói ngắn gọn, datamodeling biến attribution thành supervised learning.", "In short, datamodeling turns attribution into supervised learning."),
    ],
    [
        ("Phiên bản đơn giản và quan trọng nhất là linear datamodel.", "The simplest and most important version is the linear datamodel."),
        ("Prediction bằng bias term cộng tổng contribution của các data point.", "Prediction equals a bias term plus contributions from data points."),
        ("Nếu data point i có mặt, indicator m i bằng một.", "If data point i is present, indicator m i equals one."),
        ("Khi đó coefficient tau i được cộng vào prediction.", "Then coefficient tau i is added to the prediction."),
        ("Nếu data point vắng mặt, indicator bằng không.", "If the data point is absent, the indicator is zero."),
        ("Contribution đó biến mất.", "That contribution disappears."),
        ("Vì vậy tau i có thể đọc như attribution coefficient.", "So tau i can be read as an attribution coefficient."),
        ("Score này luôn gắn với behavior đang được đo.", "This score is always tied to the measured behavior."),
        ("Linear datamodel có họ hàng với influence functions.", "Linear datamodels are related to influence functions."),
        ("Mỗi data point có một effect tuyến tính, cố định.", "Each data point has a fixed linear effect."),
        ("Nó cũng gợi nhớ Shapley vì ta nhìn nhiều subsets.", "It also resembles Shapley because we inspect many subsets."),
        ("Nhưng mục tiêu chính ở đây là predict counterfactual behavior.", "But the main goal here is predicting counterfactual behavior."),
        ("Vì thế evaluation cực kỳ quan trọng.", "Therefore, evaluation is critical."),
        ("Ta giữ lại một số subsets chưa dùng để train datamodel.", "We hold out some subsets not used to train the datamodel."),
        ("Với các subsets đó, ta lấy behavior thật của model chính.", "For those subsets, we measure the true behavior of the main model."),
        ("Rồi so sánh với behavior datamodel dự đoán.", "Then we compare it with the datamodel prediction."),
        ("Nếu predicted-vs-actual khớp tốt, attribution đáng tin hơn.", "If predicted versus actual matches well, attribution is more trustworthy."),
        ("Nếu correlation thấp, score nhìn đẹp cũng chưa đủ.", "If correlation is low, a nice-looking score is still not enough."),
    ],
    [
        ("Ta có thể tóm tắt Part II bằng năm ý.", "We can summarize Part II in five points."),
        ("Một: predictive attribution có gốc gần với statistical analog lâu đời.", "One: predictive attribution has roots in an older statistical analog."),
        ("Nó hỏi estimator đổi thế nào khi data hoặc data weights đổi.", "It asks how estimators change when data or weights change."),
        ("Hai: M-estimation cho ta ngôn ngữ để nói về data.", "Two: M-estimation gives us a language for data."),
        ("Data đi vào learning algorithm qua weight vector.", "Data enters the learning algorithm through a weight vector."),
        ("Ba: leave-one-out là counterfactual cơ bản nhất.", "Three: leave-one-out is the basic counterfactual."),
        ("Nó rõ ràng, dễ hiểu, nhưng quá đắt ở scale lớn.", "It is clear and intuitive, but too costly at large scale."),
        ("Bốn: influence functions dùng gradient và Hessian để xấp xỉ ảnh hưởng.", "Four: influence functions use gradients and Hessians to approximate influence."),
        ("Nhưng chúng đi kèm giả định mạnh.", "But they come with strong assumptions."),
        ("Strong convexity, unique minimizer, convergence, và Hessian ổn định.", "Strong convexity, unique minimizer, convergence, and stable Hessian."),
        ("Năm: datamodels học trực tiếp map từ subset sang behavior.", "Five: datamodels directly learn the map from subsets to behavior."),
        ("Nếu học tốt, attribution trở thành một bài toán prediction có thể đánh giá.", "If learned well, attribution becomes an evaluable prediction problem."),
        ("Điểm chung là attribution không nên chỉ là một ranking đẹp.", "The common point is that attribution should not be just a nice ranking."),
        ("Nó phải trả lời: nếu data đổi, behavior có đổi như dự đoán không?", "It must answer: if data changes, does behavior change as predicted?"),
        ("Đó là nơi Part III bắt đầu.", "That is where Part III begins."),
        ("Modern ML không nhỏ, không convex, và không rẻ.", "Modern ML is not small, not convex, and not cheap."),
        ("Vậy làm sao scale các ý tưởng này lên deep networks và foundation models?", "So how do we scale these ideas to deep networks and foundation models?"),
        ("Phần tiếp theo nói về scaling và evaluation trong thế giới messy đó.", "The next part covers scaling and evaluation in that messy world."),
    ],
]


def fmt_time(seconds: float) -> str:
    ms_total = round(seconds * 1000)
    hours, rem = divmod(ms_total, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    sec, ms = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{sec:02d},{ms:03d}"


def split_long_text(text: str, limit: int = MAX_VI_CHARS) -> list[str]:
    text = " ".join(text.split())
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    current = ""
    phrase_parts = re.split(r"(?<=[,;:])\s+", text)
    if len(phrase_parts) == 1:
        phrase_parts = text.split(" ")

    for part in phrase_parts:
        candidate = f"{current} {part}".strip()
        if len(candidate) > limit and current:
            chunks.append(current)
            current = part
        else:
            current = candidate
    if current:
        chunks.append(current)

    result: list[str] = []
    for chunk in chunks:
        if len(chunk) > limit and " " in chunk:
            result.extend(split_long_text(chunk, limit))
        else:
            result.append(chunk)
    return result


def split_voice_text(text: str) -> list[str]:
    chunks: list[str] = []
    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n+", text) if paragraph.strip()]
    for paragraph in paragraphs:
        sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                chunks.extend(split_long_text(sentence))
    return chunks


def extract_voice_segments(path: Path) -> list[list[str]]:
    text = path.read_text(encoding="utf-8")
    sections: list[list[str]] = []
    matches = list(re.finditer(r"^## (p2_\d+)[^\n]*\n", text, re.MULTILINE))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        if "Voice:" not in block:
            continue
        voice = block.split("Voice:", 1)[1]
        voice = voice.split("\n## Research Notes", 1)[0]
        lines = []
        for raw_line in voice.splitlines():
            line = raw_line.strip()
            if line and not line.startswith("Visual:"):
                lines.append(line)
        sections.append(split_voice_text("\n".join(lines)))
    return sections


def pair_with_english_hints(segment_index: int, vietnamese_cues: list[str]) -> list[tuple[str, str]]:
    english_hints = [english for _, english in SEGMENTS[segment_index]]
    if not english_hints:
        return [(cue, "") for cue in vietnamese_cues]
    if len(vietnamese_cues) == 1:
        return [(vietnamese_cues[0], english_hints[0])]

    result = []
    last_hint = len(english_hints) - 1
    last_cue = len(vietnamese_cues) - 1
    for cue_index, cue in enumerate(vietnamese_cues):
        hint_index = round(cue_index * last_hint / last_cue)
        result.append((cue, english_hints[hint_index]))
    return result


def read_exact_english_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def allocate(start: float, duration: float, cues: list[tuple[str, str]]) -> list[tuple[float, float, str, str]]:
    weights = [max(len(vi) + 0.55 * len(en), 36) for vi, en in cues]
    total = sum(weights)
    raw = [duration * weight / total for weight in weights]
    min_duration = 1.8
    if sum(max(value, min_duration) for value in raw) <= duration:
        fixed = [max(value, min_duration) for value in raw]
        extra = sum(fixed) - duration
        flexible = [index for index, value in enumerate(fixed) if value > min_duration]
        flex_sum = sum(fixed[index] - min_duration for index in flexible)
        if extra > 0 and flex_sum > 0:
            for index in flexible:
                fixed[index] -= extra * (fixed[index] - min_duration) / flex_sum
    else:
        fixed = raw

    result = []
    cursor = start
    for index, (vi, en) in enumerate(cues):
        end = start + duration if index == len(cues) - 1 else cursor + fixed[index]
        result.append((cursor, end, vi, en))
        cursor = end
    return result


def main() -> int:
    exact_segments = extract_voice_segments(VOICE_SCRIPT)
    if len(exact_segments) != len(SEGMENT_DURATIONS):
        raise ValueError(
            f"Expected {len(SEGMENT_DURATIONS)} voice sections, found {len(exact_segments)} in {VOICE_SCRIPT}"
        )

    english_lines = read_exact_english_lines(ENGLISH_LINES)
    vietnamese_lines = [cue for segment in exact_segments for cue in segment]
    if len(english_lines) != len(vietnamese_lines):
        raise ValueError(
            f"Expected {len(vietnamese_lines)} English subtitle lines, found {len(english_lines)} in {ENGLISH_LINES}"
        )

    all_cues = []
    cursor = 0.0
    english_cursor = 0
    for segment_index, (duration, vietnamese_cues) in enumerate(zip(SEGMENT_DURATIONS, exact_segments, strict=True)):
        segment_english = english_lines[english_cursor : english_cursor + len(vietnamese_cues)]
        english_cursor += len(vietnamese_cues)
        cues = list(zip(vietnamese_cues, segment_english, strict=True))
        all_cues.extend(allocate(cursor, duration, cues))
        cursor += duration

    blocks = [
        f"{index}\n{fmt_time(start)} --> {fmt_time(end)}\n{vi}\n{en}"
        for index, (start, end, vi, en) in enumerate(all_cues, start=1)
    ]
    output = Path("subtitles/part2_core_theory_bilingual.srt")
    output.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    print(f"Wrote {output} ({len(all_cues)} cues, {cursor:.3f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
