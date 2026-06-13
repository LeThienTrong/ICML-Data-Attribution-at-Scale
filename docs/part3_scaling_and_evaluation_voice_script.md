# Part 3 - Scaling and Evaluation Voice Script

Mục tiêu: bản chi tiết khoảng 26-30 phút ở tốc độ đọc tự nhiên. CapCut voice speed giữ ở `1.00`.

Giữ nguyên các thuật ngữ: `data attribution`, `scaling`, `estimator`, `counterfactual`, `leave-one-out`, `influence function`, `Hessian-vector product`, `gradient similarity`, `TracIn`, `TRAK`, `random projection`, `surrogate`, `datamodel`, `LDS`, `calibration`, `ranking`, `counterfactual evaluation`, `ablation`, `future work`.

Gợi ý tạo audio theo đoạn:

- `p3_00.mp3` - Từ theory sạch sang modern ML messy
- `p3_01.mp3` - Ba trục scale: data, parameter, target behavior
- `p3_02.mp3` - Ground truth counterfactual không còn đơn giản
- `p3_03.mp3` - Influence functions ở scale lớn
- `p3_04.mp3` - Training dynamics và TracIn
- `p3_05.mp3` - TRAK: behavior attribution ở scale lớn
- `p3_06.mp3` - Datamodels khi scale: chính xác hơn nhưng đắt
- `p3_07.mp3` - Method landscape: accuracy/cost trade-off
- `p3_08.mp3` - Evaluation: predicted vs actual counterfactual
- `p3_09.mp3` - Failure modes và hygiene khi đánh giá
- `p3_10.mp3` - Future work: attribution vẫn là bài toán mở
- `p3_11.mp3` - Practical takeaway và chuyển sang applications

## p3_00 - Từ theory sạch sang modern ML messy

Visual: Part II thu lại thành bốn khối `weights -> LOO -> IF -> datamodels`, rồi phóng to sang một mô hình lớn với data stream rất dài.

Voice:

Ở cuối Part II, ta đã có một bộ ngôn ngữ khá sạch.

Data đi vào learning algorithm qua weight vector. Leave-one-out cho ta một counterfactual rõ ràng. Influence function dùng gradient và Hessian để xấp xỉ ảnh hưởng của một sample. Datamodels học trực tiếp map từ subset data sang model behavior.

Nếu chỉ dừng ở đây, câu chuyện nghe có vẻ đã gần xong.

Nhưng Part III mới là nơi chữ "at scale" bắt đầu cắn thật mạnh.

Trong toy problem, ta có thể tưởng tượng bỏ một điểm dữ liệu, train lại model, đo behavior, rồi so sánh. Ta cũng có thể tưởng tượng lưu Hessian, đảo Hessian, hoặc train nhiều model trên nhiều subset.

Nhưng modern machine learning không vận hành trong kích thước đó.

Dataset có thể có hàng triệu, hàng trăm triệu, hoặc hàng tỷ examples. Model có thể có hàng triệu đến hàng tỷ parameters. Behavior ta quan tâm không chỉ là một scalar duy nhất, mà có thể là loss trên hàng nghìn prompts, accuracy trên nhiều groups, hoặc probability của một output cụ thể.

Vậy câu hỏi của Part III là:

Làm sao giữ lại tinh thần counterfactual của Part II, nhưng sống được với compute, memory, randomness, và non-convexity của modern ML?

Điều quan trọng là: scaling không chỉ có nghĩa là "làm code chạy nhanh hơn".

Scaling buộc ta phải chọn approximation. Ta phải quyết định bỏ qua phần nào của bài toán, giữ lại phần nào, và kiểm tra approximation đó bằng dữ liệu thực nghiệm.

Nói cách khác, Part III không chỉ hỏi: method nào nhanh?

Nó hỏi: method nào còn dự đoán đúng behavior khi mọi thứ trở nên lớn, noisy, và messy?

## p3_01 - Ba trục scale: data, parameter, target behavior

Visual: ba trục tọa độ `n = number of training points`, `p = number of parameters`, `m = number of target behaviors`; các công thức cost mọc lên trên từng trục.

Voice:

Để thấy vấn đề rõ hơn, hãy tách scaling thành ba trục.

Trục thứ nhất là số lượng training points, gọi là n.

Nếu ta muốn exact leave-one-out cho từng data point, chi phí tối thiểu đã là n lần retraining. Với một triệu điểm, đó là gần một triệu lần train lại. Nếu ta muốn xét mọi subset, số khả năng không còn là n nữa, mà là hai mũ n. Đây không phải một con số lớn; nó là một con số biến bài toán thành bất khả thi.

Trục thứ hai là số parameters, gọi là p.

Influence function nhìn gọn trên công thức:

delta f j xấp xỉ bằng âm gradient của behavior, nhân inverse Hessian, nhân gradient của training sample j.

Nhưng Hessian là một object kích thước p nhân p. Với model nhỏ, ta còn có thể tưởng tượng nó. Với neural network lớn, lưu Hessian đầy đủ đã không thực tế, chứ chưa nói đến việc đảo ma trận.

Vì vậy các method thực tế thường không bao giờ dùng Hessian đầy đủ. Chúng dùng Hessian-vector products, conjugate gradient, LiSSA, diagonal approximation, K-FAC style approximation, hoặc một dạng sketching nào đó.

Trục thứ ba là số target behaviors, gọi là m.

Một attribution score thường không tồn tại một mình. Ta muốn biết data point z ảnh hưởng đến target nào. Một test image? Một prompt? Một class? Một subgroup? Một metric như robustness hoặc fairness?

Nếu có n training points và m targets, chỉ riêng bảng attribution đã có thể có n nhân m entries. Với n và m đều lớn, ngay cả việc lưu score cũng trở thành vấn đề.

Vì vậy ở scale lớn, câu hỏi không còn là "tính attribution cho mọi thứ".

Câu hỏi thực tế hơn là:

Ta cần attribution cho behavior nào, ở độ phân giải nào, và với ngân sách compute bao nhiêu?

Nếu không trả lời câu này trước, ta rất dễ chọn một method nhìn sang trên paper nhưng không dùng được trong pipeline thật.

## p3_02 - Ground truth counterfactual không còn đơn giản

Visual: hai nhánh retraining từ cùng dataset: `same data, different seed`, `same data, different checkpoint`; output behavior dao động quanh một vùng thay vì một điểm.

Voice:

Trước khi nói về estimator, ta cần cẩn thận với chữ ground truth.

Trong Part II, ta nói exact leave-one-out như thể nó là một con số rõ ràng:

Train trên S, train trên S bỏ z j, rồi lấy hiệu behavior.

Nhưng với deep learning, ngay cả "train lại model" cũng không hoàn toàn là một phép toán deterministic.

Cùng một dataset, nhưng seed khác, data order khác, augmentation khác, checkpoint khác, hoặc learning rate schedule khác, model có thể đi đến behavior hơi khác. Với model lớn, những khác biệt nhỏ này đôi khi đủ để làm attribution nhìn khác đi.

Vì vậy khi đánh giá attribution ở scale lớn, ta phải định nghĩa counterfactual protocol.

Ví dụ: khi bỏ một subset A, ta retrain từ scratch hay fine-tune từ checkpoint? Dùng cùng seed hay nhiều seeds? Đo behavior ở final checkpoint hay trung bình qua checkpoints? Nếu target là language model output, ta đo log probability, exact match, win rate, hay một judge score?

Những chi tiết này nghe có vẻ kỹ thuật, nhưng chúng quyết định attribution có nghĩa gì.

Một estimator không thể đúng nếu target counterfactual chưa được định nghĩa.

Điểm này đặc biệt quan trọng khi so sánh methods. Nếu một method dự đoán effect của việc upweight nhẹ một sample, còn benchmark lại đo effect của việc bỏ hẳn một subset rồi retrain với seed khác, thì hai thứ đó không hoàn toàn cùng một câu hỏi.

Vì vậy Part III có một nguyên tắc nền:

Trước khi hỏi estimator nào tốt, hãy hỏi: estimator đang cố dự đoán counterfactual nào?

Sau đó, evaluation phải dùng đúng loại counterfactual đó.

## p3_03 - Influence functions ở scale lớn

Visual: công thức IF từ Part II xuất hiện, sau đó phần `H^{-1}` biến thành một khối lớn bị nén qua `HVP`, `CG`, `sketch`, `low-rank`.

Voice:

Nhóm method đầu tiên cố giữ lại tinh thần của influence functions.

Ở mức công thức, influence function rất hấp dẫn vì ta chỉ train một model, rồi dùng local geometry quanh model đó để ước lượng effect của từng training point.

Công thức behavior influence có dạng:

delta f j xấp xỉ bằng âm gradient của behavior theo theta, nhân inverse Hessian, nhân gradient loss của sample j.

Vấn đề nằm ở inverse Hessian.

Với model lớn, ta không thể xây H rồi đảo H. Thay vào đó, ta cố tính một thứ yếu hơn: inverse-Hessian-vector product. Nghĩa là thay vì hỏi toàn bộ ma trận H inverse là gì, ta hỏi H inverse nhân với một vector cụ thể thì ra vector nào.

Các kỹ thuật như conjugate gradient hoặc LiSSA cố giải bài toán này mà không lưu Hessian đầy đủ. Auto-differentiation cho phép tính Hessian-vector product tương đối hiệu quả hơn so với việc materialize toàn bộ Hessian.

Nhưng ngay cả vậy, cost vẫn không hề nhỏ.

Ta phải tính gradient cho nhiều training points, gradient cho target behavior, rồi chạy iterative solver. Nếu target nhiều, cost nhân lên. Nếu model lớn, memory và batching trở thành vấn đề. Nếu Hessian noisy hoặc không positive definite, kết quả có thể kém ổn định.

Một hướng đơn giản hơn là dùng approximation thô: diagonal Hessian, block diagonal, low-rank, K-FAC style, hoặc thậm chí bỏ Hessian đi và dùng gradient similarity.

Gradient similarity hỏi: training point và target có gradient cùng hướng không?

Nếu gradient của z và gradient của target cùng hướng, thì z có thể đang hỗ trợ behavior đó. Nếu ngược hướng, z có thể đang chống lại. Cách này rẻ hơn, dễ scale hơn, nhưng mất phần curvature mà influence function ban đầu cố giữ.

Vì vậy tradeoff rất rõ:

Càng giữ nhiều geometry, method càng gần theory hơn nhưng đắt hơn.

Càng bỏ nhiều geometry, method càng scale tốt hơn nhưng cần evaluation nghiêm túc hơn.

## p3_04 - Training dynamics và TracIn

Visual: training trajectory đi qua nhiều checkpoints; mỗi checkpoint tạo một dot product giữa gradient của training sample và gradient của target.

Voice:

Một hướng khác là nhìn vào training dynamics.

Thay vì chỉ nhìn model cuối cùng và cố xấp xỉ Hessian quanh nghiệm cuối, ta hỏi:

Trong suốt quá trình training, sample z đã ảnh hưởng đến target behavior như thế nào?

Một method tiêu biểu cho lens này là TracIn.

Trực giác của TracIn khá dễ hình dung. Khi model đang training, nếu một training example z được dùng ở một bước nào đó, gradient update từ z có thể làm loss của target x tăng hoặc giảm. Nếu update từ z làm target tốt hơn nhiều lần qua các checkpoints, z được xem là helpful. Nếu nó làm target tệ hơn, z có thể harmful.

Công thức thường được viết như một tổng qua các checkpoints:

score của z lên target x xấp xỉ tổng theo t của learning rate eta t, nhân dot product giữa gradient loss của target x tại theta t và gradient loss của training point z tại theta t.

Điểm hay của cách này là nó không cần inverse Hessian.

Nó dùng những thứ thực tế hơn: gradients, loss functions, và saved checkpoints. Nếu training pipeline đã lưu checkpoint, ta có thể tận dụng chúng.

Nhưng TracIn cũng có giới hạn.

Nó phụ thuộc vào checkpoints được chọn. Nếu checkpoint quá thưa, ta bỏ lỡ dynamics quan trọng. Nếu quá dày, compute và storage tăng. Dot product gradient cũng có thể bị dominated bởi layer lớn, scale của loss, hoặc representation chưa được normalize tốt.

Ngoài ra, TracIn đo một dạng influence dọc theo training trajectory, không nhất thiết bằng exact leave-one-out sau retraining. Đây không phải lỗi; đây là một counterfactual khác.

Vì vậy khi dùng training dynamics methods, câu hỏi evaluation vẫn quay lại:

Score này có dự đoán đúng behavior thay đổi khi ta thật sự sửa data không?

Nếu có, nó là estimator hữu ích. Nếu không, dù trực giác training nghe rất hay, ta vẫn phải thận trọng.

## p3_05 - TRAK: behavior attribution ở scale lớn

Visual: một model lớn được linearize thành `after-kernel`; gradient features đi qua random projection, rồi tạo score cho nhiều training examples và targets.

Voice:

Một method hiện đại quan trọng trong câu chuyện "at scale" là TRAK.

TRAK viết tắt của Tracing with the Randomly-projected After Kernel.

Tên có vẻ dài, nhưng có thể hiểu theo ba ý.

Thứ nhất, TRAK nhắm trực tiếp vào model behavior. Nó không chỉ hỏi parameter đổi thế nào; nó muốn attribute một prediction hoặc một behavior cụ thể về training data.

Thứ hai, TRAK dùng ý tưởng linearization hoặc kernel approximation quanh các trained models. Thay vì retrain hàng nghìn model để biết data point nào ảnh hưởng, nó dùng gradient features của model đã train để xây một estimator rẻ hơn.

Thứ ba, TRAK dùng random projection để giảm kích thước. Gradient của neural network rất lớn, nên nếu giữ nguyên toàn bộ gradient vector cho mọi training point thì storage và compute sẽ nổ. Random projection nén gradient features xuống kích thước nhỏ hơn, với hy vọng vẫn giữ đủ thông tin để ranking attribution hữu ích.

Một điểm đáng chú ý là TRAK thường dùng nhiều models hoặc nhiều checkpoints, nhưng không cần con số cực lớn như datamodels đầy đủ. Nó cố đứng giữa hai cực:

Rẻ hơn retraining hàng nghìn lần, nhưng giàu thông tin hơn một gradient similarity baseline quá đơn giản.

TRAK cũng cho thấy một pattern rất quan trọng trong modern data attribution:

Ở scale lớn, ta thường không cố lấy exact value hoàn hảo. Ta cố lấy ranking đủ tốt, hoặc score đủ predictive cho task downstream.

Nếu mục tiêu là tìm top training examples hỗ trợ một prediction, ranking có thể quan trọng hơn calibration tuyệt đối.

Nhưng điều này cũng tạo ra một câu hỏi evaluation mới:

Nếu score của TRAK nói z1 quan trọng hơn z2, thứ tự đó có được xác nhận bởi counterfactual experiment không? Nếu ta remove hoặc downweight top positive examples, behavior có giảm như dự đoán không? Nếu ta remove harmful examples, behavior có cải thiện không?

TRAK mạnh vì nó được thiết kế cho large-scale differentiable models, nhưng nó vẫn là estimator.

Nó không miễn nhiễm với lỗi target definition, dữ liệu trùng lặp, distribution shift, hoặc evaluation không đúng counterfactual.

## p3_06 - Datamodels khi scale: chính xác hơn nhưng đắt

Visual: nhiều subset indicators đi vào nhiều training runs; sau đó một surrogate học map `subset -> behavior`; thanh cost upfront lớn nhưng query sau rẻ.

Voice:

Datamodels đi theo hướng gần brute force hơn.

Thay vì xấp xỉ local geometry của một model, datamodeling tạo nhiều training subsets, train hoặc fine-tune model trên các subsets đó, đo behavior, rồi học một surrogate.

Input của surrogate là subset indicator. Output là behavior sau khi training trên subset đó.

Nếu surrogate là linear datamodel, ta có:

f hat của m bằng beta zero cộng tổng theo i của m i nhân tau i.

Tau i lúc này được đọc như attribution coefficient của data point i đối với behavior đang xét.

Điểm mạnh của datamodels là chúng trực tiếp học relation giữa data và behavior. Chúng không cần giả định loss convex, không cần Hessian khả nghịch, và không cần model đã hội tụ đến một unique minimizer theo nghĩa cổ điển.

Nhưng đổi lại, datamodels trả một chi phí upfront rất lớn.

Ta phải train nhiều models hoặc nhiều fine-tuned variants. Ta phải thiết kế cách sample subsets. Ta phải quyết định subset size, sampling distribution, target behaviors, và số lượng runs đủ để surrogate học được signal.

Nếu data có một triệu points, không thể xem mọi subset. Ta phải dùng random subsets, group-level attribution, data shards, hoặc active design để chọn experiments thông minh hơn.

Vì vậy datamodels thường hợp khi ta có thể amortize cost.

Nghĩa là ta chịu tốn ban đầu để tạo một dataset of training runs, rồi dùng surrogate để trả lời nhiều counterfactual queries sau đó.

Một cách nhìn thực tế là:

Influence-style methods thường rẻ hơn nhưng phụ thuộc nhiều vào approximation quanh model hiện tại.

Datamodel-style methods thường đắt hơn nhưng đo trực tiếp hơn relation giữa subsets và behavior.

Không có bên nào thắng tuyệt đối. Lựa chọn phụ thuộc vào model size, data size, number of target behaviors, và việc ta có chấp nhận trả upfront cost hay không.

## p3_07 - Method landscape: accuracy/cost trade-off

Visual: một mặt phẳng hai trục `cost` và `counterfactual accuracy`; các method đi từ trái dưới sang phải trên: `representation similarity`, `gradient similarity`, `IF`, `TracIn`, `TRAK`, `empirical influence`, `Shapley`, `datamodels`.

Voice:

Đến đây, sẽ rất tự nhiên nếu ta hỏi: vậy nên dùng method nào?

Câu trả lời thực tế là: không có một method thống trị mọi trường hợp. Nên nhìn chúng như một landscape giữa hai trục.

Trục ngang là cost: phải train lại bao nhiêu lần, lưu bao nhiêu gradient, giải bao nhiêu linear systems, hoặc chạy bao nhiêu forward-backward passes.

Trục dọc là counterfactual accuracy: score có dự đoán đúng behavior khi ta thật sự thay đổi data hay không.

Ở vùng rất rẻ, ta có representation similarity hoặc nearest neighbors trong embedding space. Những method này dễ chạy, dễ giải thích trực giác, và có thể hữu ích cho retrieval hoặc kiểm tra duplicate. Nhưng chúng thường chỉ trả lời câu hỏi "data nào giống target?", chứ chưa chắc trả lời câu hỏi "data nào làm model behavior đổi?"

Tiếp theo là gradient similarity và TracIn. Chúng dùng gradient để đo training sample và target có kéo model theo hướng giống nhau hay không. Cost cao hơn similarity thường, nhưng vẫn dễ scale hơn exact retraining. Điểm mạnh là chúng bám vào learning dynamics hơn. Điểm yếu là score phụ thuộc checkpoint, loss, optimizer path, và cách ta định nghĩa target.

Influence functions nằm gần nhóm này, nhưng có thêm cấu trúc second-order qua Hessian. Khi giả định tốt, IF cho một xấp xỉ rất đẹp. Nhưng ở DNN lớn, non-convex, không hội tụ sạch, hoặc Hessian khó xử lý, IF dễ trở thành một baseline hơn là bằng chứng cuối cùng.

TRAK cố chiếm một vùng giữa khá hấp dẫn: không đắt như datamodels full, nhưng vẫn nhắm trực tiếp vào behavior attribution trong non-convex differentiable models. Nó dùng random projection và surrogate dạng after-kernel để giữ cost vừa phải.

Ở vùng đắt hơn là empirical influence, Shapley estimators, và datamodels. Chúng gần counterfactual hơn vì dựa trên nhiều training runs hoặc nhiều subsets. Nhưng cái giá là compute rất lớn. Với model lớn, đây thường là lựa chọn chỉ khả thi khi ta có thể amortize cost, làm trên subset nhỏ, hoặc làm ở group level.

Vì vậy, khi chọn estimator, đừng chỉ hỏi method nào "đúng nhất" trên giấy.

Hãy hỏi năm câu:

Ta cần point-level hay group-level attribution? Ta cần ranking hay magnitude? Ta có thể trả bao nhiêu compute? Target behavior có bao nhiêu? Và ta có ground-truth counterfactual nào để kiểm tra không?

Nếu không trả lời các câu hỏi này, method landscape chỉ là một bảng tên. Nếu trả lời rõ, nó trở thành bản đồ để chọn công cụ.

## p3_08 - Evaluation: predicted vs actual counterfactual

Visual: scatter plot `predicted delta` vs `actual delta`; đường chéo là perfect prediction; thêm một panel `LDS` với nhiều subset masks đi vào `sum attribution scores`, rồi so với actual behavior.

Voice:

Phần quan trọng nhất của Part III là evaluation.

Với predictive attribution, một score chỉ đáng tin khi nó giúp dự đoán counterfactual behavior.

Cấu trúc evaluation cơ bản là:

Một: chọn một intervention trên data. Ví dụ remove một point, remove một subset, upweight một group, hoặc add một data shard.

Hai: dùng estimator để dự đoán behavior sẽ đổi bao nhiêu.

Ba: thực hiện counterfactual thật, hoặc một approximation đủ đáng tin của nó, rồi đo actual behavior.

Bốn: so sánh predicted với actual.

Nếu predicted delta và actual delta khớp tốt, estimator có giá trị predictive. Nếu không, score có thể vẫn đẹp, nhưng chưa chắc dùng được cho decision.

Có nhiều cách đo.

Nếu ta quan tâm absolute effect, ta cần calibration: score dự đoán magnitude đúng đến đâu? Mean absolute error, R squared, hoặc predicted-vs-actual scatter plot có ích.

Nếu ta chỉ cần ranking, ta có thể dùng Spearman correlation, Kendall tau, hoặc top-k overlap. Ví dụ estimator có tìm đúng top harmful examples không?

Nếu ta quan tâm direction, ta đo sign accuracy: estimator có dự đoán đúng là remove subset này làm behavior tăng hay giảm không?

Nếu ứng dụng là debugging, top-k precision có thể quan trọng hơn calibration. Nếu ứng dụng là unlearning hoặc dataset selection, magnitude và sign có thể quan trọng hơn.

Một metric rất đáng nhắc ở đây là LDS, thường hiểu là Linear Datamodeling Score.

Trực giác của LDS rất đơn giản.

Ta lấy nhiều held-out subsets của training data. Với mỗi subset, ta thật sự train hoặc evaluate một model tương ứng để có actual behavior. Sau đó, ta dùng attribution scores để dự đoán behavior của subset đó bằng một mô hình tuyến tính:

y hat của subset bằng bias cộng tổng score của những data points có mặt trong subset.

Nếu predicted behavior này tương quan cao với actual behavior trên các held-out subsets, attribution scores đang nắm được một phần cấu trúc counterfactual thật. Nếu tương quan thấp, score có thể vẫn nhìn hợp lý trên từng point, nhưng chưa đủ để dự đoán behavior của dataset intervention.

Nói ngắn gọn, LDS không hỏi "điểm nào nhìn giống target nhất?"

Nó hỏi: nếu tôi cộng các attribution scores theo một subset, tôi có dự đoán được model behavior sau khi train trên subset đó không?

Đây là lý do LDS, hoặc các metric tương tự dựa trên held-out counterfactuals, rất hợp với Part III. Nó ép estimator phải chứng minh khả năng dự đoán, chứ không chỉ tạo ra một ranking đẹp.

Tất nhiên LDS cũng có giới hạn. Nó thiên về một surrogate tuyến tính. Nếu effect giữa data points có interaction mạnh, một tổng tuyến tính có thể bỏ sót. Nhưng chính giới hạn này lại hữu ích: nó cho ta một baseline rõ ràng để hỏi liệu linear attribution đã đủ chưa, hay phải dùng surrogate phi tuyến hơn.

Điểm cần nhớ là: metric evaluation phải khớp với use case.

Một method có ranking tốt chưa chắc có calibration tốt. Một method dự đoán tốt trên single-point removal chưa chắc dự đoán tốt trên large subset removal. Một method hoạt động trên image classification chưa chắc giữ nguyên behavior trên language model prompts.

Vì vậy câu hỏi không phải "method này có tốt không" theo nghĩa chung chung.

Câu hỏi đúng hơn là: method này có dự đoán đúng loại counterfactual mà ứng dụng của ta cần không?

## p3_09 - Failure modes và hygiene khi đánh giá

Visual: checklist cảnh báo: `duplicates`, `correlated data`, `target mismatch`, `seed noise`, `OOD intervention`, `metric mismatch`.

Voice:

Ở scale lớn, attribution rất dễ nhìn thuyết phục nhưng sai vì evaluation không sạch.

Failure mode đầu tiên là duplicate hoặc near-duplicate data.

Nếu nhiều training examples gần giống nhau, remove một điểm riêng lẻ có thể không làm behavior đổi nhiều, vì các bản sao còn lại vẫn giữ signal. Một method có thể xếp điểm đó thấp, không phải vì nó vô dụng, mà vì nó redundant. Ngược lại, group removal có thể cho thấy cả cụm đó rất quan trọng.

Failure mode thứ hai là correlated data.

Data point hiếm khi độc lập hoàn toàn. Một sample có thể đại diện cho một subpopulation, một style, một label convention, hoặc một artifact. Attribution point-level có thể bỏ lỡ cấu trúc group-level.

Failure mode thứ ba là target mismatch.

Nếu ta tính attribution cho training loss nhưng ứng dụng lại quan tâm fairness trên một subgroup, score có thể không giúp ích. Behavior phải được định nghĩa đúng ngay từ đầu.

Failure mode thứ tư là seed noise.

Nếu retraining stochastic, actual counterfactual có variance. Khi effect nhỏ hơn noise của training, rất khó nói estimator sai hay experiment quá noisy. Lúc này cần repeated seeds hoặc confidence intervals.

Failure mode thứ năm là intervention quá xa distribution.

Upweight nhẹ một sample, remove một sample, remove một shard lớn, và thay toàn bộ data distribution là bốn loại counterfactual khác nhau. Một local approximation có thể hợp lý cho perturbation nhỏ nhưng hỏng khi intervention lớn.

Vì vậy evaluation hygiene nên có vài nguyên tắc.

Luôn ghi rõ target behavior. Luôn ghi rõ intervention. Tách validation counterfactuals khỏi những runs dùng để fit estimator. Kiểm tra both ranking và sign nếu ứng dụng cần decision. Và khi có thể, test trên nhiều scales của intervention: point, small subset, và group.

Một attribution method tốt không chỉ tạo ra heatmap đẹp.

Nó phải đứng vững khi ta hỏi: nếu tôi hành động theo score này, model behavior có đổi theo hướng tôi kỳ vọng không?

## p3_10 - Future work: attribution vẫn là bài toán mở

Visual: năm cánh cửa nghiên cứu mở ra: `beyond linear`, `multi-stage pipelines`, `better surrogate`, `single-model counterfactual`, `efficient proxies`; phía sau là một pipeline dữ liệu lớn.

Voice:

Trước khi chuyển sang applications, cần nói rõ một điều:

Data attribution at scale chưa phải một bài toán đã đóng.

Part II cho ta ngôn ngữ. Part III cho ta các estimator và cách evaluate. Nhưng vẫn còn nhiều hướng nghiên cứu rất sống.

Hướng thứ nhất là beyond linear.

Rất nhiều attribution methods, kể cả khi dùng ngôn ngữ khác nhau, cuối cùng vẫn cố gán một score riêng cho từng data point rồi cộng các score đó lại. Cách này dễ hiểu, dễ visualize, và dễ dùng cho ranking. Nhưng data không luôn cộng tuyến tính.

Hai examples có thể chỉ hữu ích khi đi cùng nhau. Một nhóm data có thể redundant: remove một điểm không sao, remove cả cụm thì model sụp. Một point có thể harmful trong context này nhưng helpful trong context khác. Đây là interaction, và linear attribution không luôn bắt được.

Vì vậy future work tự nhiên là học surrogate phi tuyến hơn, hoặc attribution ở mức group, cluster, concept, hay data slice thay vì chỉ point-level.

Hướng thứ hai là multiple stages.

Trong hệ thống thật, model không chỉ được train một lần từ raw data. Có pretraining, filtering, deduplication, supervised fine-tuning, preference tuning, alignment, retrieval augmentation, và evaluation loop. Một data point có thể ảnh hưởng không trực tiếp qua final training step, mà qua việc nó thay đổi filter, thay đổi selected data, hoặc thay đổi intermediate checkpoint.

Attribution cho một pipeline nhiều stage khó hơn attribution cho một training run đơn. Nhưng nếu muốn hiểu modern AI systems, đây là hướng rất quan trọng.

Hướng thứ ba là better surrogate.

TRAK dùng một surrogate có cấu trúc kernel sau khi linearize model. Datamodels học surrogate từ subset indicators sang behavior. Các hướng tương lai có thể hỏi: surrogate nào đủ expressive để bắt interaction, nhưng vẫn đủ rẻ để scale? Khi nào ta nên dùng linear model, kernel, low-rank model, set function, hoặc neural surrogate?

Hướng thứ tư là single-model counterfactual.

Counterfactual chuẩn thường cần retraining, nhưng retraining quá đắt. Một câu hỏi lớn là: từ một hoặc vài trained models, ta có thể dự đoán đủ tốt effect của data removal, data addition, hay data reweighting không? Đây là lý do các method kiểu influence, TRAK, và approximation quanh model hiện tại vẫn rất hấp dẫn.

Hướng thứ năm là efficient proxies.

Đôi khi ta không cần counterfactual hoàn hảo. Ta cần một proxy đủ tốt để lọc candidate, phát hiện nhóm đáng ngờ, hoặc chọn subset cần kiểm tra kỹ hơn. Một proxy rẻ nhưng được evaluate đúng có thể hữu dụng hơn một estimator đẹp nhưng không chạy nổi ở scale thật.

Tóm lại, future work không chỉ là làm metric cao hơn.

Nó là tìm đúng mức approximation cho đúng use case: đủ chính xác để ra quyết định, đủ rẻ để chạy, và đủ minh bạch để biết khi nào không nên tin.

## p3_11 - Practical takeaway và chuyển sang applications

Visual: decision tree: `Need evidence? -> corroborative`; `Need fair credit? -> game-theoretic`; `Need behavior prediction? -> predictive + evaluation`; sau đó mũi tên sang Part IV.

Voice:

Ta có thể tóm tắt Part III bằng bốn takeaway.

Một: scale làm thay đổi bản chất bài toán. Với modern ML, exact retraining cho mọi data point thường không khả thi. Hessian đầy đủ cũng không khả thi. Và attribution cho mọi target behavior có thể quá lớn để lưu.

Hai: mọi scalable method đều là estimator. Influence approximations, gradient similarity, TracIn, TRAK, và datamodels đều bỏ qua một phần nào đó của bài toán để đổi lấy compute.

Ba: không có estimator nào tự động đúng vì công thức nhìn đẹp. Với predictive attribution, bằng chứng mạnh nhất là counterfactual evaluation: predicted behavior phải gần actual behavior trong những interventions ta quan tâm.

Bốn: method tốt phụ thuộc vào use case. Nếu ta cần debug một prediction cụ thể, top-k ranking có thể đủ. Nếu ta cần chọn data để cải thiện subgroup robustness, sign và group-level effect quan trọng hơn. Nếu ta cần unlearning, ta phải dự đoán behavior sau khi remove một forget set, không chỉ một point riêng lẻ.

Nói ngắn gọn:

Part II cho ta theory. Part III nhắc rằng ở scale lớn, theory phải đi cùng approximation và evaluation.

Một score đẹp chưa đủ. Một ranking hợp lý chưa đủ. Câu hỏi cuối cùng luôn là:

Nếu ta thay đổi data theo score đó, model behavior có đổi như estimator dự đoán không?

Và khi đã có câu trả lời thực nghiệm cho câu hỏi này, ta mới có thể dùng data attribution như một công cụ trong pipeline thật.

Đó là cầu nối sang Part IV.

Phần tiếp theo sẽ không chỉ hỏi attribution được tính như thế nào, mà hỏi: attribution giúp ta làm gì?

Debug model. Chọn data. Phát hiện poisoning. Hỗ trợ unlearning. Và trong hệ thống RAG hoặc citation, giúp người dùng hiểu output được chống lưng bởi nguồn nào.

## Research Notes

Các ý chính trong script này dựa trên mạch Part II-III của tutorial và các paper nền:

- `DataTutorialICML2024.pdf`, phần scaling/evaluation nếu có trong workspace hoặc tài liệu gốc của tutorial.
- Koh & Liang, 2017: influence functions trace prediction qua learning algorithm về training data.
- Pruthi et al., 2020: TracIn dùng gradients, checkpoints, và loss functions để trace influence theo training dynamics.
- Ilyas et al., 2022: datamodels học map từ training subsets sang predictions/behavior.
- Park et al., 2023: TRAK dùng random projection và after-kernel approximation cho model behavior attribution at scale.
