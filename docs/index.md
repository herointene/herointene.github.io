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



<div class="titlecard">
  <div class = "tinggif">
    <img src = './assets/tinggif.gif' style="display: block; margin: auto;">
    <p>滾燙熱湯，冰冷生蠔；生猛海鮮，值得啖一陣</p>
  </div>
</div>


<div class="index">

  <div class="flex-container-right">
    <div class="head-container-left">
      <h2>搭建 Mkdocs </h2>
      <h4>簡約的個人網站搭建教學，純粹心得</h4>
    </div>
    <div class="card">
      <a href="./tech/mkdocsbuild">
        <img src="mis/sunf.jpg" alt=" " style="width:100%">
        <div class="container">
          <h4><b>Mkdocs 搭建：快速導覽</b></h4>
          <p>輕鬆閲讀，快速上手</p>
        </div>
      </a>
    </div>
  </div>

  <div class="flex-container">
    <div class="head-container">
      <h2>下弦之伍</h2>
      <h4>搞錯，但都是蜘蛛啦</h4>
    </div>
    <div class="card">
      <a href="./tech/steam-crawling-python">
        <img src="mis/steampy.jpg" alt=" " style="width:100%">
        <div class="container">
          <h4><b>爬取Steam游戲榜單</b></h4>
          <p>分析的第一步：打開Python！</p>
        </div>
      </a>
    </div>
  </div>

  <div class="flex-container-right">
    <div class="head-container-left">
      <h2>加點個性</h2>
      <h4>這個頁面好看嗎？</h4>
    </div>
    <div class="card">
      <a href="./tech/mixedmkdocs">
        <img src="mis/mixmk.jpg" alt=" " style="width:100%">
        <div class="container">
          <h4><b>Mkdocs 混合頁面</b></h4>
          <p>markdown+HTML+CSS</p>
        </div>
      </a>
    </div>
  </div>

  <div class="flex-container-right">
    <div class="fullblock" style="width:600px; background-image: url(mis/tapwaterbg.png);">
      <h1>TapWater</h1>
      <p>再來七杯自來水，持續更新...</p>
      <div class="relativebox">
        <a class="btn" href="./poems/preface">
          > 擰開
        </a>
      </div>
    </div>
    <div class="fullblock" style="background-color: #FCA5A5 ; background-position: bottom;">
      <h1>KanaKill</h1>
      <p>一個日本五十音練習游戲</p>
        <div class="relativebox">
          <a class="btn" style="background-color: #FDD9D9" href="https://kanakill.netlify.app" target="_blank">
          > 努力
          </a>
      </div>
    </div>
  </div>
  
  <div class="garagebandcontainer"> 
    <div class="garagebandtextbox">
      <div><img src="./mis/garagebandicon.png" style="width: 100px;"></div>
      <div><img src="mis/garagebandtext.png" style="width:1000px;"></div>
      <h3>模仿、抄襲、致敬，生活。</h3>
      <h4>主頁面敬請期待</h4>
    </div>
    <div class="garagebandbox">
    <iframe src="//player.bilibili.com/player.html?aid=925581718&bvid=BV1YT4y1372J&cid=188741128&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width= "540px" height="360px"> </iframe>
    </div>
  </div>

  <div class="flex-container-right">
    <div class="head-container-left">
      <h2>我説：</h2>
      <h4>你不好好學習，將來怎麽養活自己？</h4>
    </div>
    <div class="card">
      <a href="./talk/about-life-choices">
        <img src="mis/oldmancard.png" alt=" " style="width:100%">
        <div class="container">
          <h4><b>關於選擇</b></h4>
          <p>那年是七年級的夏天，我第一次明白：只要擁有白石洲一棟樓，一世就都不用愁。</p>
        </div>
      </a>
    </div>
  </div>



  <div class="flex-container">
    <div class="head-container">
      <h2>那晚的流星……</h2>
    </div>
    <div class="card">
      <a href="./talk/grant-wishes">
        <img src="mis/bluepole.jpg" alt=" " style="width:100%">
        <div class="container">
          <h4><b>許願</b></h4>
          <p>看到流星，記得按A鍵許願</p>
        </div>
      </a>
    </div>
  </div>

  <div class="flex-container-right">
    <div class="head-container-left">
      <h2>秋末 冬至</h2>
      <h4>書寫夢境裏的湯圓大軍</h4>
    </div>
    <div class="card">
      <a href="./talk/digital-sweetdumpling">
        <img src="mis/tingqianchuiliu.png" alt=" " style="width:100%">
        <div class="container">
          <h4><b>電子湯圓</b></h4>
          <p>“刺繡五紋添弱線，吹葭六管動浮灰。”</p>
        </div>
      </a>
    </div>
  </div>

  <h4 style="text-align: center; font-size: 10px; color: gray; margin-bottom: 0;">更多首頁導覽内容，敬請期待下一次更新……</h4>

</div>
