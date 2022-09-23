# Python 與 Mkdocs 安裝

我們從這一章開始就真正進入使用 Mkdocs 之中了。我會説明 Windows 下的安裝操作，在不久的將來會更新 Mac 版本的安裝操作，Mac 讀者們也可以閲覽官方文檔進行安裝。

## 安裝 Python & Mkdocs

我們將使用 Anaconda 下的 Python 作爲我們的 Mkdocs 啓動環境。這個概念對新手并不是很友好，因爲不知道 python 跟 Anaconda 到底有什麽關係。但這并不會有什麽大問題，理解不了的話可以照著接下來的教程操作，因爲往後的部分我們不會再接觸到 Anaconda 了。

1. 我們在 [Anaconda 下載頁面](https://www.anaconda.com/products/distribution)下載 Anaconda，並不斷的按下一步
。

!!! warning
    第一次安裝 python 的話請勾選  `add Anaconda to the PATH environment variable`，儘管它并不推薦我們這麽做，但對於只用於啓動 Mkdocs 的話選擇它會少掉許多步驟。

2. 當安裝器完成它的使命之後，你可以嘗試打開 Anaconda Navigator 驗證安裝成功與否。如果順利打開，請打開視圖界面裏的 `Anaconda Prompt`，輸入以下代碼：

```cmd
pip install mkdocs-material
```

這樣 python 就會自行下載 Material for Mkdocs 與它所需要的依賴包。

3.  接下來打開 VS Code （沒有 VS Code 的話直接下載即可），進入想要建立網站的文件夾裏，新建一個終端（Terminal），然後輸入

```cmd
mkdocs new .
```
4.  執行完畢后，如果在文件夾裏能看到如下文件，説明 Mkdocs 安裝成功了：

```
.
├─ docs/
│  └─ index.md
└─ mkdocs.yml
```

## 使用 Material for mkdocs

我們仍舊在 VS code 下，打開 `mkdocs.yml` 文件。這是一個配置文件，我們所有内容都需要遵從它所規定的格式與縮進。

複製如下的字句，即可使用 Material for mkdocs 模板：

```yaml
theme:
  name: material
```

回到我們的 Terminal，輸入以下代碼

```
mkdocs serve 
```

!!! success
    我們在每一次更新網站都會先用此代碼進行部署網頁前的預覽，非常重要！

之後點擊它出現的網站，你就可以進入你的網站預覽頁面了。

接下來，我們會對我們的網站開始進行初始設置，即下一篇的配置文件教程“mkdocs.yml 設置”。