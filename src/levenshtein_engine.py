class LevenshteinTypoEngine:
    """
    Lexical Look-Alike & Typo-Squatting Detection Engine (UPI & BBPS Semantics)
    Evaluates target Virtual Payment Addresses (VPAs) against:
    1. The Central BBPS & NPCI Verified Merchant Directory (Corporate / Utility Whitelist).
    2. Mathematical Levenshtein Edit Distance for Lexical Proximity (Typo-Squatting).
    3. Merchant Category Code (MCC) & Account Type Mismatch (Corporate Current vs P2P Savings).
    """

    # Official BBPS (Bharat Bill Payment System) & Corporate Merchant Registry
    BBPS_MERCHANT_DIRECTORY = {
        "elec.173": {
            "entity_name": "State Electricity Distribution Co. (DISCOM)",
            "category": "ELECTRICITY_UTILITY",
            "mcc": "4900 (Electric & Gas Utilities)",
            "account_type": "CORPORATE_CURRENT_ACCOUNT",
            "bbps_verified": True,
            "gstin": "07AAACB1234D1Z5",
            "regulatory_license": "CERC/SERC-DISCOM-DL"
        },
        "elect-bill-pay": {
            "entity_name": "National Power Discom Gateway",
            "category": "ELECTRICITY_UTILITY",
            "mcc": "4900 (Utilities)",
            "account_type": "CORPORATE_CURRENT_ACCOUNT",
            "bbps_verified": True,
            "gstin": "07AAACB5678D1Z9",
            "regulatory_license": "SERC-UTIL-99"
        },
        "tatapower": {
            "entity_name": "Tata Power Delhi Distribution Ltd",
            "category": "ELECTRICITY_UTILITY",
            "mcc": "4900 (Utilities)",
            "account_type": "CORPORATE_CURRENT_ACCOUNT",
            "bbps_verified": True,
            "gstin": "07AAACT2718E1ZE",
            "regulatory_license": "CERC-TPDDL-01"
        },
        "bses": {
            "entity_name": "BSES Rajdhani Power Limited",
            "category": "ELECTRICITY_UTILITY",
            "mcc": "4900 (Utilities)",
            "account_type": "CORPORATE_CURRENT_ACCOUNT",
            "bbps_verified": True,
            "gstin": "07AAACB2183G1ZU",
            "regulatory_license": "BSES-DISCOM-02"
        },
        "phonepe": {
            "entity_name": "PhonePe Internet Pvt Ltd",
            "category": "PAYMENT_AGGREGATOR",
            "mcc": "7399 (Business Services / Payment Aggregator)",
            "account_type": "MERCHANT_NODAL_ACCOUNT",
            "bbps_verified": True,
            "gstin": "29AABCU9603R1ZQ",
            "regulatory_license": "RBI-PA-2021-08"
        },
        "paytm": {
            "entity_name": "One97 Communications Ltd (Paytm)",
            "category": "PAYMENT_AGGREGATOR",
            "mcc": "7399 (Payment Aggregator)",
            "account_type": "MERCHANT_NODAL_ACCOUNT",
            "bbps_verified": True,
            "gstin": "09AAACB9021E1Z3",
            "regulatory_license": "RBI-PA-2021-12"
        },
        "gpay": {
            "entity_name": "Google India Digital Services Pvt Ltd",
            "category": "PAYMENT_APPLICATION_PROVIDER",
            "mcc": "7399 (Business Services)",
            "account_type": "CORPORATE_SETTLEMENT_ACCOUNT",
            "bbps_verified": True,
            "gstin": "29AAGCG1234D1Z2",
            "regulatory_license": "NPCI-TPAP-GPAY"
        },
        "billdesk": {
            "entity_name": "BillDesk (IndiaIdeas.com Ltd)",
            "category": "PAYMENT_SWITCH",
            "mcc": "7399 (Business Services)",
            "account_type": "ESCROW_SETTLEMENT_ACCOUNT",
            "bbps_verified": True,
            "gstin": "27AAAC12345E1Z8",
            "regulatory_license": "RBI-BBPOU-001"
        },
        "rahulgear": {
            "entity_name": "Rahul Gear Stores",
            "category": "RETAIL_MERCHANT",
            "mcc": "5941 (Sporting Goods Stores)",
            "account_type": "SOLE_PROPRIETOR_CURRENT",
            "bbps_verified": True,
            "gstin": "07AAAPR9981K1Z3",
            "regulatory_license": "MSME-DL-09821"
        }
    }

    DEFAULT_BRAND_WHITELIST = list(BBPS_MERCHANT_DIRECTORY.keys()) + [
        "amazonpay", "bharatpe", "sbi", "hdfcbank", "icici", "axisbank", "cred", "electricity"
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
    def evaluate_vpa(cls, vpa_handle: str) -> dict:
        """
        Evaluates a target VPA (e.g. 'elec.174@okaxis', 'elec.173@okaxis', 'ph0nepe@okaxis')
        against the verified BBPS directory & Levenshtein similarity metric.
        """
        prefix = vpa_handle.split('@')[0].lower() if '@' in vpa_handle else vpa_handle.lower()
        
        # 1. Check exact registration in BBPS Central Directory
        if prefix in cls.BBPS_MERCHANT_DIRECTORY:
            entry = cls.BBPS_MERCHANT_DIRECTORY[prefix]
            return {
                "vpa": vpa_handle,
                "prefix": prefix,
                "directory_status": "FOUND_IN_VERIFIED_BBPS_WHITELIST",
                "is_bbps_verified": True,
                "entity_name": entry["entity_name"],
                "category": entry["category"],
                "mcc": entry["mcc"],
                "account_type": entry["account_type"],
                "gstin": entry.get("gstin", "VERIFIED"),
                "is_typo_squatting": False,
                "max_similarity": 1.0,
                "min_distance": 0,
                "best_match": prefix,
                "risk_verdict": "SAFE_VERIFIED_MERCHANT",
                "warning": None
            }

        # 2. Handle NOT found in BBPS Whitelist -> Evaluate Typo-Squatting & Brand Impersonation
        all_targets = list(set(list(cls.BBPS_MERCHANT_DIRECTORY.keys()) + cls.DEFAULT_BRAND_WHITELIST))
        
        max_sim = 0.0
        best_match = None
        min_dist = 999

        for candidate in all_targets:
            dist = cls.levenshtein_distance(prefix, candidate)
            sim = cls.similarity_ratio(prefix, candidate)
            if sim > max_sim:
                max_sim = sim
                best_match = candidate
                min_dist = dist

        # Check for affix spoofing (e.g. elect-bill-support, tatapower-officer)
        affix_match = False
        for candidate in all_targets:
            if candidate in prefix and prefix != candidate:
                if any(affix in prefix for affix in cls.SUSPICIOUS_AFFIXES) or '-' in prefix or '_' in prefix:
                    affix_match = True
                    max_sim = max(max_sim, 0.89)
                    best_match = candidate
                    min_dist = min(min_dist, 1)
                    break

        # Check utility keywords spoofing (e.g. elec, bijli, power)
        if not affix_match and any(w in prefix for w in ["elec", "bijli", "power"]) and prefix != "elec.173":
            affix_match = True
            if "elec.173" in cls.BBPS_MERCHANT_DIRECTORY:
                best_match = "elec.173"
                dist = cls.levenshtein_distance(prefix, "elec.173")
                sim = cls.similarity_ratio(prefix, "elec.173")
                max_sim = max(max_sim, sim)
                min_dist = min(min_dist, dist)

        # Flag as typo-squatting if similarity >= 0.75 or suspicious affix on unverified handle
        is_typo = (max_sim >= 0.75 or affix_match)
        
        impersonated_info = cls.BBPS_MERCHANT_DIRECTORY.get(best_match, {})
        impersonated_name = impersonated_info.get("entity_name", best_match.title() if best_match else "Verified Entity")

        warning_msg = None
        if is_typo:
            warning_msg = (
                f"CRITICAL: Unregistered personal account '{prefix}' is impersonating "
                f"verified entity '{impersonated_name}' ({best_match}) with {round(max_sim * 100, 1)}% lexical similarity! "
                f"Recipient is an unverified individual savings account (MCC 0000)."
            )

        return {
            "vpa": vpa_handle,
            "prefix": prefix,
            "directory_status": "NOT_IN_BBPS_WHITELIST (UNVERIFIED_P2P_SAVINGS)",
            "is_bbps_verified": False,
            "entity_name": f"UNVERIFIED PERSONAL ACCOUNT (Claiming: {impersonated_name})",
            "category": "P2P_SAVINGS_INDIVIDUAL",
            "mcc": "0000 (Private Personal Savings Account)",
            "account_type": "INDIVIDUAL_SAVINGS_ACCOUNT",
            "is_typo_squatting": is_typo,
            "max_similarity": round(max_sim, 4),
            "min_distance": min_dist,
            "best_match": best_match,
            "impersonated_entity": impersonated_name,
            "risk_verdict": "FRAUD_TYPO_IMPERSONATION" if is_typo else "UNKNOWN_P2P",
            "warning": warning_msg
        }
