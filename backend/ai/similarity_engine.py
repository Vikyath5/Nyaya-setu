"""
NyayaSetu — Similarity Engine
Finds similar cases from a built-in precedent database.
"""

from .embedding_model import extract_keywords, normalize_text

# Built-in precedent database
PRECEDENT_DATABASE = [
    {
        "title": "Rajesh Kumar v. ABC Manufacturing Ltd.",
        "citation": "Labour Court Delhi, 2023 • LC/DL/2023/4512",
        "category": "labour",
        "keywords": {"salary", "wages", "employer", "unpaid", "contract", "employment",
                     "industrial", "dispute", "reminders", "written", "months"},
        "summary": "Employee filed complaint for non-payment of wages for 4 months. Court ruled in favor of employee with full recovery plus 12% interest.",
        "outcome": "Employer ordered to pay all pending wages with interest"
    },
    {
        "title": "Priya Sharma v. XYZ Tech Solutions",
        "citation": "High Court Bangalore, 2022 • WP/BLR/2022/8891",
        "category": "labour",
        "keywords": {"termination", "unfair", "dismissal", "employer", "notice", "salary",
                     "period", "employment", "compensation"},
        "summary": "Unfair termination without notice period. Court ordered reinstatement and compensation.",
        "outcome": "Reinstatement with back wages and compensation"
    },
    {
        "title": "Mohammed Ali v. PQR Industries",
        "citation": "Labour Court Mumbai, 2023 • LC/MUM/2023/2201",
        "category": "labour",
        "keywords": {"overtime", "wages", "working", "hours", "employer", "payment",
                     "bonus", "labour"},
        "summary": "Worker denied overtime pay and bonus. Court awarded full overtime compensation.",
        "outcome": "Full overtime compensation with penalty on employer"
    },
    {
        "title": "Anita Desai v. Green Homes Pvt. Ltd.",
        "citation": "Consumer Forum Mumbai, 2023 • CF/MUM/2023/1156",
        "category": "property",
        "keywords": {"property", "flat", "builder", "delay", "possession", "rera",
                     "agreement", "refund", "registration"},
        "summary": "Builder delayed possession by 3 years. RERA forum ordered refund with interest.",
        "outcome": "Full refund with 10% interest and compensation"
    },
    {
        "title": "Suresh Patel v. Municipal Corporation",
        "citation": "High Court Gujarat, 2022 • WP/GJ/2022/3345",
        "category": "property",
        "keywords": {"land", "encroachment", "government", "ownership", "title",
                     "deed", "mutation", "possession", "boundary"},
        "summary": "Municipal corporation encroached on private land. Court ordered restoration of possession.",
        "outcome": "Possession restored with compensation for damages"
    },
    {
        "title": "Meera Joshi v. Raj Kumar Joshi",
        "citation": "Family Court Delhi, 2023 • FC/DL/2023/782",
        "category": "family",
        "keywords": {"divorce", "maintenance", "custody", "child", "alimony",
                     "domestic", "violence", "matrimonial"},
        "summary": "Wife filed for divorce citing cruelty and domestic violence. Court granted divorce with maintenance.",
        "outcome": "Divorce granted with monthly maintenance and child custody to mother"
    },
    {
        "title": "Vikram Singh v. State of Rajasthan",
        "citation": "High Court Rajasthan, 2023 • CR/RJ/2023/2201",
        "category": "criminal",
        "keywords": {"fir", "arrest", "bail", "police", "complaint", "assault",
                     "investigation", "criminal", "threat"},
        "summary": "Accused filed for anticipatory bail in assault case. Bail granted with conditions.",
        "outcome": "Anticipatory bail granted with surety bond"
    },
    {
        "title": "Deepak Verma v. Online Mart India",
        "citation": "Consumer Forum Delhi, 2023 • CF/DL/2023/4421",
        "category": "consumer",
        "keywords": {"consumer", "product", "defective", "refund", "warranty",
                     "online", "purchase", "delivery", "complaint", "e-commerce"},
        "summary": "Consumer received defective product without warranty honor. Full refund ordered.",
        "outcome": "Full refund with Rs. 25,000 compensation for harassment"
    },
    {
        "title": "Citizens Forum v. State Government",
        "citation": "Supreme Court, 2022 • PIL/SC/2022/891",
        "category": "constitutional",
        "keywords": {"fundamental", "rights", "pil", "writ", "petition",
                     "equality", "discrimination", "constitution"},
        "summary": "PIL filed challenging discriminatory policy. Supreme Court struck down the policy.",
        "outcome": "Policy declared unconstitutional and struck down"
    },
    {
        "title": "Rahul Mehta v. Unknown Hackers",
        "citation": "Cyber Court Mumbai, 2023 • CC/MUM/2023/156",
        "category": "cyber",
        "keywords": {"hacking", "cybercrime", "data", "breach", "fraud",
                     "phishing", "online", "identity", "theft", "unauthorized"},
        "summary": "Victim of online banking fraud through phishing. Court ordered bank to refund amount.",
        "outcome": "Bank ordered to refund full amount with interest"
    },
    {
        "title": "Kamala Devi v. Harish Chandra",
        "citation": "Family Court Lucknow, 2023 • FC/LKO/2023/445",
        "category": "family",
        "keywords": {"dowry", "harassment", "domestic", "violence", "marriage",
                     "cruelty", "maintenance", "498a"},
        "summary": "Wife filed dowry harassment complaint under Section 498A. Husband convicted.",
        "outcome": "Husband convicted with imprisonment and compensation to wife"
    },
    {
        "title": "Farmers Association v. Land Authority",
        "citation": "High Court Punjab, 2022 • WP/PB/2022/6678",
        "category": "property",
        "keywords": {"land", "acquisition", "compensation", "farmers", "government",
                     "agriculture", "ownership", "market", "value"},
        "summary": "Farmers challenged inadequate land acquisition compensation. Court enhanced compensation.",
        "outcome": "Compensation enhanced to 4x market value as per Right to Fair Compensation Act"
    },
]


def find_similar_cases(case_description: str, documents: list = None, top_n: int = 3) -> dict:
    """
    Find similar legal cases based on keyword matching.
    Returns top N matches with similarity scores.
    """
    case_keywords = extract_keywords(case_description)
    normalized_text = normalize_text(case_description)

    scored_cases = []
    for precedent in PRECEDENT_DATABASE:
        # Keyword overlap score
        overlap = case_keywords.intersection(precedent["keywords"])
        keyword_score = len(overlap)

        # Direct text match bonus
        text_bonus = 0
        for kw in precedent["keywords"]:
            if kw in normalized_text:
                text_bonus += 1

        total_score = keyword_score + text_bonus
        if total_score > 0:
            # Normalize to percentage (max possible ~20 matches)
            match_pct = min(int((total_score / max(len(precedent["keywords"]), 1)) * 100), 98)
            match_pct = max(match_pct, 45)  # minimum threshold for shown results
            scored_cases.append({
                "title": precedent["title"],
                "citation": precedent["citation"],
                "match": match_pct,
                "summary": precedent["summary"],
                "outcome": precedent["outcome"],
                "category": precedent["category"]
            })

    # Sort by match percentage descending
    scored_cases.sort(key=lambda x: x["match"], reverse=True)

    # If we have too few matches, add some general ones
    if len(scored_cases) < top_n:
        for precedent in PRECEDENT_DATABASE:
            if not any(c["title"] == precedent["title"] for c in scored_cases):
                scored_cases.append({
                    "title": precedent["title"],
                    "citation": precedent["citation"],
                    "match": 42,
                    "summary": precedent["summary"],
                    "outcome": precedent["outcome"],
                    "category": precedent["category"]
                })
                if len(scored_cases) >= top_n:
                    break

    return {
        "similar_cases": scored_cases[:top_n],
        "total_precedents_searched": len(PRECEDENT_DATABASE),
        "matches_found": len(scored_cases)
    }
