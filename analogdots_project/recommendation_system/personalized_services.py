import pandas as pd
from datetime import datetime, timedelta
from .utils import load_shoes, load_interactions, load_weather
from .recommender import HybridRecommender
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TODAY = datetime(2024, 9, 30)  # fixed for demo reproducibility

def proactive_care_alerts(user_id, month_window_days=30, wear_threshold=20):
    interactions = load_interactions(parse_dates=True)
    shoes = load_shoes()
    start = TODAY - timedelta(days=month_window_days)
    mask = (interactions['user_id'] == user_id) & (interactions['action'] == 'wear') & (interactions['timestamp'] >= pd.Timestamp(start))
    counts = interactions[mask].groupby('shoe_id').size().to_dict()
    alerts = []
    for shoe_id, cnt in counts.items():
        if cnt >= wear_threshold:
            shoe = shoes[shoes['shoe_id'] == int(shoe_id)].iloc[0]
            alerts.append({
                'shoe_id': int(shoe_id),
                'message': f"Your {shoe['brand']} {shoe['model']} has been worn {cnt} times in the last {month_window_days} days. Recommend: {shoe['care_requirements']}"
            })
    return alerts

def replacement_suggestions(user_id, wear_total_threshold=50, age_days_threshold=365):
    interactions = load_interactions(parse_dates=True)
    shoes = load_shoes(parse_dates=True)
    purchases = interactions[(interactions['user_id'] == user_id) & (interactions['action'] == 'purchase')]
    suggestions = []
    for _, row in purchases.iterrows():
        shoe_id = int(row['shoe_id'])
        purchase_date = pd.to_datetime(row['timestamp'])
        wear_count = interactions[(interactions['user_id'] == user_id) & (interactions['shoe_id'] == shoe_id) & (interactions['action'] == 'wear')].shape[0]
        age_days = (TODAY - purchase_date.to_pydatetime()).days
        if (age_days > age_days_threshold and wear_count > wear_total_threshold) or (wear_count > 2 * wear_total_threshold):
            shoe = shoes[shoes['shoe_id'] == shoe_id].iloc[0]
            hr = HybridRecommender()
            similar = hr.generate_recommendations(user_id, top_n=3)
            suggestions.append({
                'shoe_id': shoe_id,
                'message': f"Consider replacing {shoe['brand']} {shoe['model']} (worn {wear_count} times; purchased {purchase_date.date()}). Suggested replacements: {similar}"
            })
    return suggestions

def weather_aware_recommendations(user_id, location='Delhi'):
    weather = load_weather(parse_dates=True)
    upcoming = weather[(weather['location'] == location) & (pd.to_datetime(weather['date']) >= TODAY)]
    heavy_rain = upcoming['precipitation_mm'].max() if not upcoming.empty else 0
    hr = HybridRecommender()
    base_recs = hr.generate_recommendations(user_id, top_n=6)
    if heavy_rain >= 8:
        shoes = load_shoes()
        filtered = [s for s in base_recs if str(shoes[shoes['shoe_id'] == s]['material'].values[0]).lower() in ['leather','synthetic','rubber']]
        if filtered:
            return filtered[:6]
    return base_recs

# === Wrappers to match run_demo.py expected names ===
def generate_hybrid_recommendations(user_id):
    hr = HybridRecommender()
    return hr.generate_recommendations(user_id, top_n=6)

def generate_proactive_care_alerts(user_id):
    return proactive_care_alerts(user_id)

def generate_replacement_suggestions(user_id):
    return replacement_suggestions(user_id)

def generate_weather_aware_recommendations(user_id):
    return weather_aware_recommendations(user_id)

if __name__ == "__main__":
    print("Care alerts for user 1:", proactive_care_alerts(1, month_window_days=30, wear_threshold=15))
    print("Replacement suggestions for user 1:", replacement_suggestions(1))
    print("Weather-aware recs for user 1:", weather_aware_recommendations(1))
