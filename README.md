# Data Attribution at Scale - ICML 2024 Tutorial Report

Video học thuật khoảng 2 tiếng về tutorial **Data Attribution at Scale: Connecting ML behavior to (training) data** tại ICML 2024.

## Thông tin cần điền khi nộp YouTube

- Danh sách thành viên + MSSV:
  - Họ tên 1 - MSSV
  - Họ tên 2 - MSSV
- Môn học: [Tên môn học]
- Khóa/lớp: [Khóa/lớp]
- GVLT: [Tên GVLT]
- TG/GVTH: [Tên TG/GVTH]
- Tutorial được chọn: Data Attribution at Scale
- Hội nghị và năm: ICML 2024
- Link tutorial: https://ml-data-tutorial.org
- Link GitHub source Manim: [Dán link repo GitHub]
- Link video YouTube public: [Dán link video]

## Cấu trúc thư mục

```text
data-attribution-icml2024-manim/
├── README.md
├── requirements.txt
├── .gitignore
├── scenes/                 # Mã nguồn ManimCE theo từng gói/chương
├── notebooks/              # Notebook demo / live-code PyTorch, attribution
├── scripts/                # Script render, ghép audio, tạo subtitle
├── assets/                 # Tài nguyên đầu vào
│   ├── audio/              # AI voice theo từng scene
│   ├── subtitles/          # Phụ đề .srt/.vtt Anh/Việt
│   ├── images/             # Hình minh họa được phép dùng
│   ├── fonts/              # KHÔNG commit font có bản quyền nếu không được phép
│   └── reference/          # Slide/tutorial gốc để tham khảo nội bộ
├── outputs/                # Sản phẩm render tạm, không commit file lớn
│   ├── videos/
│   └── frames/
└── docs/                   # Kịch bản, checklist nộp bài, mô tả YouTube
```

## Cách cài đặt

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Cách render Manim

Render thử nhanh:

```bash
manim -pqh scenes/part1_g1_intro_taxonomy.py IntroTaxonomy
```

Render 1080p:

```bash
manim -p -r 1920,1080 scenes/part1_g1_intro_taxonomy.py IntroTaxonomy
```

## Quy ước đặt tên scene

```text
part1_g1_intro_taxonomy.py
part1_g2_corroborative.py
part1_g3_game_theoretic.py
part1_g4_predictive.py
part2_g1_problem_setup.py
...
```

## Checklist điểm cộng

- [ ] Video public trên YouTube.
- [ ] Mô tả YouTube có đầy đủ thành viên, MSSV, môn học, GV, tutorial, hội nghị/năm.
- [ ] Có link GitHub chứa source Manim sạch.
- [ ] Có phụ đề tiếng Việt.
- [ ] Có phụ đề tiếng Anh.
- [ ] Không vượt quá thời lượng tutorial gốc đáng kể.
- [ ] Nội dung phủ đủ các phần trong slide gốc.
```
