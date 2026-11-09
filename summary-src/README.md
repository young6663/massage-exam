# summary.html 產生方式

- out/NN.json：每題病因病理、人事時地、症狀、解剖、目的注意事項、補充（重點整理版為主、規範確認、講義最後）
- out3/NN.json：每題體位、墊枕、運動法、測試
- steps.json／meta.json：由 extract.py 從 index.html 抽出的步驟與穴數
- 重建：`python build.py v44 2026-11-09 ../summary.html`
- 驗證口訣與原文一致：先 `python extract.py ../index.html` 產生 src/，再 `python verify.py`
