document.addEventListener('DOMContentLoaded', () => {
  const overviewEl = document.getElementById('overview');
  const hotList = document.getElementById('hot-list');
  const coldList = document.getElementById('cold-list');
  const aiRanking = document.getElementById('ai-ranking');
  const missingList = document.getElementById('missing-list');
  const distributionList = document.getElementById('distribution-list');
  const alertBox = document.getElementById('upload-alert');

  async function loadOverview() {
    const response = await fetch('/api/overview');
    const data = await response.json();

    if (data.error) {
      alertBox.textContent = data.error;
      alertBox.style.display = 'block';
      return;
    }

    document.getElementById('draw-count').textContent = data.draw_count;
    document.getElementById('source-name').textContent = data.source;
    document.getElementById('min-max').textContent = `${data.min_number} - ${data.max_number}`;

    renderList(hotList, data.hot_numbers.slice(0, 10));
    renderList(coldList, data.cold_numbers.slice(0, 10));
    renderList(missingList, data.missing_numbers.slice(0, 12));
    renderDistribution(distributionList, data.distribution);
    renderAiRanking(aiRanking, data.ai_ranking.top_numbers);
  }

  function renderList(el, items) {
    if (!items || !items.length) {
      el.innerHTML = '<li>暂无数据</li>';
      return;
    }

    el.innerHTML = items.map(item => `
      <li>
        <span>${item.number}</span>
        <strong>${item.value}</strong>
      </li>
    `).join('');
  }

  function renderDistribution(el, dist) {
    if (!dist || !dist.length) {
      el.innerHTML = '<li>暂无数据</li>';
      return;
    }

    el.innerHTML = dist.map(item => `
      <li>
        <span>${item.label}</span>
        <strong>${item.value}</strong>
      </li>
    `).join('');
  }

  function renderAiRanking(el, items) {
    if (!items || !items.length) {
      el.innerHTML = '<li>暂无数据</li>';
      return;
    }

    el.innerHTML = items.map(item => `
      <div class="inline-numbers">
        <span class="number-pill">${item.number}</span>
      </div>
    `).join('');
  }

  document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('csv-file');
    const file = fileInput.files[0];
    if (!file) {
      alertBox.textContent = '请选择 CSV 文件。';
      alertBox.style.display = 'block';
      return;
    }

    formData.append('file', file);
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      alertBox.textContent = data.error || '上传失败';
      alertBox.style.display = 'block';
      return;
    }

    alertBox.textContent = `已加载 ${data.filename}，共 ${data.draw_count} 期数据。`;
    alertBox.style.display = 'block';

    renderList(hotList, data.hot_numbers.slice(0, 10));
    renderList(coldList, data.cold_numbers.slice(0, 10));
    renderList(missingList, data.missing_numbers.slice(0, 12));
    renderDistribution(distributionList, data.distribution);
    renderAiRanking(aiRanking, data.ai_ranking.top_numbers);

    document.getElementById('draw-count').textContent = data.draw_count;
    document.getElementById('source-name').textContent = data.filename;
  });

  document.getElementById('retrain-btn').addEventListener('click', async () => {
    const response = await fetch('/api/retrain');
    const data = await response.json();
    alertBox.textContent = data.message || '模型已重训';
    alertBox.style.display = 'block';
    renderAiRanking(aiRanking, data.top_numbers);
  });

  loadOverview();
});
