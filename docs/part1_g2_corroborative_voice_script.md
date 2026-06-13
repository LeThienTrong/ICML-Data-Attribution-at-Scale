# Part 1 G2 - Corroborative Attribution Voice Script

Video đã được sync với 3 file voice trong `assets/audio`:

- `g2_.00_intro.mp3`: 00:00.00-00:14.34
- `g2_01_continue.mp3`: 00:14.34-00:37.75
- `g2_02_rest.mp3`: 00:37.75-02:30.31

Các mốc dưới đây là timeline video sau khi đã chỉnh theo voice thật.

## 00:00.00-00:14.34

Trong phần này, ta đi vào `Corroborative Attribution`.

Ở đây, câu hỏi không phải là: data nào đã gây ra output.

Câu hỏi trước tiên là: có bằng chứng nào trong dữ liệu làm output này đáng tin hơn không?

## 00:14.34-00:37.75

Hãy tưởng tượng model vừa sinh ra một claim, hoặc một đoạn generation.

Ta quét qua một `corpus` cho trước: doc A, doc B, doc C, và nhiều đoạn khác.

Một vài đoạn chỉ là nhiễu. Nhưng một vài đoạn lại có nội dung rất gần với output.

Những đoạn đó được kéo ra như các `evidence candidates`: ứng viên bằng chứng cho output hiện tại.

## 00:37.75-00:59.92

Góc nhìn này xuất hiện trong nhiều use case thực tế.

Với citation, ta muốn biết câu trả lời của LLM được hỗ trợ bởi nguồn nào.

Với copyright detection, ta muốn biết output có quá giống một đoạn trong dữ liệu gốc hay không.

Dù mục tiêu khác nhau, cấu trúc chung vẫn là: từ output, tìm dữ liệu liên quan nhất.

## 00:59.92-01:23.80

Ta có thể viết ý tưởng đó bằng một score.

Với một input x, model sinh ra output y. Với một item z trong corpus, ta tính một `similarity score`.

Nếu score cao, z corroborate tốt cho output. Nói cách khác, z là bằng chứng mạnh hơn.

Điểm quan trọng là: relation ở đây là sự tương đồng hoặc hỗ trợ, không phải quan hệ nhân quả.

## 01:23.80-01:54.49

Pipeline đầy đủ có ba bước.

Đầu tiên, train set S tạo ra model. Sau đó, model sinh ra output y ở test time.

Cuối cùng, output y được so sánh với từng item trong search set.

Mỗi item nhận một score. Ta sắp xếp các item theo score đó, và lấy những item đứng đầu làm evidence.

Trong ví dụ này, z2 là bằng chứng mạnh nhất, z4 đứng tiếp theo.

## 01:54.49-02:16.67

Một cách triển khai quen thuộc là `Information Retrieval`.

Ta đưa output và các chunk trong corpus vào cùng một embedding space.

Những chunk nằm gần output nhất sẽ được xem là top evidence.

Đây là lý do retrieval-based attribution rất hữu ích khi corpus lớn và cần tìm nhanh.

## 02:16.67-02:30.31

Nhưng cần nhớ giới hạn.

Evidence hỗ trợ output không đồng nghĩa với causal claim, và cũng không tự động cho ta fair credit.

Muốn phân bổ credit một cách nguyên tắc, ta sẽ chuyển sang `Game-theoretic Attribution`.
