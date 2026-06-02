# packages/language-science/src/language_science/confusion_map.py

from __future__ import annotations

from typing import Any

# Entry: (term_a, term_b, topic, explanation, detection_strategy)
EXPLICIT_CFA_CONFUSIONS: list[tuple[str, str, str, str, str]] = [
    # Fixed Income -- Duration
    ("Macaulay duration", "Modified duration", "Fixed Income",
     "Macaulay = weighted avg time to CF; Modified = Macaulay / (1 + YTM/n)",
     "explicit"),
    ("Modified duration", "Effective duration", "Fixed Income",
     "Modified assumes flat yield curve; Effective allows embedded options",
     "explicit"),
    ("Modified duration", "Money duration", "Fixed Income",
     "Modified = % price change; Money = dollar price change per 100bp",
     "explicit"),
    ("Key rate duration", "Effective duration", "Fixed Income",
     "Key rate = sensitivity to one maturity point; Effective = parallel shift",
     "explicit"),

    # Fixed Income -- Yield
    ("Yield to maturity", "Current yield", "Fixed Income",
     "YTM = total return if held to maturity; Current = annual coupon / price",
     "explicit"),
    ("Yield to maturity", "Yield to call", "Fixed Income",
     "YTM assumes held to maturity; YTC assumes called at first call date",
     "explicit"),
    ("Yield to maturity", "Bond equivalent yield", "Fixed Income",
     "YTM is annual; BEY doubles semi-annual YTM for comparison",
     "explicit"),
    ("Current yield", "Holding period return", "Fixed Income",
     "Current = coupon/price; HPR = total return over holding period",
     "explicit"),

    # Fixed Income -- Spreads
    ("G-spread", "Z-spread", "Fixed Income",
     "G = YTM diff vs govt bond; Z = constant spread to spot curve",
     "explicit"),
    ("Z-spread", "OAS", "Fixed Income",
     "Z assumes constant spread; OAS adjusts for embedded options",
     "explicit"),

    # Quant -- Statistics
    ("Type I error", "Type II error", "Quantitative Methods",
     "Type I = false positive (reject true null); Type II = false negative (fail to reject false null)",
     "explicit"),
    ("Arithmetic mean", "Geometric mean", "Quantitative Methods",
     "Arith = simple avg; Geo = compounded return, always <= arith",
     "explicit"),
    ("Arithmetic mean", "Harmonic mean", "Quantitative Methods",
     "Arith = sum/n; Harmonic = n / sum(1/x), used for averaging ratios",
     "explicit"),
    ("Money-weighted return", "Time-weighted return", "Quantitative Methods",
     "MWR = IRR of cash flows; TWR = geometric mean of sub-period returns",
     "explicit"),
    ("Confidence interval", "Prediction interval", "Quantitative Methods",
     "CI = range for parameter estimate; PI = wider range for individual prediction",
     "explicit"),

    # Corporate Issuers -- Capital
    ("NPV", "IRR", "Corporate Issuers",
     "NPV = absolute $ value; IRR = discount rate where NPV=0; conflict on mutually exclusive",
     "explicit"),
    ("Cost of debt", "Cost of equity", "Corporate Issuers",
     "Debt = after-tax (Rd*(1-t)); Equity = no tax shield, higher risk",
     "explicit"),
    ("WACC", "Cost of equity", "Corporate Issuers",
     "WACC = blended cost of all capital; Cost of equity = required return on equity only",
     "explicit"),

    # Equity
    ("DDM", "FCFE model", "Equity",
     "DDM values equity via dividends; FCFE values via free cash flow to equity",
     "explicit"),
    ("P/E ratio", "EV/EBITDA", "Equity",
     "P/E = price/earnings per share; EV/EBITDA = enterprise value / EBITDA",
     "explicit"),
    ("Market order", "Limit order", "Equity",
     "Market = execute at best available; Limit = execute at specified price or better",
     "explicit"),

    # FSA
    ("LIFO", "FIFO", "Financial Statement Analysis",
     "LIFO = last-in-first-out inventory; FIFO = first-in-first-out; opposite during inflation",
     "explicit"),
    ("Direct method", "Indirect method", "Financial Statement Analysis",
     "Direct = actual cash flows; Indirect = net income adjusted for non-cash items",
     "explicit"),
    ("Operating lease", "Finance lease", "Financial Statement Analysis",
     "Operating = off-balance sheet (pre-IFRS 16); Finance = on-balance sheet",
     "explicit"),
    ("DTA", "DTL", "Financial Statement Analysis",
     "DTA = future tax benefit (tax payable > tax expense); DTL = future tax obligation",
     "explicit"),

    # Portfolio
    ("Sharpe ratio", "Treynor ratio", "Portfolio Management",
     "Sharpe = excess return / total risk (sigma); Treynor = excess return / systematic risk (beta)",
     "explicit"),
    ("Sharpe ratio", "Sortino ratio", "Portfolio Management",
     "Sharpe uses sigma (total risk); Sortino uses downside deviation only",
     "explicit"),
    ("Systematic risk", "Unsystematic risk", "Portfolio Management",
     "Systematic = market-wide, non-diversifiable; Unsystematic = firm-specific, diversifiable",
     "explicit"),
    ("CML", "SML", "Portfolio Management",
     "CML = efficient frontier + risk-free rate (total risk x-axis); SML = CAPM (beta x-axis)",
     "explicit"),

    # Derivatives
    ("Forward contract", "Futures contract", "Derivatives",
     "Forward = OTC, customized, counterparty risk; Futures = exchange-traded, standardized, margined",
     "explicit"),
    ("Call option", "Put option", "Derivatives",
     "Call = right to buy; Put = right to sell",
     "explicit"),
    ("American option", "European option", "Derivatives",
     "American = exercise anytime before expiry; European = exercise only at expiry",
     "explicit"),

    # Economics
    ("Fiscal policy", "Monetary policy", "Economics",
     "Fiscal = government spending/taxation; Monetary = central bank money supply/rates",
     "explicit"),
    ("Absolute advantage", "Comparative advantage", "Economics",
     "Absolute = produce more with same inputs; Comparative = lower opportunity cost",
     "explicit"),
    ("GDP deflator", "CPI", "Economics",
     "GDP deflator = all domestic goods; CPI = fixed basket of consumer goods",
     "explicit"),
]

# Language-specific confusions
LANGUAGE_CONFUSIONS: list[tuple[str, str, str, str, str]] = [
    # English grammar
    ("its", "it's", "grammar", "Its = possessive; It's = it is", "explicit"),
    ("there", "their", "grammar", "There = place; Their = possessive; They're = they are", "explicit"),
    ("there", "they're", "grammar", "There = place; Their = possessive; They're = they are", "explicit"),
    ("affect", "effect", "vocabulary", "Affect = verb (to influence); Effect = noun (result)", "explicit"),
    ("principal", "principle", "vocabulary", "Principal = main/head/sum of money; Principle = fundamental truth", "explicit"),
    ("complement", "compliment", "vocabulary", "Complement = goes well with; Compliment = praise", "explicit"),
    ("stationary", "stationery", "vocabulary", "Stationary = not moving; Stationery = writing materials", "explicit"),
    ("accept", "except", "vocabulary", "Accept = receive; Except = excluding", "explicit"),
    ("than", "then", "grammar", "Than = comparison; Then = next in time", "explicit"),
    ("who", "whom", "grammar", "Who = subject; Whom = object", "explicit"),
    ("less", "fewer", "grammar", "Less = uncountable; Fewer = countable", "explicit"),

    # Finance English -- from CFA context
    ("yield (bond)", "yield (stock)", "finance",
     "Bond yield = coupon/price or YTM; Stock yield = dividend/price", "explicit"),
    ("duration (bond)", "duration (time)", "finance",
     "Duration = price sensitivity to rates vs length of time", "explicit"),
    ("premium (bond)", "premium (option)", "finance",
     "Bond premium = price > par; Option premium = price of the contract", "explicit"),
    ("spread (credit)", "spread (bid-ask)", "finance",
     "Credit spread = yield diff vs risk-free; Bid-ask spread = trading cost", "explicit"),
]


def build_confusion_map() -> dict[str, dict[str, Any]]:
    """Build a lookup dict: pair_id -> confusable pair data."""
    pairs: dict[str, dict[str, Any]] = {}
    for term_a, term_b, topic, explanation, strategy in EXPLICIT_CFA_CONFUSIONS:
        pair_id = f"cfaconf-{term_a.lower().replace(' ', '-')}-vs-{term_b.lower().replace(' ', '-')}"
        pair_data = {
            "pair_id": pair_id,
            "term_a": term_a,
            "term_b": term_b,
            "topic": topic,
            "explanation": explanation,
            "detection_strategy": strategy,
            "domain": "cfa",
        }
        pairs[pair_id] = pair_data
    for term_a, term_b, topic, explanation, strategy in LANGUAGE_CONFUSIONS:
        pair_id = f"langconf-{term_a.lower().replace(' ', '-')}-vs-{term_b.lower().replace(' ', '-')}"
        pair_data = {
            "pair_id": pair_id,
            "term_a": term_a,
            "term_b": term_b,
            "topic": topic,
            "explanation": explanation,
            "detection_strategy": strategy,
            "domain": "language",
        }
        pairs[pair_id] = pair_data
    return pairs


CONFUSION_MAP = build_confusion_map()


def lookup_confusions(term: str, domain: str | None = None) -> list[dict[str, Any]]:
    """Find all confusable pairs for a given term."""
    normalized = term.lower().strip()
    results = []
    for pair in CONFUSION_MAP.values():
        if domain and pair.get("domain") != domain:
            continue
        if normalized in (pair["term_a"].lower(), pair["term_b"].lower()):
            results.append(pair)
    return results
