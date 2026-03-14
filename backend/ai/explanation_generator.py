"""
NyayaSetu — Legal Explanation Generator
Generates plain-language legal explanation of the case analysis.
"""

from .embedding_model import detect_legal_category, normalize_text


# Explanation templates by category
EXPLANATIONS = {
    "labour": {
        "detected_type": "Labour/Employment Dispute",
        "section_ref": "Industrial Disputes Act, 1947 (Section 33C)",
        "summary_template": (
            "Your situation constitutes a {specific_issue} under the Industrial Disputes Act, 1947. "
            "{evidence_detail} This establishes a clear basis for legal proceedings under applicable labour laws."
        ),
        "key_provision": (
            "Section 33C of the Industrial Disputes Act allows workers to recover money due from "
            "an employer through the Labour Court. The Payment of Wages Act, 1936 further protects "
            "your right to timely wage payment."
        ),
        "applicable_relief": (
            "Recovery of unpaid dues with interest, potential compensation for mental harassment, "
            "and employer penalties under BNS guidelines. Pre-litigation mediation is also available."
        ),
        "specific_issues": {
            "salary": "non-payment of wages dispute",
            "termination": "wrongful termination dispute",
            "harassment": "workplace harassment complaint",
            "overtime": "unpaid overtime wages dispute",
            "bonus": "unpaid bonus dispute",
            "default": "employment dispute"
        }
    },
    "property": {
        "detected_type": "Property/Real Estate Dispute",
        "section_ref": "Transfer of Property Act, 1882",
        "summary_template": (
            "Your situation involves a {specific_issue} under the Transfer of Property Act and "
            "related property legislation. {evidence_detail} Legal remedies are available through civil courts."
        ),
        "key_provision": (
            "The Transfer of Property Act, 1882 governs all property transactions in India. "
            "RERA (Real Estate Regulation and Development Act, 2016) provides additional protection "
            "for homebuyers against builder defaults."
        ),
        "applicable_relief": (
            "Injunction orders, restoration of possession, compensation for damages, and in case "
            "of builder disputes, full refund with interest under RERA provisions."
        ),
        "specific_issues": {
            "property": "property ownership dispute",
            "land": "land title dispute",
            "tenant": "landlord-tenant dispute",
            "encroachment": "encroachment dispute",
            "builder": "builder delay/default dispute",
            "default": "property dispute"
        }
    },
    "criminal": {
        "detected_type": "Criminal Matter",
        "section_ref": "Bharatiya Nyaya Sanhita (BNS) 2023",
        "summary_template": (
            "Your situation involves a {specific_issue} under the Bharatiya Nyaya Sanhita (BNS). "
            "{evidence_detail} Legal proceedings can be initiated through the appropriate criminal court."
        ),
        "key_provision": (
            "The Bharatiya Nyaya Sanhita (BNS) replaces the Indian Penal Code and applies to all "
            "criminal offences. The Bharatiya Nagarik Suraksha Sanhita governs criminal procedure."
        ),
        "applicable_relief": (
            "Filing of FIR, police investigation, bail applications, and criminal prosecution. "
            "Victim compensation scheme is also available under BNS provisions."
        ),
        "specific_issues": {
            "assault": "criminal assault matter",
            "fraud": "criminal fraud/cheating matter",
            "theft": "theft/robbery matter",
            "threat": "criminal intimidation matter",
            "domestic": "domestic violence matter",
            "default": "criminal matter"
        }
    },
    "family": {
        "detected_type": "Family/Matrimonial Dispute",
        "section_ref": "Hindu Marriage Act, 1955 / Special Marriage Act, 1954",
        "summary_template": (
            "Your situation involves a {specific_issue} under applicable family law. "
            "{evidence_detail} Family courts provide specialized jurisdiction for such matters."
        ),
        "key_provision": (
            "The Hindu Marriage Act, 1955 and Family Courts Act, 1984 provide comprehensive "
            "framework for matrimonial disputes. Section 125 CrPC ensures right to maintenance."
        ),
        "applicable_relief": (
            "Divorce decree, maintenance/alimony orders, child custody arrangements, protection "
            "orders under Domestic Violence Act, and division of matrimonial property."
        ),
        "specific_issues": {
            "divorce": "divorce/separation matter",
            "custody": "child custody dispute",
            "maintenance": "maintenance/alimony dispute",
            "domestic": "domestic violence complaint",
            "dowry": "dowry harassment complaint",
            "default": "family/matrimonial dispute"
        }
    },
    "consumer": {
        "detected_type": "Consumer Complaint",
        "section_ref": "Consumer Protection Act, 2019",
        "summary_template": (
            "Your situation involves a {specific_issue} under the Consumer Protection Act, 2019. "
            "{evidence_detail} Consumer forums provide quick and affordable resolution."
        ),
        "key_provision": (
            "The Consumer Protection Act, 2019 protects buyers against defective goods, "
            "deficient services, unfair trade practices, and misleading advertisements."
        ),
        "applicable_relief": (
            "Replacement/refund of product, compensation for deficiency in service, punitive "
            "damages for unfair trade practices, and costs of litigation."
        ),
        "specific_issues": {
            "defective": "defective product complaint",
            "refund": "refund/replacement dispute",
            "service": "deficiency in service complaint",
            "online": "e-commerce/online purchase dispute",
            "insurance": "insurance claim dispute",
            "default": "consumer complaint"
        }
    },
    "constitutional": {
        "detected_type": "Constitutional/Fundamental Rights Matter",
        "section_ref": "Constitution of India, Part III",
        "summary_template": (
            "Your situation involves a {specific_issue} under the Constitution of India. "
            "{evidence_detail} Writ petitions can be filed in High Court or Supreme Court."
        ),
        "key_provision": (
            "Part III of the Constitution guarantees fundamental rights. Article 32 (Supreme Court) "
            "and Article 226 (High Court) provide remedies through writ petitions."
        ),
        "applicable_relief": (
            "Writ of mandamus, habeas corpus, certiorari, prohibition, or quo warranto as "
            "appropriate. Declaration of rights and constitutional remedies."
        ),
        "specific_issues": {
            "discrimination": "fundamental rights violation (discrimination)",
            "equality": "right to equality violation",
            "freedom": "freedom of speech/expression violation",
            "default": "constitutional rights matter"
        }
    },
    "cyber": {
        "detected_type": "Cybercrime/Digital Offence",
        "section_ref": "Information Technology Act, 2000",
        "summary_template": (
            "Your situation involves a {specific_issue} under the Information Technology Act, 2000. "
            "{evidence_detail} Cyber cells and specialized courts handle such matters."
        ),
        "key_provision": (
            "The IT Act, 2000 and its amendments address cybercrimes including hacking, data theft, "
            "online fraud, and identity theft. Section 66 provides for punishment of computer-related offences."
        ),
        "applicable_relief": (
            "Criminal prosecution under IT Act, compensation through adjudicating officer, "
            "and recovery of financial losses through civil suit."
        ),
        "specific_issues": {
            "hacking": "unauthorized computer access/hacking complaint",
            "fraud": "online/cyber fraud complaint",
            "data": "data breach/privacy violation complaint",
            "identity": "identity theft complaint",
            "default": "cybercrime complaint"
        }
    }
}

DEFAULT_EXPLANATION = {
    "detected_type": "Legal Matter",
    "section_ref": "Applicable Indian Law",
    "summary_template": (
        "Your situation involves a legal matter that requires professional analysis. "
        "{evidence_detail} Please consult a qualified advocate for specific legal advice."
    ),
    "key_provision": "Multiple legal provisions may be applicable based on the specifics of your case.",
    "applicable_relief": "Legal remedies will depend on the specific nature and jurisdiction of the case.",
    "specific_issues": {"default": "legal matter"}
}


def generate_explanation(case_description: str) -> dict:
    """
    Generate a plain-language legal explanation of the case.
    Returns detected type, summary, key provisions, and applicable relief.
    """
    category_info = detect_legal_category(case_description)
    category = category_info["primary_category"]
    normalized = normalize_text(case_description)

    template = EXPLANATIONS.get(category, DEFAULT_EXPLANATION)

    # Determine specific issue
    specific_issue = template["specific_issues"].get("default", "legal matter")
    for keyword, issue in template["specific_issues"].items():
        if keyword != "default" and keyword in normalized:
            specific_issue = issue
            break

    # Build evidence detail
    evidence_parts = []
    if any(w in normalized for w in ["written", "email", "letter", "documented"]):
        evidence_parts.append("The written communication records provide strong evidentiary support.")
    if any(w in normalized for w in ["contract", "agreement"]):
        evidence_parts.append("The existence of a formal agreement strengthens your position.")
    if any(w in normalized for w in ["witness", "witnesses"]):
        evidence_parts.append("Witness testimony further supports your claims.")
    if "months" in normalized or "years" in normalized:
        evidence_parts.append("The duration of the issue establishes a clear pattern.")

    evidence_detail = " ".join(evidence_parts) if evidence_parts else (
        "Gathering documentary evidence will strengthen your case."
    )

    summary = template["summary_template"].format(
        specific_issue=specific_issue,
        evidence_detail=evidence_detail
    )

    return {
        "detected_type": template["detected_type"],
        "section_ref": template["section_ref"],
        "summary": summary,
        "key_provision": template["key_provision"],
        "applicable_relief": template["applicable_relief"],
        "legal_points": [
            {
                "title": "Key Legal Provision",
                "content": template["key_provision"],
                "color": "var(--semantic-positive)"
            },
            {
                "title": "Applicable Relief",
                "content": template["applicable_relief"],
                "color": "var(--accent-primary)"
            }
        ],
        "category": category,
        "matched_keywords": category_info["matched_keywords"]
    }
