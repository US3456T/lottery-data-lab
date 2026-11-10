<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Lottery Data Lab</title>
    <link rel="stylesheet" href="/static/styles.css" />
  </head>
  <body>
    <div class="page">
      <header class="topbar">
        <div>
          <p class="eyebrow">LOTTERY DATA LAB</p>
          <h1>彩票数据分析平台</h1>
        </div>
        <span class="status-badge">AI 数据研究</span>
      </header>

      <section class="toolbar">
        <form id="upload-form">
          <label for="csv-file">导入 CSV</label>
          <input id="csv-file" type="file" accept=".csv,text/csv" />
          <button type="submit">更新分析</button>
        </form>
        <button id="reset-demo" class="secondary" type="button">恢复演示数据</button>
      </section>

      <div id="message" class="message">加载中…</div>

      <section class="metrics">
        <div class="card">
          <span>数据期数</span>
          <strong id="draw-count">0</strong>
        </div>
        <div class="card">
          <span>数据源</span>
          <strong id="source">demo</strong>
        </div>
        <div class="card">
          <span>最大号码</span>
          <strong>49</strong>
        </div>
        <div class="card">
          <span>分析模块</span>
          <strong>20</strong>
        </div>
      </section>

      <section class="grid">
        <div class="panel">
          <h2>热点号码</h2>
          <ul id="hot-list"></ul>
        </div>
        <div class="panel">
          <h2>冷门号码</h2>
          <ul id="cold-list"></ul>
        </div>
        <div class="panel">
          <h2>缺失号码</h2>
          <div id="missing-list" class="chips"></div>
        </div>
        <div class="panel">
          <h2>近期热度</h2>
          <ul id="recent-list"></ul>
        </div>
      </section>

      <section class="grid second">
        <div class="panel">
          <h2>分布摘要</h2>
          <ul id="distribution-list"></ul>
        </div>
        <div class="panel">
          <h2>AI 学习排序</h2>
          <div id="ai-ranking" class="chips tall"></div>
        </div>
      </section>

      <section class="panel full">
        <h2>20 个分析模块</h2>
        <div id="module-list" class="module-grid"></div>
      </section>
    </div>

    <script src="/static/app.js"></script>
  </body>
</html>
