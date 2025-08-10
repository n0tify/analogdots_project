import pandas as pd
import os

# Path to data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def load_shoes(parse_dates=False):
    """
    Load shoe catalog CSV. 
    Ensures consistent column names and expected fields even if missing.
    """
    path = os.path.join(DATA_DIR, 'sample_shoe_catalog.csv')
    if not os.path.exists(path):
        raise FileNotFoundError(f"Shoe catalog not found at {path}")

    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    # Optional date parsing
    if parse_dates and 'release_date' in df.columns:
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    # Fill in missing expected columns
    if 'category' not in df.columns and 'type' in df.columns:
        df['category'] = df['type']
    if 'type' not in df.columns and 'category' in df.columns:
        df['type'] = df['category']
    if 'price' not in df.columns and 'price_usd' in df.columns:
        df['price'] = df['price_usd']

    # Ensure shoe_id exists and is integer
    if 'shoe_id' not in df.columns:
        df['shoe_id'] = range(1, len(df) + 1)
    else:
        df['shoe_id'] = pd.to_numeric(df['shoe_id'], errors='coerce').fillna(-1).astype(int)

    return df


def load_users():
    """
    Load user profiles CSV.
    Ensures user_id exists and is integer.
    """
    path = os.path.join(DATA_DIR, 'sample_user_profiles.csv')
    if not os.path.exists(path):
        raise FileNotFoundError(f"User profiles not found at {path}")

    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    if 'user_id' not in df.columns:
        df['user_id'] = range(1, len(df) + 1)
    else:
        df['user_id'] = pd.to_numeric(df['user_id'], errors='coerce').fillna(-1).astype(int)

    return df


def load_interactions(parse_dates=False):
    """
    Load user interactions CSV.
    Normalizes column names and ensures required IDs are integers.
    """
    path = os.path.join(DATA_DIR, 'sample_user_interactions.csv')
    if not os.path.exists(path):
        raise FileNotFoundError(f"User interactions not found at {path}")

    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    # Normalize column names
    if 'interaction_type' in df.columns and 'action' not in df.columns:
        df = df.rename(columns={'interaction_type': 'action'})

    if parse_dates and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Ensure numeric IDs
    if 'user_id' not in df.columns:
        df['user_id'] = -1
    else:
        df['user_id'] = pd.to_numeric(df['user_id'], errors='coerce').fillna(-1).astype(int)

    if 'shoe_id' not in df.columns:
        df['shoe_id'] = -1
    else:
        df['shoe_id'] = pd.to_numeric(df['shoe_id'], errors='coerce').fillna(-1).astype(int)

    return df


def load_weather(parse_dates=False):
    """
    Load weather data CSV.
    Ensures consistent column names and optional date parsing.
    """
    path = os.path.join(DATA_DIR, 'sample_weather.csv')
    if not os.path.exists(path):
        raise FileNotFoundError(f"Weather data not found at {path}")

    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    if parse_dates and 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    return df
