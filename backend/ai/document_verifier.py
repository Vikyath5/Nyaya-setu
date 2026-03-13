import pdfplumber


class DocumentVerifier:

    def extract_text(self, file_path):
        """
        Extract text from a PDF document.
        """

        text = ""

        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text

        except Exception:
            return ""

        return text.lower()

    def verify_document(self, file_path, expected_type):

        text = self.extract_text(file_path)

        if not text:
            return {
                "detected_type": "unknown",
                "verification_status": "unable_to_read"
            }

        rules = {

            "employment contract": [
                "employment",
                "contract",
                "salary",
                "position"
            ],

            "salary slips": [
                "salary",
                "pay",
                "employee",
                "earnings"
            ],

            "bank statements": [
                "account number",
                "transaction",
                "balance",
                "statement"
            ],

            "property deed": [
                "property",
                "ownership",
                "deed",
                "registration"
            ],

            "land registration documents": [
                "land",
                "registration",
                "survey",
                "property"
            ],

            "identity proof": [
                "name",
                "date of birth",
                "id",
                "government"
            ],

            "purchase invoice": [
                "invoice",
                "purchase",
                "amount",
                "product"
            ],

            "warranty card": [
                "warranty",
                "product",
                "serial",
                "service"
            ],

            "product photos": [
                "image",
                "product",
                "photo"
            ],

            "rental agreement": [
                "rent",
                "tenant",
                "landlord",
                "agreement"
            ],

            "payment receipts": [
                "receipt",
                "payment",
                "amount",
                "paid"
            ],

            "transaction records": [
                "transaction",
                "transfer",
                "amount",
                "date"
            ],

            "marriage certificate": [
                "marriage",
                "spouse",
                "certificate",
                "registration"
            ],

            "financial records": [
                "income",
                "expense",
                "financial",
                "statement"
            ]
        }

        keywords = rules.get(expected_type.lower(), [])

        score = sum(keyword in text for keyword in keywords)

        if score >= 2:
            return {
                "detected_type": expected_type,
                "verification_status": "verified"
            }

        return {
            "detected_type": "unknown",
            "verification_status": "mismatch"
        }