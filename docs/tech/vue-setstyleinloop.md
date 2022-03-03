# Vue.js 循環裏匹配不同樣式

## 場景描述

通過 `v-for` 循環渲染出的元素，需要對每一個元素進行判斷，true 則顯示預設好的樣式，false 則普通樣式。

如果在 `v-for` 内的循環元素直接綁定 `$data` 裏的值，會出現所有元素都共享同一個開關。所以需要為每一個循環元素添加獨立的開關。

也就是説，遍歷的對象裏需要各自添加一個開關，并且它不需要受到 Vue 本身的數據劫持所控制（這樣會簡單許多，Vue 不用對它作 get/set 處理）。

## 步驟

1. 預設好 style class
2. 在循環元素標簽裏加入 `:class="handleStyleToggle(i)"`
   1. 傳入一個函數，parameter 為 `v-for` 所遍歷的那個對象
3. 於 `methods:` 加入該函數，加入判斷。

如果只需要單一 class，可以直接傳入 conditional operator （三元表達式）：

``` javascript
//...,
methods:{
  //...,
  handleStyleToggle(i){
    return i.StyleToggle === true? 'styleClass' : ''
  },
}


```

當有多個 class 需要傳入時， return 則是一個對象（待編輯）。

同樣的，在 methods 裏加入處理這個開關何時出發的 function：

``` javascript
//...,
methods:{
  //...,
  //以我的例子，我是通過點擊事件傳給以下 function 一個 i 對象
  toggleMyStyle(i){
    //...
    i.StyleToggle = true //如果沒有 StyleToggle 則會自動新增
    //但是它不受 Vue 的動態渲染所捕獲 i.e. 沒有 $get/$set 
  }

  handleStyleToggle(i){
    return i.StyleToggle === true? 'styleClass' : ''
  },
}

```

此時，html 應該是這樣子：

``` html

<div v-for="i in items" >
  <div :class="handleStyleToggle(i)" @click="toggleMyStyle(i)" >blabla<div>
<div>

```
結束。
