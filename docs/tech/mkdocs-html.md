# HTML in Mkdocs

在 Mkdocs 中，`.md` 文件與普通的 markdown 文件一樣都是可以用 html 的形式來進行編寫的。

## 一些 tips

### 在新標籤頁中打開某鏈接的方法

markdown 文件無法直接點開鏈接之後從新的標籤頁打開，因此需要用 html 的 `<a> </a>` tag 來操作，比如：

``` html
<a style="display: block;" href="https://kanakill.netlify.app/" target="_blank">&#127800;KanaKill - 五十音練習&#128279;</a>
```

### 在 `.md` 文件裏的 html 書寫規範

在 markdown 文件中，空行會被編譯為 `<p>` 標簽。所以盡可能的在寫 html 的過程中**不要**爲了美觀在各個大標簽裏面空行。


在下一篇文章中將講述 html 與其他語言結合進 mkdocs 的方法。


