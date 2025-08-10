import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .utils import load_shoes, load_interactions

class HybridRecommender:
    def __init__(self):
        self.shoes_df = load_shoes()
        self.interactions_df = load_interactions()
        self._prepare_content_matrix()

    def _prepare_content_matrix(self):
        df = self.shoes_df.copy()

        # Safely ensure required columns exist
        if 'type' not in df.columns:
            df['type'] = ''
        if 'category' not in df.columns:
            df['category'] = ''
        if 'style' not in df.columns:
            df['style'] = ''
        if 'brand' not in df.columns:
            df['brand'] = ''

        # Create combined features
        df['features'] = (
            df['brand'].fillna('') + ' ' +
            df['type'].fillna('') + ' ' +
            df['category'].fillna('') + ' ' +
            df['style'].fillna('')
        )

        # Vectorize the features
        vectorizer = TfidfVectorizer(stop_words="english")
        self.content_matrix = vectorizer.fit_transform(df['features'])
        self.shoes_df = df

    def _content_based(self, shoe_id, top_n=5):
        if shoe_id not in self.shoes_df['shoe_id'].values:
            return []
        idx = self.shoes_df.index[self.shoes_df['shoe_id'] == shoe_id][0]
        cosine_similarities = cosine_similarity(
            self.content_matrix[idx], self.content_matrix
        ).flatten()
        similar_indices = cosine_similarities.argsort()[::-1][1: top_n + 1]
        return self.shoes_df.iloc[similar_indices]['shoe_id'].tolist()

    def _collaborative_filtering(self, user_id, top_n=5):
        user_shoes = self.interactions_df[
            self.interactions_df['user_id'] == user_id
        ]['shoe_id'].unique()

        scores = {}
        for shoe_id in user_shoes:
            similar = self._content_based(shoe_id, top_n=top_n)
            for s in similar:
                scores[s] = scores.get(s, 0) + 1

        sorted_shoes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [shoe_id for shoe_id, _ in sorted_shoes[:top_n]]

    def generate_recommendations(self, user_id, top_n=5):
        collab_recs = self._collaborative_filtering(user_id, top_n)
        seen = set()
        final_recs = []
        for sid in collab_recs:
            if sid not in seen:
                final_recs.append({"shoe_id": sid})
                seen.add(sid)
        return final_recs
