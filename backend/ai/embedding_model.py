"""
NyayaSetu — Text Preprocessing & Keyword Extraction Utilities
Used by all AI modules for text analysis.
"""

import re
from typing import List, Dict, Set

# Legal domain keyword categories
LEGAL_CATEGORIES = {
    "labour": {
        "keywords": ["salary", "wages", "employer", "employee", "termination", "fired",
                     "dismissed", "retrenchment", "bonus", "overtime", "working hours",
                     "workplace", "harassment", "discrimination", "unfair dismissal",
                     "employment contract", "notice period", "gratuity", "provident fund",
                     "labour court", "industrial dispute", "workmen", "layoff"],
        "acts": ["Industrial Disputes Act", "Payment of Wages Act", "Minimum Wages Act",
                 "Payment of Bonus Act", "Payment of Gratuity Act", "Employees Provident Fund Act"],
        "sections": ["Section 33C", "Section 25F", "Section 25G", "Section 2(s)"]
    },
    "property": {
        "keywords": ["property", "land", "house", "flat", "apartment", "tenant", "landlord",
                     "rent", "lease", "eviction", "encroachment", "title", "deed", "mutation",
                     "possession", "trespassing", "boundary", "mortgage", "sale deed",
                     "registration", "ownership", "inheritance", "partition"],
        "acts": ["Transfer of Property Act", "Registration Act", "Indian Stamp Act",
                 "Land Acquisition Act", "Rent Control Act", "RERA"],
        "sections": ["Section 54", "Section 106", "Section 111"]
    },
    "criminal": {
        "keywords": ["fir", "police", "arrest", "bail", "theft", "robbery", "assault",
                     "murder", "fraud", "cheating", "criminal", "complaint", "investigation",
                     "charge sheet", "cognizable", "non-cognizable", "bailable", "warrant",
                     "domestic violence", "dowry", "cybercrime", "threat", "extortion"],
        "acts": ["Bharatiya Nyaya Sanhita (BNS)", "Code of Criminal Procedure",
                 "Bharatiya Nagarik Suraksha Sanhita", "Bharatiya Sakshya Adhiniyam",
                 "Protection of Women from Domestic Violence Act"],
        "sections": ["Section 302", "Section 376", "Section 420", "Section 498A"]
    },
    "family": {
        "keywords": ["divorce", "marriage", "custody", "child", "alimony", "maintenance",
                     "domestic violence", "dowry", "matrimonial", "guardianship", "adoption",
                     "separation", "annulment", "conjugal rights", "mutual consent"],
        "acts": ["Hindu Marriage Act", "Special Marriage Act", "Hindu Succession Act",
                 "Muslim Personal Law", "Family Courts Act", "Guardians and Wards Act",
                 "Protection of Women from Domestic Violence Act"],
        "sections": ["Section 13", "Section 125 CrPC", "Section 24"]
    },
    "consumer": {
        "keywords": ["consumer", "product", "defective", "deficiency", "service", "refund",
                     "warranty", "complaint", "unfair trade", "misleading", "advertisement",
                     "e-commerce", "online purchase", "delivery", "insurance claim"],
        "acts": ["Consumer Protection Act 2019", "E-Commerce Rules",
                 "Insurance Regulatory and Development Authority Act"],
        "sections": ["Section 2(7)", "Section 35", "Section 38"]
    },
    "constitutional": {
        "keywords": ["fundamental rights", "right to equality", "freedom of speech",
                     "right to life", "discrimination", "reservation", "public interest",
                     "PIL", "writ petition", "habeas corpus", "mandamus", "certiorari"],
        "acts": ["Constitution of India"],
        "sections": ["Article 14", "Article 19", "Article 21", "Article 32", "Article 226"]
    },
    "cyber": {
        "keywords": ["cyberbullying", "hacking", "data breach", "phishing", "online fraud",
                     "identity theft", "social media", "defamation online", "cyber stalking",
                     "ransomware", "unauthorized access", "data privacy"],
        "acts": ["Information Technology Act 2000", "IT Amendment Act 2008",
                 "Personal Data Protection Bill"],
        "sections": ["Section 43", "Section 66", "Section 66C", "Section 67"]
    }
}

# Evidence strength indicators
EVIDENCE_INDICATORS = {
    "strong": ["written", "documented", "contract", "agreement", "email", "letter",
               "receipt", "proof", "witness", "recorded", "signed", "notarized",
               "registered", "certified", "photograph", "video", "cctv", "bank statement"],
    "moderate": ["verbal", "mentioned", "told", "said", "heard", "informed", "noticed",
                 "remember", "recall", "approximate", "around", "about"],
    "weak": ["think", "maybe", "possibly", "not sure", "uncertain", "might", "guess",
             "assume", "believe"]
}

# Time-related patterns
TIME_PATTERNS = {
    "days": r"(\d+)\s*days?",
    "weeks": r"(\d+)\s*weeks?",
    "months": r"(\d+)\s*months?",
    "years": r"(\d+)\s*years?",
}


def normalize_text(text: str) -> str:
    """Normalize text for analysis: lowercase, remove extra whitespace."""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def extract_keywords(text: str) -> Set[str]:
    """Extract meaningful words from text (remove stopwords)."""
    stopwords = {
        "i", "me", "my", "myself", "we", "our", "ours", "you", "your", "he",
        "him", "his", "she", "her", "it", "its", "they", "them", "their",
        "what", "which", "who", "whom", "this", "that", "these", "those",
        "am", "is", "are", "was", "were", "be", "been", "being", "have",
        "has", "had", "having", "do", "does", "did", "doing", "a", "an",
        "the", "and", "but", "if", "or", "because", "as", "until", "while",
        "of", "at", "by", "for", "with", "about", "against", "between",
        "through", "during", "before", "after", "to", "from", "up", "down",
        "in", "out", "on", "off", "over", "under", "again", "further",
        "then", "once", "here", "there", "when", "where", "why", "how",
        "all", "both", "each", "few", "more", "most", "other", "some",
        "such", "no", "nor", "not", "only", "own", "same", "so", "than",
        "too", "very", "can", "will", "just", "should", "now"
    }
    words = re.findall(r'\b[a-z]+\b', normalize_text(text))
    return set(w for w in words if w not in stopwords and len(w) > 2)


def detect_legal_category(text: str) -> Dict:
    """Detect the primary legal category of a case description."""
    normalized = normalize_text(text)
    scores = {}

    for category, data in LEGAL_CATEGORIES.items():
        score = 0
        matched_keywords = []
        for keyword in data["keywords"]:
            if keyword.lower() in normalized:
                score += 1
                matched_keywords.append(keyword)
        scores[category] = {
            "score": score,
            "matched_keywords": matched_keywords,
            "acts": data["acts"],
            "sections": data["sections"]
        }

    # Sort by score descending
    sorted_categories = sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True)
    primary = sorted_categories[0] if sorted_categories else ("general", {"score": 0})

    return {
        "primary_category": primary[0],
        "primary_score": primary[1]["score"],
        "matched_keywords": primary[1].get("matched_keywords", []),
        "applicable_acts": primary[1].get("acts", []),
        "applicable_sections": primary[1].get("sections", []),
        "all_scores": {k: v["score"] for k, v in scores.items()}
    }


def assess_evidence_strength(text: str) -> Dict:
    """Assess the strength of evidence mentioned in the case description."""
    normalized = normalize_text(text)
    strong_count = sum(1 for word in EVIDENCE_INDICATORS["strong"] if word in normalized)
    moderate_count = sum(1 for word in EVIDENCE_INDICATORS["moderate"] if word in normalized)
    weak_count = sum(1 for word in EVIDENCE_INDICATORS["weak"] if word in normalized)

    total = strong_count + moderate_count + weak_count
    if total == 0:
        return {"strength": "unknown", "score": 50, "details": "No clear evidence indicators found"}

    weighted = (strong_count * 3 + moderate_count * 2 + weak_count * 1)
    max_weighted = total * 3
    score = int((weighted / max_weighted) * 100)

    if score >= 70:
        strength = "strong"
    elif score >= 45:
        strength = "moderate"
    else:
        strength = "weak"

    return {
        "strength": strength,
        "score": score,
        "strong_indicators": strong_count,
        "moderate_indicators": moderate_count,
        "weak_indicators": weak_count
    }


def extract_time_duration(text: str) -> Dict:
    """Extract time durations mentioned in the text."""
    normalized = normalize_text(text)
    durations = {}
    for unit, pattern in TIME_PATTERNS.items():
        matches = re.findall(pattern, normalized)
        if matches:
            durations[unit] = [int(m) for m in matches]
    return durations
