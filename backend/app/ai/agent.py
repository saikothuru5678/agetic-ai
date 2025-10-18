# # backend/app/ai/agent.py
# from transformers import pipeline

# # Load a pre-trained sentiment analysis model
# sentiment_model = pipeline("sentiment-analysis")

# def analyze_feedback(text: str) -> dict:
#     """
#     Analyze feedback and return sentiment, category, and department.
#     For now, category and department are simple placeholders.
#     """
#     result = sentiment_model(text)[0]  # e.g. {'label': 'POSITIVE', 'score': 0.99}
#     label = result['label'].lower()

#     if label == "negative":
#         sentiment = "negative"
#     elif label == "positive":
#         sentiment = "positive"
#     else:
#         sentiment = "neutral"

#     # For now, set dummy values. Later you can replace with ML/NLP models.
#     category = "general"
#     department = "support"

#     return {
#         "sentiment": sentiment,
#         "category": category,
#         "department": department,
#     }


# backend/app/ai/agent.py
from transformers import pipeline

# Load a pre-trained sentiment analysis model
sentiment_model = pipeline("sentiment-analysis")

# Simple keyword maps
DEPARTMENT_KEYWORDS = {
    "library": "Library",
    "book": "Library",
    "exam": "Examination Cell",
    "admission": "Admissions",
    "fee": "Finance",
    "payment": "Finance",
    "canteen": "Canteen",
    "food": "Canteen",
    "hostel": "Hostel",
    "room": "Hostel",
    "class": "Academics",
    "teacher": "Academics",
    "professor": "Academics",
    "lab": "Laboratories",
    "sports": "Sports",
    "game": "Sports",
    "placement": "Placement Cell",
    "job": "Placement Cell",
}

CATEGORY_KEYWORDS = {
    "infrastructure": ["hostel", "room", "lab", "building", "wifi"],
    "academics": ["teacher", "class", "exam", "professor", "syllabus"],
    "administration": ["admission", "fee", "payment", "rules", "documents"],
    "facilities": ["canteen", "library", "food", "transport", "bus"],
    "extracurricular": ["sports", "game", "fest", "cultural", "event"],
}

def detect_department(text: str) -> str:
    text_lower = text.lower()
    for keyword, dept in DEPARTMENT_KEYWORDS.items():
        if keyword in text_lower:
            return dept
    return "General"

def detect_category(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in text_lower for word in keywords):
            return category.capitalize()
    return "General"

def analyze_feedback(text: str) -> dict:
    """
    Analyze feedback and return sentiment, category, and department.
    """
    # Sentiment
    result = sentiment_model(text)[0]  # e.g. {'label': 'POSITIVE', 'score': 0.99}
    label = result['label'].lower()

    if label == "negative":
        sentiment = "negative"
    elif label == "positive":
        sentiment = "positive"
    else:
        sentiment = "neutral"

    # Department & Category
    department = detect_department(text)
    category = detect_category(text)

    return {
        "sentiment": sentiment,
        "category": category,
        "department": department,
    }
