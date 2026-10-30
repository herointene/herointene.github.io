# 艇仔粥 TingZaiZuk

[造訪網站](https://blog.wulited.com/) · [關於本站](https://blog.wulited.com/about/)

> 滾燙熱湯，冰冷生蠔；生猛海鮮，值得啖一陣

「艇仔粥」是 **wulited** 的個人網站，記錄技術學習，也收留詩歌、生活片段與天馬行空的想像。

## 網站內容

- **Tech Talk**：網站搭建、Python 爬蟲、前端開發等實作筆記，分享學習與解決問題時的心得。
- **Tap Water**：以《再來七杯自來水》為名的詩歌專欄，寫日常、旅行、記憶與想念。
- **mini Ted Talk**：生活隨筆、小故事與年度總結，記錄一些選擇、觀察和腦洞。

## 本機預覽

本倉庫以 **Zensical** 建置靜態網站，文章以 Markdown 撰寫，使用 GitHub Pages 託管。
如需在本機瀏覽，請使用 Python 3.12：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
zensical serve
```

建置靜態頁面：

```bash
zensical build --clean --strict
```

文章與素材位於 [docs/](docs/)，網站設定位於 [mkdocs.yml](mkdocs.yml)，建置產物輸出至 `site/`。

## 版權

**Copyright © 2014–2026 wulited. All rights reserved.**

網站原創內容，包括文章、詩歌、隨筆與自製圖像，其版權均歸 **wulited** 所有，保留一切權利。使用與授權範圍見 [COPYRIGHT.md](COPYRIGHT.md)。

此作品版權聲明不適用於網站建置程式碼、樣式、模板、設定或部署腳本，也不變更它們的既有授權。

網站使用的第三方套件、圖示與引用素材，其權利歸各自的權利人所有，並依各自的授權條款使用。

聯絡作者：[x@wulited.com](mailto:x@wulited.com)。
