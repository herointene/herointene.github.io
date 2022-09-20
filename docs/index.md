---
hide:
  - navigation
  - toc
---
<script>
  // change index style: full page

  let styleElem = document.head.appendChild(document.createElement("style"));
  styleElem.innerHTML = `
    .md-main__inner {
      margin-top: 0;
      backgroud: white;
    }
  
    main> .md-grid {
      max-width: none;
    }
    .md-content__inner {
      margin: 0;
      padding-top: 0;
    }
    .md-content__inner:before {
      height: 0;
    }

  
  `

  
</script>
#
<h1 style="display:none">TingZaiZuk - 艇仔粥</h1>
<div class="titlecard">
  <div class = "tinggif">
    <img src = './assets/tinggif.gif' style="display: block; margin: auto;">
    <p>滾燙熱湯，冰冷生蠔；生猛海鮮，值得啖一陣</p>
  </div>
</div>
<div class="index">
  <div class="flexbox">
    <div class="contentcard">
      <div class="cardtitle">&#128187; 前端練習</div>
      <div class="cardinfo">
        <a style="display: block;" href="https://kanakill.netlify.app/" target="_blank">&#127800;KanaKill - 五十音練習&#128279;</a>
        <a style="display: block;" href="https://tangokill.netlify.app/" target="_blank">&#128218;TangoKill - 日語單詞卡&#128279;</a>
        <a style="display: block;" href="https://herointene.github.io/donatcal/withvue" target="_blank">&#128200;Donacal - 可視化的派對得分計算器&#128279;</a>
      </div>
    </div>
    <div class="contentcard">
      <div class="cardtitle">&#127760; mkdocs教學</div>
      <div class="cardinfo">
        <a style="display: block;" href="tech/mkdocsbuild/">&#128682;Material for Mkdocs 個人網站搭建入口</a>
      </div>
    </div>
    <div class="contentcard">
      <div class="cardtitle">&#128540; 純粹興趣</div>
      <div class="cardinfo">
        <a style="display: block;" href="tech/steam-crawling-python/">&#128376;Python爬取游戲榜單</a>
        <a style="display: block;" target="_blank" href="https://www.bilibili.com/video/BV1YT4y1372J?share_source=copy_web&vd_source=d8a6dfd1a191d941c82d16c48512ba70">&#127928;GarageBand&#128279;</a>
        <a style="display: block;" href="talk/about-life-choices/">> And More...</a>
      </div>
    </div>
  </div>
</div>