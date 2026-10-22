class LevenshteinTypoEngine:
    """
    Lexical Look-Alike & Typo-Squatting Detection Engine (UPI Semantics)
    Evaluates target Virtual Payment Addresses (VPAs) against brand whitelist tokens.
    """
    DEFAULT_BRAND_WHITELIST = [
        "paytm", "gpay", "phonepe", "amazonpay", "bharatpe", 
        "sbi", "hdfcbank", "icici", "axisbank", "cred",
        "electricity", "elect-bill", "tatapower", "bses", "billdesk"
    ]

    SUSPICIOUS_AFFIXES = [
        "support", "care", "refund", "kyc", "help", "desk", 
        "officer", "service", "tollfree", "bill", "pay", "dept", "portal"
    ]

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """
        Computes standard Levenshtein edit distance between two strings s1 and s2.
        """
        if len(s1) < len(s2):
            return LevenshteinTypoEngine.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    @staticmethod
    def similarity_ratio(s1: str, s2: str) -> float:
        """
        Normalized Levenshtein ratio: (|s1| + |s2| - dist) / (|s1| + |s2|)
        """
        s1, s2 = s1.lower(), s2.lower()
        total_len = len(s1) + len(s2)
        if total_len == 0:
            return 1.0
        dist = LevenshteinTypoEngine.levenshtein_distance(s1, s2)
        return (total_len - dist) / total_len

    @classmethod
    def evaluate_vpa(cls, vpa_handle: str, whitelist=None) -> dict:
        """
        Evaluates a target VPA (e.g. 'ph0nepe@okaxis', 'paytm-support@sbi') against brand whitelist.
        Returns highest similarity match score and typo-squatting flag.
        """
        if whitelist is None:
            whitelist = cls.DEFAULT_BRAND_WHITELIST

        # Extract handle prefix before @
        prefix = vpa_handle.split('@')[0].lower() if '@' in vpa_handle else vpa_handle.lower()
        
        # If exact match in whitelist, similarity is 1.0 (legitimate)
        if prefix in whitelist:
            return {
                "prefix": prefix,
                "best_match": prefix,
                "max_similarity": 1.0,
                "min_distance": 0,
                "is_typo_squatting": False
            }

        max_sim = 0.0
        best_match = None
        min_dist = 999

        # 1. Whole string Levenshtein comparison
        for brand in whitelist:
            dist = cls.levenshtein_distance(prefix, brand)
            sim = cls.similarity_ratio(prefix, brand)
            if sim > max_sim:
                max_sim = sim
                best_match = brand
                min_dist = dist

        # 2. Tokenized & Affix spoofing detection (e.g. paytm-support, elect-bill-pay)
        affix_match = False
        for brand in whitelist:
            if brand in prefix and prefix != brand:
                if any(affix in prefix for affix in cls.SUSPICIOUS_AFFIXES) or '-' in prefix or '_' in prefix:
                    affix_match = True
                    max_sim = max(max_sim, 0.89)
                    best_match = brand
                    min_dist = min(min_dist, 1)
                    break

        # Also check utility/electricity keyword spoofing
        if not affix_match and any(w in prefix for w in ["elect", "bijli", "bill-pay", "power"]):
            affix_match = True
            max_sim = max(max_sim, 0.85)
            best_match = "electricity-board"
            min_dist = 1

        # Scores exceeding 0.75 on unregistered handles indicate impersonation
        is_typo = (max_sim >= 0.75 or affix_match) and prefix not in whitelist

        return {
            "prefix": prefix,
            "best_match": best_match,
            "max_similarity": round(max_sim, 4),
            "min_distance": min_dist,
            "is_typo_squatting": is_typo
        }
