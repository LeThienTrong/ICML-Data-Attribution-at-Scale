# Part 4 - Applications Voice Script

Mục tiêu đọc: khoảng 19-21 phút, tùy giọng đọc. Video không embed audio; tạo voice bằng ElevenLabs rồi ghép thủ công trong CapCut.

Giữ nguyên các thuật ngữ: `data attribution`, `model behavior`, `counterfactual`, `model debugging`, `dataset selection`, `data valuation`, `data poisoning`, `machine unlearning`, `RAG`, `citation`, `evidence`, `credit`, `predictive attribution`, `counterfactual evaluation`.

Khuyến nghị tạo audio thành các file:

- `p4_00.mp3` - Từ estimator sang quyết định ứng dụng
- `p4_01.mp3` - Recipe chung cho mọi ứng dụng
- `p4_02.mp3` - Model debugging
- `p4_03.mp3` - Dataset selection
- `p4_04.mp3` - Data valuation và fair credit
- `p4_05.mp3` - Data poisoning và security
- `p4_06.mp3` - Machine unlearning
- `p4_07.mp3` - Citation, RAG, copyright
- `p4_08.mp3` - Pitfalls: dùng sai lens
- `p4_09.mp3` - Recap và chuyển sang epilogue

## p4_00 - Từ estimator sang quyết định ứng dụng

Visual: Part III thu nhỏ thành ba khối `estimator`, `evaluation`, `budget`; sau đó mở ra dashboard ứng dụng với nhiều nút: debug, select, poison, unlearn, cite.

Voice:

Ở Part III, ta đã nhìn data attribution như một bài toán scaling và evaluation.

Ta hỏi: nếu không thể retrain model cho mọi counterfactual, ta có thể dùng estimator nào? Influence function? TracIn? TRAK? Datamodels? Hay một proxy rẻ hơn?

Nhưng khi bước sang ứng dụng, câu hỏi thay đổi một chút.

Người dùng cuối thường không hỏi: estimator này đẹp về mặt toán học không?

Họ hỏi: score này giúp tôi làm gì?

Nó có giúp debug một lỗi cụ thể không? Có giúp chọn data tốt hơn không? Có giúp phát hiện poisoning không? Có giúp unlearn một tập dữ liệu mà không phá model không? Có giúp trích dẫn nguồn cho một câu trả lời không?

Vì vậy Part IV là lớp quyết định nằm trên tất cả những gì ta đã xây.

Ta không còn nhìn attribution score như một con số đứng một mình. Ta nhìn nó như một tín hiệu để hành động.

Và khi đã nói đến hành động, câu hỏi quan trọng nhất là: hành động đó cần loại quan hệ nào giữa data và behavior?

Nếu cần evidence, ta dùng một lens. Nếu cần credit, ta dùng lens khác. Nếu cần dự đoán counterfactual behavior, ta lại cần một lens khác.

Đây là điểm giữ cho toàn bộ video không bị lẫn lộn: ứng dụng quyết định ý nghĩa của attribution.

## p4_01 - Recipe chung cho mọi ứng dụng

Visual: một pipeline 5 bước: `behavior` -> `data unit` -> `intervention` -> `attribution notion` -> `evaluation`. Mỗi bước sáng lên theo voice.

Voice:

Trước khi đi vào từng ứng dụng, hãy đặt một recipe chung.

Bước một: định nghĩa model behavior ta quan tâm.

Behavior có thể là một output sai, loss trên một subgroup, hallucination rate, win rate, toxicity, robustness, fairness, hoặc accuracy trên một benchmark cụ thể.

Nếu behavior không rõ, attribution score cũng sẽ mơ hồ.

Bước hai: định nghĩa data unit.

Một unit có thể là một document, một paragraph, một image, một user record, một prompt-response pair, một cluster dữ liệu, hoặc cả một dataset.

Việc chọn unit quyết định score có thể hành động được hay không. Nếu unit quá nhỏ, score nhiễu. Nếu unit quá lớn, ta không biết nên sửa phần nào.

Bước ba: định nghĩa intervention.

Ta sẽ remove data? Downweight data? Add data? Replace label? Deduplicate? Hay retrain không có một forget set?

Attribution dùng để giải thích một output không nhất thiết trả lời được câu hỏi remove data sẽ làm gì.

Bước bốn: chọn notion of attribution.

Corroborative attribution đo evidence. Game-theoretic attribution đo credit trong một utility. Predictive attribution đo khả năng dự đoán behavior khi data thay đổi.

Bước năm: kiểm tra bằng evaluation phù hợp.

Nếu score dùng để rank data cho debugging, ta kiểm tra precision của top examples. Nếu score dùng để chọn data, ta kiểm tra model sau khi thêm hoặc bỏ data. Nếu score dùng cho unlearning, ta kiểm tra behavior sau intervention.

Recipe này nghe có vẻ chậm, nhưng nó tiết kiệm rất nhiều sai lầm.

Vì nếu không định nghĩa behavior, unit, intervention, và evaluation, một score rất đẹp vẫn có thể không trả lời đúng câu hỏi của ứng dụng.

## p4_02 - Model debugging

Visual: một output lỗi màu đỏ; mũi tên ngược về training examples; các cụm lỗi: mislabeled, duplicated, spurious, distribution shift.

Voice:

Ứng dụng đầu tiên là model debugging.

Ta bắt đầu từ một behavior xấu đã quan sát được: model phân loại sai một image, trả lời sai một factual question, hallucinate một claim, hoặc fail trên một nhóm người dùng cụ thể.

Một phản ứng tự nhiên là hỏi: trong training data, có những examples nào liên quan đến lỗi này?

Ở đây, attribution không nhất thiết phải chứng minh nhân quả hoàn toàn. Nhiều khi ta chỉ cần một shortlist tốt để con người kiểm tra.

Ví dụ, nếu model trả lời sai vì học nhầm một pattern, attribution có thể kéo ra các training examples có label sai, annotation mơ hồ, hoặc data bị duplicated quá nhiều.

Nếu model fail trên một subgroup, attribution có thể chỉ ra rằng training set có rất ít examples giống subgroup đó, hoặc có nhiều examples gần giống nhưng label không nhất quán.

Các nghiên cứu về datamodels còn cho ta một kiểu audit rộng hơn: tìm brittle predictions, tức những prediction đổi mạnh khi training subset thay đổi; và tìm train-test leakage, khi một test example có dấu vết phụ thuộc bất thường vào một phần training data rất gần với nó.

Trong debugging, top-k examples thường quan trọng hơn một score tuyệt đối hoàn hảo.

Người engineer muốn biết: tôi nên nhìn vào 20 examples nào trước?

Vì vậy evaluation cho debugging có thể rất thực dụng: trong top-k examples, bao nhiêu cái thật sự giúp chẩn đoán lỗi? Nếu remove hoặc sửa chúng, lỗi có giảm không? Nếu thêm data tương tự, behavior có cải thiện không?

Nhưng có một bẫy nhỏ.

Data liên quan về mặt semantic chưa chắc là data gây lỗi.

Một example nhìn rất giống test case có thể chỉ là evidence, không phải nguyên nhân. Ngược lại, một cluster dữ liệu tưởng như xa hơn có thể đã làm model học một shortcut sai.

Vì vậy debugging thường cần kết hợp hai thứ: similarity để tìm evidence gần, và predictive hoặc counterfactual attribution để kiểm tra tác động khi data thay đổi.

## p4_03 - Dataset selection

Visual: một pool dữ liệu lớn; model behavior meter; các điểm dữ liệu sáng lên theo expected gain; cuối cùng chọn subset nhỏ hơn.

Voice:

Ứng dụng thứ hai là dataset selection.

Nếu debugging bắt đầu từ câu hỏi "lỗi này đến từ đâu?", dataset selection hỏi: "ta nên huấn luyện thêm, giữ lại, hoặc ưu tiên dữ liệu nào?"

Đây là một câu hỏi rất thực tế.

Trong nhiều pipeline, dữ liệu không còn là thứ ta chỉ gom càng nhiều càng tốt.

Data có chi phí: chi phí lưu trữ, chi phí annotation, chi phí training, chi phí kiểm duyệt, và đôi khi cả chi phí pháp lý.

Nếu ta có một ngân sách hữu hạn, attribution có thể giúp chọn data dự kiến cải thiện behavior quan trọng nhất.

Ví dụ, ta muốn cải thiện accuracy trên rare classes. Ta có thể tìm những examples mà estimator dự đoán sẽ làm behavior trên rare classes tốt hơn.

Hoặc ta muốn giảm hallucination cho một loại câu hỏi. Ta có thể ưu tiên data có tác động dự đoán tốt lên metric đó, thay vì chỉ thêm data giống query về mặt embedding.

Ở đây, predictive attribution rất tự nhiên.

Ta không chỉ hỏi data nào giống target. Ta hỏi nếu thêm hoặc tăng trọng số data này, behavior mục tiêu có cải thiện không?

Literature về data valuation, như Data Shapley, cũng cho một góc nhìn liên quan. Data có value cao có thể gợi ý ta nên acquire thêm dữ liệu cùng kiểu. Data có value thấp bất thường có thể là outlier, corrupted example, hoặc label cần kiểm tra lại.

Tuy nhiên dataset selection cũng là nơi dễ bị overfit vào metric.

Nếu ta chọn data chỉ để cải thiện một benchmark, model có thể tốt lên trên benchmark đó nhưng tệ hơn ở nơi khác.

Vì vậy một workflow tốt thường có ba lớp: chọn data theo attribution, train hoặc fine-tune model, rồi kiểm tra trên held-out behaviors không dùng để chọn data.

Nói cách khác, data selection không nên chỉ là "sort theo score rồi lấy top".

Nó nên là một vòng lặp: score, chọn subset, train, evaluate, rồi cập nhật lại mục tiêu.

## p4_04 - Data valuation và fair credit

Visual: nhiều contributors đưa data vào một utility chung; utility bar tăng; Shapley/marginal contribution xuất hiện; duplicate data làm credit chia nhỏ.

Voice:

Ứng dụng thứ ba là data valuation.

Ở đây câu hỏi không phải "data nào giúp debug lỗi?", cũng không hẳn là "data nào nên thêm vào model?".

Câu hỏi là: nếu nhiều bên đóng góp dữ liệu, giá trị hoặc credit nên được phân bổ như thế nào?

Đây là nơi game-theoretic attribution trở lại.

Nếu ta có một utility function, ví dụ accuracy, revenue, win rate, hoặc một metric chất lượng, ta có thể hỏi mỗi contributor đóng góp bao nhiêu vào utility đó.

Shapley value là một lý tưởng đẹp vì nó trung bình marginal contribution qua nhiều context khác nhau.

Trong Data Shapley, trực giác này được đưa vào machine learning: giá trị của một datum được đo qua đóng góp của nó vào performance của predictor, đồng thời cố gắng giữ các nguyên tắc valuation tự nhiên như dữ liệu giống nhau nên nhận credit giống nhau, và dữ liệu không làm đổi utility thì không nên nhận credit lớn.

Nhưng trong thực tế, data valuation cực kỳ nhạy với định nghĩa utility.

Một dataset có thể rất có giá trị cho task y tế, nhưng gần như vô dụng cho task dịch máy.

Một contributor có thể đóng góp rất nhiều examples, nhưng nếu hầu hết là duplicates của data đã có, marginal contribution thật sự có thể thấp.

Ngược lại, một contributor nhỏ có thể cung cấp một nhóm dữ liệu hiếm, làm model cải thiện mạnh trên một subgroup quan trọng.

Vì vậy data valuation không nên được hiểu là "dữ liệu này có giá trị tuyệt đối bao nhiêu?".

Nó nên được hiểu là: đối với utility này, trong bối cảnh dữ liệu hiện tại, contribution của data này là gì?

Điểm này cũng giúp tránh một hiểu lầm phổ biến.

Fair credit và predictive usefulness không phải lúc nào cũng giống nhau.

Một attribution method có thể dự đoán rất tốt behavior khi remove data, nhưng chưa chắc thỏa mãn các axioms công bằng mà ta muốn cho payment.

Ngược lại, một credit allocation rất đẹp về mặt fairness có thể quá đắt hoặc quá noisy để dùng trong pipeline selection hằng ngày.

Ứng dụng quyết định tradeoff.

## p4_05 - Data poisoning và security

Visual: training set có một vài điểm đỏ; model bị kéo lệch; attribution heatmap highlight outliers; warning icon `dual-use`.

Voice:

Ứng dụng thứ tư là data poisoning và security.

Trong data poisoning, attacker chèn vào training data những examples được thiết kế để làm model sai, mở backdoor, hoặc thiên lệch theo một hướng có lợi cho attacker.

Một số attack hiện đại còn nguy hiểm hơn vì chúng có thể clean-label: nhìn bằng mắt thì label vẫn hợp lý, nhưng example được chỉnh rất tinh vi để gradient kéo model về một target sai trong quá trình training.

Attribution có thể giúp defense theo hai cách.

Cách thứ nhất là truy vết từ behavior xấu về những training examples có ảnh hưởng bất thường.

Nếu một nhóm nhỏ data có score rất cao đối với một failure mode cụ thể, đó có thể là tín hiệu cần audit.

Cách thứ hai là phát hiện outliers trong ảnh hưởng.

Một data point bình thường có thể hơi giúp hoặc hơi hại. Nhưng một data point có tác động quá lớn, nhất là lên một target behavior nhạy cảm, đáng được kiểm tra kỹ.

Tuy nhiên đây là phần cần nói cẩn thận.

Attribution trong security là dual-use.

Nó có thể giúp defender tìm data độc hại, nhưng cũng có thể giúp attacker hiểu điểm nào có ảnh hưởng lớn và tối ưu attack tốt hơn.

Vì vậy trong ứng dụng security, ta không chỉ hỏi estimator có chính xác không.

Ta còn hỏi: ai được quyền xem score? Score được aggregate ở mức nào? Có cần privacy protection không? Có thể bị dùng để reverse engineer training data hay không?

Nói cách khác, security không chỉ là một use case kỹ thuật.

Nó là nơi data attribution phải đi kèm governance.

## p4_06 - Machine unlearning

Visual: dataset S; forget set F bị khoanh; câu hỏi `train on S \ F?`; predictive surrogate ước lượng behavior; validation panel.

Voice:

Ứng dụng thứ năm là machine unlearning.

Giả sử có một forget set F: một người dùng yêu cầu xóa dữ liệu, một license thay đổi, hoặc một phần data được phát hiện là không nên dùng.

Câu hỏi lý tưởng là: nếu ta train model từ đầu trên S trừ F, model behavior sẽ như thế nào?

Đó là một câu hỏi counterfactual rất tự nhiên.

Nhưng với model lớn, retrain từ đầu mỗi khi có yêu cầu unlearning có thể quá đắt.

Một hướng như SISA training cố giảm chi phí này bằng cách chia training thành shard và slice, để khi cần quên một data point, ta chỉ phải cập nhật một phần nhỏ hơn của hệ thống thay vì toàn bộ model.

Data attribution không tự động giải quyết machine unlearning, nhưng nó giúp ta ước lượng và kiểm tra tác động của việc quên.

Predictive attribution có thể dự đoán remove F sẽ làm behavior nào thay đổi nhiều.

Influence-style methods có thể cho một approximation nhanh khi giả định đủ ổn.

Datamodels có thể học map từ subset hoặc group removal sang behavior, nếu ta có đủ training runs để học surrogate.

Nhưng trong unlearning, tiêu chuẩn đánh giá phải rất rõ.

Ta không chỉ cần model "trông giống đã quên" trên một vài examples.

Ta cần kiểm tra utility còn giữ được không, privacy hoặc compliance có đạt không, và model có còn nhớ thông tin của forget set theo các attack probes hay không.

Vì vậy attribution ở đây là một phần của pipeline, không phải giấy chứng nhận cuối cùng.

Nó giúp ta ưu tiên, dự đoán, và audit. Nhưng quyết định unlearning vẫn cần evaluation độc lập.

## p4_07 - Citation, RAG, và copyright

Visual: user query -> generated answer; retrieved documents; evidence arrows; citation candidates; copyright similarity warning.

Voice:

Ứng dụng tiếp theo là citation, RAG, và copyright-related analysis.

Đây là nơi corroborative attribution rất tự nhiên.

Khi một language model tạo ra một câu trả lời, người dùng thường hỏi: câu trả lời này được hỗ trợ bởi nguồn nào?

Trong RAG, model đã có một retrieval step. Nhưng retrieval không tự động có nghĩa là citation đúng.

Một document có thể được retrieve nhưng không thực sự hỗ trợ claim cuối cùng.

Ngược lại, một claim trong output có thể cần nhiều sources kết hợp mới đủ evidence.

Và ngay cả khi citation đúng về mặt nội dung, vẫn còn một câu hỏi khó hơn: citation đó có faithful không? Nghĩa là model thật sự dựa vào source đó khi tạo claim, hay source chỉ được gắn vào sau như một lời giải thích hợp lý?

Corroborative attribution cố gắng nối từng output, claim, hoặc span với những evidence candidates trong corpus.

Ứng dụng này khác với predictive attribution.

Ta không hỏi nếu remove document này khỏi training data thì model behavior thay đổi ra sao.

Ta hỏi document này có hỗ trợ, phản bác, hay liên quan đến output hiện tại không.

Với copyright detection cũng vậy, câu hỏi thường không phải utility hay counterfactual behavior.

Câu hỏi là output có quá gần một source trong corpus không? Có dấu hiệu reproduction không? Đoạn nào là evidence cho nghi ngờ đó?

Vì vậy citation và copyright là ví dụ rất tốt cho việc chọn đúng lens.

Nếu dùng game-theoretic credit để giải thích citation, ta có thể nói sai.

Nếu dùng retrieval similarity để kết luận causal influence, ta cũng có thể nói sai.

Một hệ thống tốt cần tách rõ: evidence cho output, credit cho utility, và prediction cho intervention.

## p4_08 - Pitfalls: dùng sai lens

Visual: ba lens như ba màu; các đường nối sai bị gạch đỏ: `evidence != cause`, `credit != nearest neighbor`, `prediction != fairness`.

Voice:

Đến đây, ta có thể tóm lại các pitfalls quan trọng.

Pitfall thứ nhất: nhầm evidence với cause.

Một source hỗ trợ một claim không nhất thiết là nguyên nhân khiến model tạo ra claim đó.

Nó có thể chỉ là một tài liệu cùng nói về sự thật đó, hoặc một passage được retrieve sau khi model đã có xu hướng trả lời như vậy.

Với RAG, đây là khác biệt giữa citation correctness và citation faithfulness: source có thể support câu trả lời, nhưng chưa chắc là source mà model thật sự relied on.

Pitfall thứ hai: nhầm similarity với value.

Data gần target về mặt embedding có thể hữu ích cho retrieval, nhưng chưa chắc có marginal contribution cao cho training.

Pitfall thứ ba: nhầm fair credit với predictive effect.

Một score dùng để chia payment cần tiêu chí công bằng. Một score dùng để chọn data cần dự đoán improvement. Hai mục tiêu này có thể dẫn đến hai method khác nhau.

Pitfall thứ tư: quên rằng unit of attribution thay đổi kết luận.

Một document có thể có score thấp, nhưng một paragraph trong document đó lại cực kỳ quan trọng.

Một data point có thể score thấp, nhưng cả cluster của nó lại có tác động lớn.

Pitfall thứ năm: bỏ qua evaluation sau khi hành động.

Nếu ta remove data theo attribution score, cần đo lại model. Nếu ta cite source theo corroborative score, cần kiểm tra claim có thật sự được support. Nếu ta unlearn, cần kiểm tra cả utility và forgetting.

Vì vậy thông điệp thực dụng nhất của Part IV là: attribution score không phải đích đến. Nó là một proposal để hành động, và hành động đó phải được kiểm tra.

## p4_09 - Recap và chuyển sang epilogue

Visual: bảng tổng hợp: `debugging -> evidence + predictive`, `selection -> predictive`, `valuation -> game-theoretic`, `poisoning -> predictive/security`, `unlearning -> counterfactual`, `RAG/citation -> corroborative`. Cuối cùng thu về ba lens.

Voice:

Hãy gom lại Part IV.

Model debugging dùng attribution để rút ngắn đường từ một lỗi cụ thể về những data cần kiểm tra.

Nó cũng giúp audit brittle predictions và train-test leakage, miễn là ta không nhầm semantic similarity với nguyên nhân thật.

Dataset selection dùng attribution để ưu tiên data có khả năng cải thiện behavior mục tiêu, hoặc phát hiện data nên acquire, clean, hay loại khỏi pipeline.

Data valuation dùng attribution để phân bổ credit cho contributors hoặc datasets, nhưng luôn phụ thuộc utility, context, và các tiêu chí fairness ta chọn.

Data poisoning dùng attribution để audit những data có ảnh hưởng xấu bất thường, đồng thời nhắc ta về tính dual-use của score: score tốt cho defender cũng có thể giúp attacker.

Machine unlearning dùng attribution để dự đoán và kiểm tra tác động của việc quên một forget set, nhưng attribution không tự nó là chứng nhận unlearning.

Citation, RAG, và copyright dùng corroborative attribution để nối output với evidence candidates trong corpus, đồng thời phải phân biệt support với faithful reliance.

Những ứng dụng này rất khác nhau, nhưng chúng cùng tuân theo một nguyên tắc.

Đừng bắt đầu từ method. Hãy bắt đầu từ câu hỏi ứng dụng.

Bạn cần evidence? Bạn cần credit? Hay bạn cần dự đoán behavior sau một intervention?

Khi trả lời được câu đó, ta mới biết nên dùng lens nào, estimator nào, và evaluation nào.

Đó cũng là thông điệp cuối của toàn bộ tutorial: data attribution at scale không phải là một score duy nhất.

Nó là một cách đặt câu hỏi có kỷ luật về quan hệ giữa data và model behavior.

Ở epilogue, ta sẽ gom lại bức tranh này thành một bản đồ ngắn: ba lens, hai bài học về scale, và một nguyên tắc để dùng attribution một cách có trách nhiệm.
