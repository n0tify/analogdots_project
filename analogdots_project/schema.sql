-- schema.sql
-- PostgreSQL database schema for Shoe Recommendation & Personalized Service System

CREATE TABLE user_profiles (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT CHECK (age >= 0),
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
    typical_usage VARCHAR(50), -- e.g., Casual, Sports, Formal
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_profiles_location ON user_profiles(location);

CREATE TABLE shoe_catalog (
    shoe_id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    type VARCHAR(50), -- e.g., Sneakers, Boots, Loafers
    material VARCHAR(50),
    color VARCHAR(30),
    size NUMERIC(4,1) CHECK (size > 0),
    care_requirements TEXT,
    price NUMERIC(10,2) CHECK (price >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_shoe_catalog_brand_type ON shoe_catalog(brand, type);

CREATE TABLE user_interactions (
    interaction_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES user_profiles(user_id) ON DELETE CASCADE,
    shoe_id INT NOT NULL REFERENCES shoe_catalog(shoe_id) ON DELETE CASCADE,
    interaction_type VARCHAR(20) CHECK (interaction_type IN ('view', 'purchase', 'wishlist', 'care')),
    rating NUMERIC(2,1) CHECK (rating >= 0 AND rating <= 5),
    care_mode VARCHAR(50), -- e.g., Deep Clean, Quick Refresh
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_interactions_user_id ON user_interactions(user_id);
CREATE INDEX idx_user_interactions_shoe_id ON user_interactions(shoe_id);
CREATE INDEX idx_user_interactions_type ON user_interactions(interaction_type);

CREATE TABLE recommendation_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES user_profiles(user_id) ON DELETE CASCADE,
    recommended_shoes INT[] NOT NULL, -- Array of shoe_ids
    algorithm_used VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_recommendation_logs_user_id ON recommendation_logs(user_id);

CREATE TABLE environmental_data (
    env_id SERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    weather_condition VARCHAR(50), -- e.g., Rainy, Sunny, Snow
    temperature NUMERIC(4,1),
    UNIQUE (location, date)
);

CREATE INDEX idx_environmental_data_location_date ON environmental_data(location, date);
