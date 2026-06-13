# Part 5 - Epilogue Recap Voice Script

Mục tiêu đọc: khoảng 8-9 phút, tùy giọng đọc. Video không embed audio; tạo voice bằng ElevenLabs rồi ghép thủ công trong CapCut.

Giữ nguyên các thuật ngữ chính: `data attribution`, `model behavior`, `training data`, `evidence`, `credit`, `prediction`, `counterfactual`, `evaluation`, `governance`, `RAG`, `unlearning`.

Khuyến nghị tạo audio thành các file:

- `p5_00.mp3` - Mở epilogue: bản đồ cuối
- `p5_01.mp3` - Nhìn lại bốn phần
- `p5_02.mp3` - Ba lens cần nhớ
- `p5_03.mp3` - Hai bài học về scale
- `p5_04.mp3` - Một nguyên tắc dùng attribution có trách nhiệm
- `p5_05.mp3` - Closing và credit

## p5_00 - Mở epilogue: bản đồ cuối

Visual: Part IV thu nhỏ lại thành một bản đồ lớn. Ở giữa là `data attribution at scale`; xung quanh có ba vòng: `lens`, `scale`, `responsibility`.

Voice:

Đến đây, ta đã đi qua gần như toàn bộ bức tranh chính của data attribution at scale.

Epilogue này sẽ không thêm một method mới.

Nó chỉ làm một việc: gom lại mọi thứ thành một bản đồ đủ ngắn để bạn có thể mang theo sau khi video kết thúc.

Nếu phải nói bằng một câu, data attribution không phải là việc đi tìm một con số kỳ diệu cho mỗi training example.

Nó là cách đặt câu hỏi có kỷ luật về quan hệ giữa training data và model behavior.

Ta không hỏi chung chung: data nào quan trọng nhất?

Ta hỏi cụ thể hơn: quan trọng đối với behavior nào? Dưới intervention nào? Với data unit nào? Và score đó sẽ được kiểm tra bằng evaluation nào?

Khi hỏi như vậy, data attribution bớt giống một bảng xếp hạng bí ẩn, và giống hơn một dụng cụ để suy nghĩ rõ ràng.

Ở phần cuối này, hãy giữ lại ba thứ: ba lens, hai bài học về scale, và một nguyên tắc dùng attribution có trách nhiệm.

## p5_01 - Nhìn lại bốn phần

Visual: timeline bốn phần. Part I mở ra taxonomy; Part II mở ra công thức; Part III mở ra hệ thống scale; Part IV mở ra dashboard application.

Voice:

Ta bắt đầu ở Part I bằng taxonomy.

Corroborative attribution hỏi: output này được hỗ trợ bởi evidence nào?

Game-theoretic attribution hỏi: nếu nhiều data points cùng tạo ra một utility, credit nên chia thế nào?

Predictive attribution hỏi: nếu training data thay đổi, model behavior sẽ thay đổi ra sao?

Ba câu hỏi này nghe giống nhau nếu chỉ gọi chung là attribution, nhưng thật ra chúng khác nhau về bản chất.

Sang Part II, ta đi vào nền tảng lý thuyết.

Ta nhìn data weight như một núm xoay: tăng, giảm, hoặc remove một data point, rồi quan sát optimum và behavior thay đổi thế nào. Leave-one-out là counterfactual sạch nhưng đắt; influence function là xấp xỉ dựa trên gradient và Hessian; datamodels học một surrogate từ subset indicator sang behavior.

Sang Part III, ta đối mặt với scale.

Modern ML không chỉ có nhiều data hơn; nó còn có model lớn hơn, training noisy hơn, nhiều target behaviors hơn, và chi phí retrain cao hơn. Vì vậy mọi estimator ở scale lớn đều là tradeoff giữa cost, assumption, và accuracy.

Và sang Part IV, ta thấy attribution chỉ thật sự có nghĩa khi đi vào ứng dụng: debugging, dataset selection, data valuation, poisoning, unlearning, citation, RAG, và copyright-related analysis.

Bốn phần này nối với nhau bằng một ý tưởng duy nhất: ứng dụng quyết định câu hỏi attribution.

## p5_02 - Ba lens cần nhớ

Visual: ba lens lớn xoay quanh một output và một training set. Mỗi lens chiếu ra một loại câu hỏi khác nhau.

Voice:

Lens thứ nhất là evidence.

Đây là lens của corroborative attribution.

Khi ta hỏi một câu trả lời được hỗ trợ bởi source nào, một citation có đúng không, hoặc một output có quá giống một document trong corpus không, ta đang hỏi về evidence. Nhưng evidence không tự động là cause.

Lens thứ hai là credit.

Đây là lens của game-theoretic attribution.

Khi ta hỏi một contributor, một dataset, hoặc một data point nên nhận bao nhiêu credit cho một utility, ta cần định nghĩa utility trước. Credit không phải là giá trị tuyệt đối của data trong mọi hoàn cảnh; nó là contribution trong một context cụ thể.

Lens thứ ba là prediction.

Đây là lens của predictive attribution.

Khi ta hỏi nếu remove một subset, add một nhóm data, hoặc upweight một cluster thì behavior sẽ đổi thế nào, ta đang hỏi về counterfactual prediction. Ở đây, score chỉ đáng tin khi nó dự đoán đúng behavior ngoài dữ liệu dùng để fit estimator.

Nếu cần nhớ bằng ba dòng, hãy nhớ thế này.

Evidence trả lời: output được hỗ trợ bởi gì?

Credit trả lời: utility nên được chia thế nào?

Prediction trả lời: data intervention sẽ làm behavior đổi ra sao?

## p5_03 - Hai bài học về scale

Visual: hai cột lớn. Cột trái: `exact counterfactual is expensive`. Cột phải: `evaluation is part of the method`. Ở giữa có một model lớn và nhiều training runs.

Voice:

Bài học thứ nhất về scale là: counterfactual sạch thường rất đắt.

Leave-one-out nghe rất tự nhiên: bỏ một data point, retrain model, đo behavior. Nhưng nếu có hàng triệu data points, ta không thể retrain hàng triệu lần. Shapley value cũng đẹp, nhưng số coalition tăng theo cấp số mũ.

Vì vậy ở scale lớn, gần như mọi method đều là một dạng approximation.

Influence function tuyến tính hóa quanh optimum. TracIn nhìn vào training trajectory. TRAK dùng projection để scale behavior attribution. Datamodels trả upfront cost bằng nhiều training runs để dự đoán counterfactual nhanh hơn.

Không có method nào miễn phí.

Mỗi method mua tốc độ bằng một giả định, một proxy, hoặc một loại evaluation cần kiểm tra.

Bài học thứ hai là: evaluation không phải phần phụ lục.

Evaluation là một phần của định nghĩa method.

Nếu score dùng cho debugging, ta kiểm tra top-k examples có giúp chẩn đoán lỗi không. Nếu dùng cho data selection, ta kiểm tra model sau khi train với subset đã chọn. Nếu dùng cho unlearning, ta kiểm tra utility, forgetting, privacy. Nếu dùng cho citation, ta kiểm tra support và faithfulness.

Một attribution score nhìn hợp lý không đủ.

Ở scale lớn, câu hỏi không phải "score này có đẹp không?", mà là "score này có dự đoán hoặc hỗ trợ quyết định đúng trong setting ta quan tâm không?"

## p5_04 - Một nguyên tắc dùng attribution có trách nhiệm

Visual: checklist sáu bước xuất hiện từng dòng. Cuối cùng checklist đóng lại thành một la bàn `responsible attribution`.

Voice:

Nguyên tắc cuối cùng là: đừng bắt đầu từ method; hãy bắt đầu từ câu hỏi ứng dụng.

Trước khi chọn influence function, TRAK, datamodels, Shapley value, hay retrieval similarity, hãy viết câu hỏi thật rõ.

Một: behavior nào đang được giải thích hoặc dự đoán?

Hai: data unit là gì? Document, paragraph, image, user record, prompt-response pair, cluster, hay whole dataset?

Ba: intervention là gì? Remove, downweight, add, relabel, deduplicate, hay retrain không có forget set?

Bốn: notion of attribution là gì? Evidence, credit, hay prediction?

Năm: ai được quyền xem score, và score có thể bị dùng sai không?

Điểm này đặc biệt quan trọng trong security, privacy, copyright, và data governance.

Một score đủ mạnh để giúp defender tìm poisoning cũng có thể giúp attacker tối ưu attack. Một citation score có thể tạo cảm giác chắc chắn giả nếu không kiểm tra claim. Một unlearning score dùng để triage không nên bị trình bày như chứng nhận rằng model đã quên.

Sáu: evaluation nào sẽ quyết định rằng score này dùng được?

Nếu không trả lời được sáu câu hỏi đó, attribution rất dễ biến thành một con số có vẻ khoa học nhưng không dẫn đến quyết định đúng.

Responsible attribution không có nghĩa là không dùng score.

Nó có nghĩa là dùng score với đúng lens, đúng giới hạn, đúng người xem, và đúng evaluation.

## p5_05 - Closing và credit

Visual: màn hình tối dần. Ba câu cuối hiện ra như ba dòng lớn: `evidence is not cause`, `credit is utility-dependent`, `prediction must be evaluated`. Sau đó hiện credit ICML tutorial.

Voice:

Vậy nếu bạn chỉ giữ lại ba câu sau video này, hãy giữ lại ba câu này.

Evidence is not cause.

Credit is utility-dependent.

Prediction must be evaluated counterfactually.

Ba câu đó nghe đơn giản, nhưng chúng ngăn rất nhiều nhầm lẫn khi dùng data attribution trong thực tế.

Khi debug hallucination, hãy hỏi document đó là evidence, là cause, hay chỉ là một neighbor trong embedding space. Khi chia credit cho data contributors, hãy hỏi utility, context, và fairness criteria là gì. Khi remove, select, hoặc unlearn data, hãy hỏi counterfactual behavior có được dự đoán đúng không.

Đó là tinh thần của data attribution at scale.

Không phải một magic score, cũng không phải một bảng xếp hạng cuối cùng. Mà là một cách làm cho mối quan hệ giữa training data và model behavior rõ ràng hơn, kiểm chứng được hơn, và có trách nhiệm hơn.

Nội dung video này được xây dựng dựa trên ICML 2024 Tutorial: Data Attribution at Scale, cùng các ý tưởng lớn về influence functions, data valuation, datamodels, scalable attribution, counterfactual evaluation, và các ứng dụng trong modern ML.

Nếu Part I cho ta ngôn ngữ, Part II cho ta nền tảng, Part III cho ta bài toán scale, và Part IV cho ta ứng dụng, thì Part V chỉ để nhắc lại một điều:

Trước khi hỏi data nào quan trọng, hãy hỏi quan trọng theo nghĩa nào.

Và đó là nơi data attribution thật sự bắt đầu.
