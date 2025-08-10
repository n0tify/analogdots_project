import sys
from pathlib import Path

# Ensure project root is in sys.path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

import json
import pandas as pd
from tabulate import tabulate
import shutil

from recommendation_system.personalized_services import (
    generate_hybrid_recommendations,
    generate_proactive_care_alerts,
    generate_replacement_suggestions,
    generate_weather_aware_recommendations
)
from recommendation_system.utils import load_users, load_shoes


def color(text, code):
    return f"\033[{code}m{text}\033[0m"

def print_section(title, char="="):
    width = shutil.get_terminal_size((100, 20)).columns
    print("\n" + char * width)
    print(color(title, "1;36"))
    print(char * width)

def print_recommendations(recs, shoes_df):
    if not recs:
        print(color("No recommendations available.", "2"))
        return

    rows = []
    for i, rec in enumerate(recs, start=1):
        shoe_id = rec.get("shoe_id")
        shoe = shoes_df[shoes_df["shoe_id"] == shoe_id]
        if not shoe.empty:
            s = shoe.iloc[0]
            name = str(s.get("name", "")).strip()
            brand = str(s.get("brand", "")).strip()
            category = str(s.get("category", "")).strip()
            price = s.get("price", "")
            price = f"${price:,.2f}" if pd.notna(price) else "N/A"
            rows.append([i, name, brand, category, price])

    colalign = ("center", "left", "left", "center", "right")
    print(tabulate(
        rows,
        headers=["Rank", "Shoe Name", "Brand", "Category", "Price"],
        tablefmt="rounded_outline",
        colalign=colalign
    ))

def main():
    users_df = load_users()
    shoes_df = load_shoes()

    for _, user in users_df.iterrows():
        user_id = user["user_id"]
        user_name = user['name']


        print_section(f"Hybrid Recommendations for {user_name}")
        hybrid_recs = generate_hybrid_recommendations(user_id)
        print_recommendations(hybrid_recs, shoes_df)

        print_section(f"Proactive Care Alerts for {user_name}")
        care_alerts = generate_proactive_care_alerts(user_id)
        if care_alerts:
            for alert in care_alerts:
                print(f"- {alert}")
        else:
            print(color("No proactive care alerts for this user.", "2"))

        print_section(f"Replacement Suggestions for {user_name}")
        replacement_suggestions = generate_replacement_suggestions(user_id)
        print_recommendations(replacement_suggestions, shoes_df)

        print_section(f"Weather-Aware Recommendations for {user_name}")
        weather_recs = generate_weather_aware_recommendations(user_id)
        print_recommendations(weather_recs, shoes_df)

if __name__ == "__main__":
    print(color("┌" + "─" * 101 + "┐", "36"))
    print(color("│ AnalogDots Shoe Recommendation System".ljust(102) + "│", "36"))
    print(color("│ Demo Mode".ljust(102) + "│", "36"))
    print(color("└" + "─" * 101 + "┘\n", "36"))
    main()
