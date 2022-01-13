# Mkdocs 漢語字體設置

在Material for Mkdocs中，漢語中文本身自帶。由於其本身自帶的字體為 Roboto，中文顯示與英文一樣是非襯綫字體。但mfm允許用戶使用HTML支持的字體，但更簡單的方法是只用Google Fonts提供的字體。

目前Google Fonts擁有8種不同類的字體（僅Noto支持近乎所有繁體字）。一般情況下大多數人只想轉換Serif/Sans Serif字體，其他字體雖然彰顯個性但有些字不支持改字體會顯得與内容格格不入，影響整體美觀。

mfm官方文檔沒有列出如何設置中文字體，這使得許多人在設置字體后并沒有變化。原因是字體名稱在`mkdocs.yml`文件裏與Google Fonts顯示的字體名稱不同。

以 Noto Serif Simplified Chinese 舉例，在設置文檔裏需把 “簡體中文”進行縮寫：

``` yaml
theme:
  font:
    text: Noto Serif SC       <------ 請注意此處被改爲 "SC" 。
```

!!! note
    建議使用簡中SC,有些簡化字在繁中（TC）裏沒有被收錄。

    不建議對code block裏的字體進行修改，非襯綫字體和等寬字體在顯示代碼以及較小字體的時候顯得格外清晰。

設置完成后，Noto Serif 字體在 Apple OS 設備中，導航欄上方的的網站名字超過2個字就會被縮略，使得網站標題欄位失去意義。如果要修復此錯誤，需要通過加入個性化的CSS樣式表進行精確更改：

在你的網站文件夾裏加入`extra.css`:

```
├─ docs/
│  └─ stylesheets/
│     └─ extra.css
└─ mkdocs.yml
```

然後在`mkdocs.yml`文檔裏加入代碼以啓用外挂樣式表：

```yaml
extra_css:
  - stylesheets/extra.css
```

最後在`extra.css`裏添加以下代碼：

``` CSS
.md-header__topic > .md-ellipsis {
    overflow: visible;
    text-overflow: ellipsis; 
    white-space: nowrap; 
}
/* text-overflow 與 white-space 兩個并不會生效，因爲overflow永遠都是可視的。
寫在這裏只是因爲他們三者平時經常混在一起而已。 */

```    

會發現在 Apple OS 設備裏的網頁標題欄被展開。這是由於mfm默認的標題内置overflow功能被定義爲“太長會被隱藏”，變成visible之後不管多長的文字都會被展開來，除非超出設備顯示寬度（但應該不會有人把自己的網站叫那麽長吧……）。