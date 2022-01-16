# mkdocs 導航欄設置心得

當你完成了一系列的文章之後，整理出好看的文章路徑也是需要稍加思考的事情。從一開始就計劃自己的導航欄的方向，會防止產生之後在很多文章雜亂不堪擺在網頁上的時候的那種焦躁與無助感。

## 設置 mkdocs 前

在還沒有開始搭建 mkdocs 的時候，應該先構想出未來的網頁導航欄是怎樣的。可以把同類型的文章放在一個文件夾內，便可以完成簡單的導航欄：

```
├─ My-Life/
│  ├─ My-Fav-Songs.md
│  ├─ My-Cook-Book.md
│  ├─ How-to-control-my-wallet.md
│  ├─ Best-50-games-in-wishlist.md
│  └─ ...
└─ My-Fantastic-Time-Maze/
   ├─ Chapter1.md
   ├─ Chapter2.md
   ├─ ...
```

請注意，一般文件夾與文檔用英文命名，並且名稱之中的空格用 連字符（-）或下劃線（_）表示，這樣是為了後來的網站 url 更統一和避免錯誤的出現。

至此，你已完成內容前期的搭建，再後來只需要把這些文件夾移入 mkdocs 設置之後的文檔文件夾裡就可以了，請前往 mkdocs 安裝進行搭建。

---

## 創建 mkdocs 項目之後

當創建完 mkdocs 項目之後，你應該將所有包含文檔的文件夾統一放進 mkdocs 項目文件夾的 `/docs`  裏。

在默認模式下，你的導航欄會根據以下優先級順序顯示文檔名稱：

**`mkdocs.yml` nav 設置的順序**  &#187; **文檔裏的標題（#）** &#187; **文檔命名**

在 `mkdocs.yml` 沒有設置 nav 的時候，網頁會自動把你的文件夾設爲導航欄的入口，網頁左邊的導航列表則爲文件夾裏的所有文章標題。但是文件夾裏的文章不可以更改順序。

如果想更改順序，且想在文件夾裏的那些文章再分小標題，可以加上 nav 設置：


=== "mkdocs.yml"
    ```yaml
    nav:
        - My Perfect Life:
            Favourite:    
                Songs: My-Life/My-Fav-Songs.md
                Cooking: My-Life/My-Cook-Book.md
                Games: My-Life/Best-50-games-in-wishlist.md
            Feeling:
                Where's my money: My-Life/How-to-control-my-wallet.md
        - My Fantastic Time Maze:
            Chapter1: My-Fantastic-Time-Maze/Chapter1.md
            Chapter2: My-Fantastic-Time-Maze/Chapter2.md
    ```
=== "file"
    ```
    docs/
    ├─ My-Life/
    │  ├─ My-Fav-Songs.md
    │  ├─ My-Cook-Book.md
    │  ├─ How-to-control-my-wallet.md
    │  ├─ Best-50-games-in-wishlist.md
    │  └─ ...
    └─ My-Fantastic-Time-Maze/
    ├─ Chapter1.md
    ├─ Chapter2.md
    ├─ ...
    ```

可以見到，nav 下面以連字符（-）開始的語句代替了文件夾的名稱，而往下的“Favourite”標簽則爲文件夾裏的小標題隔開文章們。

!!! Warning
    當你使用 nav 重新調整導航欄的話，所有想要顯示進網頁的文章都需要填寫在 nav 裏，如果沒有寫，mkdocs 會以爲你不想把某篇文章顯示出來。并且，每個文檔前面都要爲它賦予顯示的名字，就算是文章内的標題也要重複地寫在文章路徑的冒號前面！

至此，你就完成了導航欄的設置。它是一項重複性的活動，每次更改文檔名、添加或刪除每個新文檔都必須在 nav 裏進行登記，像是領取出生證明一樣。

<br>