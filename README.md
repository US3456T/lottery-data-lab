# Lottery Data Lab

这是一个用于历史彩票数据分析和回测的本地 AI 分析工具，目标是帮助你快速查看号码热度、冷号、间隔、奇偶/大小分布，以及在历史数据上训练一个简单的学习模型，进行“AI 评分”。

注意：
- 本项目不保证中奖，也不宣称能预测彩票结果。
- 它专注于数据分析、回测和趋势可视化，适合研究和实验。
- 适合本地运行和自定义扩展。

## 功能
- 上传本地彩票 CSV 数据
- 自动解析常见开奖格式
- 号码热度 / 冷度 / 缺号分析
- 奇偶、大小、和值分布分析
- 近 10 / 近 20 期趋势
- 训练一个简单的“AI 学习模型”给每个号码打分
- 通过网页界面查看结果

## 启动

1. 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. 启动应用

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

3. 打开浏览器

```text
http://127.0.0.1:8000/
```

## CSV 格式示例

支持以下两种格式：

### 1. 单列号码字段

```csv
draw_id,date,numbers
1,2024-01-01,"3,8,12,19,28,35"
2,2024-01-04,"5,9,17,22,29,43"
```

### 2. 分列号码字段

```csv
draw_id,date,n1,n2,n3,n4,n5,n6
1,2024-01-01,3,8,12,19,28,35
2,2024-01-04,5,9,17,22,29,43
```

如果你有自己的开奖记录，直接上传即可。

## 项目说明

这个工具重点是：
- 助你分析历史开奖数据；
- 查看热门号与冷号；
- 查看周期性和分布规律；
- 让模型基于历史数据给出排序建议。

它不是“中奖预测器”，而是一个本地可用的分析工作台。

## 目录结构

```text
.
├── app.py
├── generate_sample_data.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_draws.csv
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── styles.css
├── utils/
│   └── lottery_analysis.py
└── .gitignore
```

## 生成示例数据

```bash
python generate_sample_data.py
```

随后本地运行 `uvicorn app:app --host 0.0.0.0 --port 8000 --reload` 即可查看示例结果。
