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

### 2.1 Vitesse 模板
1. unoCSSconfig 裏的 shortcut 中更改或刪除預設樣式

### 3. 深色模式前期準備
- 在 Vue3 + Vite 版本中，模板的 `base.css` 存在 `@media (prefers-color-scheme: dark)`，如果使用手動控制深色模式功能的話需要把它改爲簡單的 `.dark{}`。

!!! tip
    Vue 的深色模式手動控制組件可參考 <a href="https://github.com/vuejs/theme/blob/main/src/core/components/VTSwitchAppearance.vue" target="_blank">VitePress 官方的組件</a>。

### 4. 關閉 prettier/prettier
- 更新了 package 之後有時候 eslint 會提示很多無理由的錯誤，幾乎每行代碼後面都有提示錯誤的空格，這是由於 CRLF 與 LF 的關係，在 vscode 右下角調整就好。但是一些可容忍的寫法依舊會不斷提示錯誤，讓我心煩氣躁，只能關閉 prettier 代碼美化模塊。
- 解決辦法：`.eslintrc.cjs` 裏添加如下代碼，直接在 `module.export = {` 下面:
```json
  "rules": {
    "prettier/prettier": 0
  },
```

## JS/TS 相關

### 1. TypeScript 與 localStorage
- 存讀 JSON 格式的時候在 pinia 的 data 存儲中會遇到報錯，因爲無法取一個 null （第一次取時），我們需要斷言。
``` typescript
state: () => ({
  user: JSON.parse(localStorage.getItem('user') as string)
})
//我習慣寫以下代碼，待驗證是否多餘
//...
user: JSON.parse(localStorage.getItem('user') as string) || [] as User[],
//...
interface User {
  // freely
  id: string
  timestamp: number
  language:string
  topic: string
  note: string
  pin: boolean
  user: string
}

```

### 2. TypeScript 添加 JSON 文件

- 默認 TypeScript 在編譯的時候不能引入 JSON 文件，需要手動在 `tsconfig.json` 裏設置。

!!! bug
    在我的 vue3 + vite 版本中，嘗試了很多方法可是引入 JSON 依舊彈出 warning。於是我把所有方法放在一起，錯誤便消失了。

```json
//tsconfig.json
{
  "include": ["src/**/*.ts", "src/**/*.json"], //1：include 這些類型的文件
  "compilerOptions": {
    "resolveJsonModule": true, //2：允許引入 json 文件
  },
}

```

在我的 `tsconfig.json` 文件中，配置了 `references`，并且有 3 個另外的 tsconfig 文件。
第三點是刪除 `tsconfig.json` 中的 `"compilerOptions"` 中的 `"composite": true`，另外三個配置文件均有該選項，所以我都注釋掉了。重啓 VSCode 之後錯誤不見了。
## 樣式相關

### 1. CSS Flexbox 相關
1. justify & align 的區別在於前者使物品左右挪動、後者為上下挪動。官方説法是 align items on main axis or on cross axis.
2. 當 flex-direction 設置爲 column 時，main axis & cross axis 會調換位置，此時如果想要在垂直方向居中需要使用 justify-center 而不是 align-center。
3. Flexbox 之中的某一個物件想要有滾動條滾動時，需要同時設置 overflow:auto 和 height(maxheight)。

### 2. CSS & v-bind
1. vue.js 可以使用 v-bind 在 `<style>` 裏，像：

```CSS

p {
  color: v-bind('theme.color');
}

```

在 `<script>` 中，用 ref 或 reactive 聲明動態數據，可以實現 CSS 的動態變化。

```js

import {reactive} from 'vue'
const theme = reactive({
  color: 'red'
})

```

### 3. 安裝 SASS/SCSS 預載

在 vite 脚手架中，用以下代碼安裝

```shell

# .scss and .sass
npm add -D sass

```