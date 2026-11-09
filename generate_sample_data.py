from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


MAX_NUMBER = 49


def ensure_sample_data(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return

    start_date = datetime(2023, 1, 2)
    rows = []
    for idx in range(1, 301):
        date_value = (start_date + timedelta(days=idx * 3)).strftime('%Y-%m-%d')
        nums = sorted(random.sample(range(1, MAX_NUMBER + 1), 6))
        rows.append({
            'draw_id': idx,
            'date': date_value,
            'n1': nums[0],
            'n2': nums[1],
            'n3': nums[2],
            'n4': nums[3],
            'n5': nums[4],
            'n6': nums[5],
        })

    pd.DataFrame(rows).to_csv(path, index=False)


def _coerce_number_list(value):
    if pd.isna(value):
        return []
    if isinstance(value, str):
        parts = [part.strip() for part in value.replace(';', ',').split(',')]
        result = []
        for part in parts:
            if not part:
                continue
            try:
                result.append(int(float(part)))
            except ValueError:
                continue
        return result
    if isinstance(value, (list, tuple, set)):
        return [int(x) for x in value]
    return [int(value)]


def _normalize_draws(df: pd.DataFrame):
    normalized = []
    for _, row in df.iterrows():
        numbers = []
        for col in df.columns:
            if col.lower().startswith('n') or col.lower() in {'number', 'numbers', 'balls', 'nums'}:
                if col.lower() == 'numbers' or col.lower() == 'balls' or col.lower() == 'nums':
                    numbers.extend(_coerce_number_list(row[col]))
                elif col.lower().startswith('n'):
                    try:
                        numbers.append(int(row[col]))
                    except (TypeError, ValueError):
                        pass
        if not numbers and 'numbers' in row:
            numbers = _coerce_number_list(row['numbers'])
        if not numbers:
            continue
        numbers = sorted({int(n) for n in numbers if 1 <= int(n) <= MAX_NUMBER})
        if len(numbers) >= 6:
            normalized.append({
                'draw_id': row.get('draw_id', len(normalized) + 1),
                'date': row.get('date', ''),
                'numbers': numbers[:6],
            })
    return normalized


def load_history_from_csv(path: str | Path):
    p = Path(path)
    if not p.exists():
        return []

    try:
        df = pd.read_csv(p)
    except Exception:
        return []

    if df.empty:
        return []

    return _normalize_draws(df)


def analyze_draws(draws):
    if not draws:
        return {
            'draw_count': 0,
            'min_number': 1,
            'max_number': MAX_NUMBER,
            'hot_numbers': [],
            'cold_numbers': [],
            'missing_numbers': [],
            'recent_trends': [],
            'distribution': [],
        }

    all_numbers = [num for draw in draws for num in draw['numbers']]
    counts = pd.Series(all_numbers).value_counts().sort_index()

    hot_numbers = [
        {'number': int(num), 'value': int(counts[num])}
        for num in counts.sort_values(ascending=False).head(10).index
    ]

    cold_numbers = [
        {'number': int(num), 'value': int(counts[num])}
        for num in counts.sort_values(ascending=True).head(10).index
    ]

    missing_numbers = [
        int(n) for n in range(1, MAX_NUMBER + 1)
        if n not in counts.index
    ]

    recent_window = draws[-10:]
    recent_trends = []
    for number in range(1, MAX_NUMBER + 1):
        seen = sum(1 for draw in recent_window if number in draw['numbers'])
        recent_trends.append({'number': number, 'value': seen})

    recent_trends = sorted(recent_trends, key=lambda x: x['value'], reverse=True)[:10]

    odd_even = {
        'odd': sum(1 for n in all_numbers if n % 2 == 1),
        'even': sum(1 for n in all_numbers if n % 2 == 0),
    }
    high_low = {
        'low': sum(1 for n in all_numbers if n <= 24),
        'high': sum(1 for n in all_numbers if n > 24),
    }
    sum_values = [sum(draw['numbers']) for draw in draws]

    distribution = [
        {'label': 'Odd', 'value': odd_even['odd']},
        {'label': 'Even', 'value': odd_even['even']},
        {'label': 'Low (1-24)', 'value': high_low['low']},
        {'label': 'High (25-49)', 'value': high_low['high']},
        {'label': 'Avg Sum', 'value': round(sum(sum_values) / len(sum_values), 2)},
    ]

    return {
        'draw_count': len(draws),
        'min_number': min(all_numbers) if all_numbers else 1,
        'max_number': max(all_numbers) if all_numbers else MAX_NUMBER,
        'hot_numbers': hot_numbers,
        'cold_numbers': cold_numbers,
        'missing_numbers': missing_numbers,
        'recent_trends': recent_trends,
        'distribution': distribution,
    }


def _feature_row(draws, number, idx):
    history = draws[:idx + 1]
    last_5 = sum(1 for draw in history[-5:] if number in draw['numbers'])
    last_10 = sum(1 for draw in history[-10:] if number in draw['numbers'])
    total_seen = sum(1 for draw in history if number in draw['numbers'])
    gaps = []
    last_seen = None
    for step, draw in enumerate(history):
        if number in draw['numbers']:
            if last_seen is not None:
                gaps.append(step - last_seen)
            last_seen = step

    avg_gap = round(sum(gaps) / len(gaps), 2) if gaps else 0
    return {
        'number': number,
        'last_5': last_5,
        'last_10': last_10,
        'total_seen': total_seen,
        'avg_gap': avg_gap,
        'trend': last_10 + last_5,
    }


def build_ai_ranking(draws):
    if len(draws) < 20:
        simple = []
        counts = {}
        for draw in draws:
            for n in draw['numbers']:
                counts[n] = counts.get(n, 0) + 1
        for number, count in sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:20]:
            simple.append({'number': number, 'score': float(count)})
        return {'top_numbers': simple, 'training_rows': 0}

    training_rows = []
    max_idx = len(draws) - 1
    for idx in range(10, max_idx):
        for number in range(1, MAX_NUMBER + 1):
            row = _feature_row(draws, number, idx)
            label = 1 if number in draws[idx + 1]['numbers'] else 0
            training_rows.append({
                'number': row['number'],
                'last_5': row['last_5'],
                'last_10': row['last_10'],
                'total_seen': row['total_seen'],
                'avg_gap': row['avg_gap'],
                'trend': row['trend'],
                'label': label,
            })

    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    df = pd.DataFrame(training_rows)
    if df.empty:
        return {'top_numbers': [], 'training_rows': 0}

    X = df[['last_5', 'last_10', 'total_seen', 'avg_gap', 'trend']]
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = LogisticRegression(max_iter=500, random_state=42)
    model.fit(X_train, y_train)

    latest_history = draws[-30:]
    current_features = []
    for number in range(1, MAX_NUMBER + 1):
        row = _feature_row(latest_history, number, len(latest_history) - 1)
        current_features.append({
            'number': number,
            'last_5': row['last_5'],
            'last_10': row['last_10'],
            'total_seen': row['total_seen'],
            'avg_gap': row['avg_gap'],
            'trend': row['trend'],
        })

    feature_df = pd.DataFrame(current_features)
    probs = model.predict_proba(feature_df[['last_5', 'last_10', 'total_seen', 'avg_gap', 'trend']])[:, 1]
    feature_df['score'] = probs

    top = feature_df.sort_values(['score', 'number'], ascending=[False, True]).head(20)
    result = [
        {'number': int(row['number']), 'score': round(float(row['score']), 4)}
        for _, row in top.iterrows()
    ]

    return {'top_numbers': result, 'training_rows': len(df)}
