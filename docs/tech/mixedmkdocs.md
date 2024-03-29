# HTML與Markdown混合使用的頁面

### 介紹

Mkdocs 使用 Markdown 格式的文檔方便執筆者，但在網頁可擴展性方面并沒有很高。但在 Mkdocs 框架裏 Markdown 文檔裏面是支持讀取 HTML 格式的，也就是說將 HTML 與 Markdown 混合使用會有更高的自由度，配合CSS也可以補充更多的網頁樣式。


比如艇仔粥的 v1.0 首頁就是用了混合頁面元素：markdown 的分割綫，CSS 渲染的卡片……

![](img/mixedmkdocs1.png)

本文通過 Markdown 格式從頭到尾的順序介紹可以混合的方式。

### META DATA

在本文檔最上方加上 meta data ，前提是需要在配置頁面 ```mkdocs.yml``` 裏加上 extensions:

```yaml
markdown_extensions:
  - meta
```

!!! tips
    2022年更新：現在不需要配置 `- meta`，可以直接在 markdown 上使用下述配置語句。


meta data 有什麽用處呢？目前它可以通過在頁首添加如下代碼來隱藏左右兩邊的網頁目錄以及頁面内章節目錄：

```yaml
---
hide:
  - navigation
  - toc
---
```

或者 tags：

```yaml
---
tags:
  - sharing
  - python
---
```

標簽 Tags 是 2022 年更新的功能，請查看[官網文檔](https://squidfunk.github.io/mkdocs-material/setup/setting-up-tags/?h=tags)設置。

### HTML 與 CSS

接下來便可以使用 HTML 于正文内。請注意，雖然 CSS 可以放在 HTML 裏，但强烈建議在 mkdocs 教學文檔所説的那樣，另開一個 ```extra.css``` 。因爲這樣網頁可以一開始一次性讀取所有 CSS，在點開其他頁面的時候有更快的讀取速度而不會逐條讀取 CSS 内容。

例如我在下方加上一個黑色框框：

<div class="fullblock">
這是一個測試盒子
</div>

代碼是這樣子的：


=== "HTML"
    ```html
    <div class="fullblock">
    這是一個測試盒子
    </div>

    ```
=== "CSS"
    ```css
    .fullblock{
    width: 100%;
    padding: 50px;
    border-radius: 30px;
    background-color: black;
    color: #ffffff;  
    }
    ```

### 同時，自如地使用 Markdown

在這篇教程裏，我也運用了混合 HTML 與 Markdown 的方法，我的源代碼如下，比如現在便是正常模式下的 md 寫作，不信你看：

```
### HTML 與 CSS

接下來便可以使用HTML于正文内。請注意，雖然 CSS 可以放在 HTML 裏，但强烈建議在 mkdocs教學文檔所説的那樣，另開一個 ```extra.css``` 。因爲這樣網頁可以一開始一次性讀取所有 CSS，在點開其他頁面的時候有更快的讀取速度而不會逐條讀取 CSS 内容。

例如我在下方加上一個黑色框框：

<div class="fullblock">
這是一個測試盒子
</div>

代碼是這樣子的：


=== "HTML"
    ```html
    <div class="fullblock">
    這是一個測試盒子
    </div>

    ```
=== "CSS"
    ```css
    .fullblock{
    width: 100%;
    padding: 50px;
    border-radius: 30px;
    background-color: black;
    color: #ffffff;  
    }
    ```

### 同時，自如地使用 Markdown

在這篇教程裏，我也運用了混合 HTML 與 Markdown 的方法，我的源代碼如下，比如現在便是正常模式下的 md 寫作，不信你看：
……
```

好了，停下循環！

### 小技巧

在我 [TapWater](../poems/preface.md) 欄目裏，我運用了大量的空行。但在 md 格式裏，多餘的空行轉譯的時候會被自動忽略的。如何優雅地解決呢？

。。。
<br>
<br>
<br>
<br>
<br>
<br>
<br>


<h1> 使用 br tag ！！！</h1>

```
~ <br> ~
```

我很喜歡 Mkdocs。這種簡單易上手并且可以自由的搭配的文檔網頁框架，讓内容產出和美觀嚴謹達到了新的高度，尤其是看完官方文檔發現可以混合使用這些元素，馬不停蹄就運用並記錄下來。