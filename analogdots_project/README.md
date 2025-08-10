# 👟 Shoe Recommendation System & Personalized Services

## 📌 Objective
This project was developed as part of the **AnalogDots Machine Learning Engineer / Data Scientist Competency Assessment**.  
It demonstrates the ability to:
- Design and implement a **shoe recommendation algorithm**.
- Develop **personalized services** based on user interaction patterns.
- Create a **PostgreSQL database schema** to store and manage relevant data.

---

## 📂 Repository Structure
analogdots_project/
│── recommendation_system/
│ ├── run_demo.py
│ ├── recommender.py
│ ├── personalized_services.py
│ ├── init.py
│
│── data/
│ ├── sample_user_interactions.csv
│ ├── sample_shoe_catalog.json
│
│── schema.sql
│── requirements.txt
│── README.md


---

## 🧠 Recommendation Algorithm

### **Chosen Approach**: **Hybrid Filtering**  
This system combines:
1. **Content-Based Filtering** – matches shoes to users based on shoe attributes and user preferences.
2. **Collaborative Filtering** – identifies patterns from similar users’ interactions.

**Rationale:**
- **Content-based** ensures recommendations work even for new users with little history.
- **Collaborative filtering** boosts accuracy for returning users by leveraging community trends.
- Hybrid methods are widely used in production systems (Netflix, Amazon) for their robustness.

**Algorithm Workflow:**
1. Load synthetic dataset from `/data/`.
2. Build a **user-shoe interaction matrix**.
3. Apply **cosine similarity** for content similarity.
4. Use **Nearest Neighbors** (Scikit-learn) for collaborative filtering.
5. Merge scores from both methods to produce ranked recommendations.

---

## 🎯 Personalized Service Logic

Two key personalized services are implemented:

### **1. Proactive Shoe Care Notifications**
- **Logic:**  
  - Track wear frequency & care history from device logs.
  - If a shoe has been worn >50 times since last care OR weather is rainy, send a **cleaning reminder**.
- **Pseudocode:**
```python
if wear_count > 50 or weather_condition in ["Rain", "Snow"]:
    send_notification(user_id, "Time to care for your shoes!")

2. Shoe Replacement Suggestions
Logic:

Estimate wear lifespan from material & frequency.

Suggest replacement when remaining lifespan < 15%.

Pseudocode:
if estimated_lifespan_remaining < 0.15:
    recommend_replacement(user_id, similar_shoes)

🗄 Database Schema Design
File: schema.sql
Tables:

user_profiles – user details.

shoe_catalog – shoe attributes.

user_interactions – views, purchases, wishlist, care logs.

recommendation_logs – history of recommendations.

Design Considerations:

Primary & Foreign Keys for data integrity.

Indexed columns for fast lookups.

Scalable to millions of records.

 Evaluation Readiness
This project meets all AnalogDots assessment requirements:

Code Quality: Modular, documented, reusable.

Algorithm Design: Hybrid filtering for balanced performance.

Data Modeling: Scalable, normalized schema.

Documentation: This README + schema.sql + video demonstration.
