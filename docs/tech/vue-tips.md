# Vue 項目開發中的心得

*本篇内容為 Vue 開發當中所遇到的困難與技巧的集合，涵蓋 JS、TS、CSS、Python 等語言。意在備忘的同時提供一個從初始到結束整個環節中的進程分享，確保在再啓新一次項目時吸取經驗與避開錯誤。陸續更新。*

---

<div style="margin:auto; width:100px; border:2px">前期準備</div>

## 創建 Vue 項目相關

### 1. Github 與 Vue 創建順序
在 Github 直接創建新項目，再 fork 到本地文件夾中，從文件夾裏的 cmd 創建 vue 項目時，會把項目文件夾建立在 GitHub 項目裏。常見的錯誤是當我打開 vscode 進行 `npm install` 時，沒有先進行 `cd vueproject` 步驟，導致依賴庫被安裝在母文件夾中。

!!! success
    先在本地創建好 vue 項目，再把它上傳到 Github 這樣的順序大概會是更好的選擇。

### 2. 清空模板
1. 清空 `Readme.md`
2. 添加作者名稱至 `LICENCE`
3. 添加項目名字與其他 meta - `index.html`
4. 更換 `public/favicon.ico`
5. 刪除 `router/index.ts` 裏的 routes
6. 刪除無用的 components，並重新更換新主頁。
7. 更換 `main.css/base.css` 中的風格樣式

### 3. 深色模式前期準備
- 在 Vue3 + Vite 版本中，模板的 `base.css` 存在 `@media (prefers-color-scheme: dark)`，如果使用手動控制深色模式功能的話需要把它改爲簡單的 `.dark{}`。

!!! tip
    Vue 的深色模式手動控制組件可參考 <a href="https://github.com/vuejs/theme/blob/main/src/core/components/VTSwitchAppearance.vue" target="_blank">VitePress 官方的組件</a>。


