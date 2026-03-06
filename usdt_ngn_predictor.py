import streamlit as st
import requests
import json
import datetime
import random

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="USDT/NGN Oracle",
    page_icon="₦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=Syne:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080c14;
    --bg2: #0c1220;
    --bg3: #101828;
    --card: #111d2e;
    --border: #1a2942;
    --border2: #243550;
    --green: #05d68a;
    --green2: rgba(5,214,138,0.12);
    --red: #f0455a;
    --red2: rgba(240,69,90,0.12);
    --amber: #f5a623;
    --amber2: rgba(245,166,35,0.12);
    --blue: #4f8ef7;
    --blue2: rgba(79,142,247,0.12);
    --purple: #a78bfa;
    --text: #dce8f8;
    --muted: #4a6080;
    --muted2: #6b84a0;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background: var(--bg) !important; }

section[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}

.block-container { padding: 1.2rem 2rem 2rem 2rem !important; max-width: 1400px !important; }

h1,h2,h3 { font-family: 'IBM Plex Mono', monospace !important; }

/* ── TICKER BAR ── */
.ticker-wrap {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    padding: 10px 0;
    margin-bottom: 20px;
    white-space: nowrap;
}
.ticker-inner {
    display: inline-flex;
    gap: 48px;
    animation: ticker 30s linear infinite;
    padding: 0 24px;
}
@keyframes ticker { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }
.ticker-item {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--muted2);
}
.ticker-item .val { color: var(--text); font-weight: 600; }
.ticker-item .up { color: var(--green); }
.ticker-item .dn { color: var(--red); }

/* ── METRIC CARDS ── */
.mcard {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
}
.mcard::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 14px;
    pointer-events: none;
}
.mcard-green { border-top: 2px solid var(--green); }
.mcard-red   { border-top: 2px solid var(--red); }
.mcard-amber { border-top: 2px solid var(--amber); }
.mcard-blue  { border-top: 2px solid var(--blue); }
.mcard-purple{ border-top: 2px solid var(--purple); }

.mcard-label {
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
    font-family: 'IBM Plex Mono', monospace;
}
.mcard-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 26px;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 4px;
}
.mcard-sub {
    font-size: 12px;
    color: var(--muted2);
    margin-top: 4px;
}

/* ── ORACLE CARD ── */
.ocard {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 16px;
}
.ocard-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}

/* ── DIRECTION BADGE ── */
.dir-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 18px;
    border-radius: 100px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.dir-bull { background: var(--green2); color: var(--green); border: 1px solid rgba(5,214,138,0.3); }
.dir-bear { background: var(--red2);   color: var(--red);   border: 1px solid rgba(240,69,90,0.3); }
.dir-neu  { background: var(--amber2); color: var(--amber); border: 1px solid rgba(245,166,35,0.3); }

/* ── SIGNAL ROWS ── */
.sig-row {
    padding: 11px 0;
    border-bottom: 1px solid var(--border);
}
.sig-row:last-child { border-bottom: none; }
.sig-tags { display: flex; align-items: center; gap: 6px; margin-bottom: 5px; flex-wrap: wrap; }
.tag {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 100px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
}
.tag-bull   { background: var(--green2); color: var(--green); }
.tag-bear   { background: var(--red2);   color: var(--red); }
.tag-neu    { background: var(--amber2); color: var(--amber); }
.tag-hi     { background: var(--blue2);  color: var(--blue); }
.tag-med    { background: rgba(167,139,250,0.1); color: var(--purple); }
.tag-lo     { background: rgba(255,255,255,0.05); color: var(--muted2); }
.sig-name   { font-size: 14px; font-weight: 600; color: var(--text); }
.sig-detail { font-size: 12px; color: var(--muted2); line-height: 1.5; margin-top: 3px; }

/* ── PROGRESS BARS ── */
.prog-wrap { margin-bottom: 14px; }
.prog-label { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 5px; }
.prog-track { background: var(--border); border-radius: 4px; height: 6px; overflow: hidden; }
.prog-fill  { height: 100%; border-radius: 4px; }

/* ── SPREAD TABLE ── */
.spread-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.spread-table th {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    padding: 8px 12px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}
.spread-table td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
}
.spread-table tr:last-child td { border-bottom: none; }
.spread-table tr:hover td { background: rgba(255,255,255,0.02); }

/* ── CHAT ── */
.chat-u {
    background: var(--blue2);
    border: 1px solid rgba(79,142,247,0.2);
    border-radius: 14px 14px 3px 14px;
    padding: 12px 16px;
    margin: 10px 0;
    margin-left: 12%;
    font-size: 14px;
    line-height: 1.6;
}
.chat-a {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px 14px 14px 3px;
    padding: 12px 16px;
    margin: 10px 0;
    margin-right: 12%;
    font-size: 14px;
    line-height: 1.6;
}
.chat-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 5px;
}

/* ── ALERT BOX ── */
.alert-box {
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    margin-bottom: 10px;
    border-left: 3px solid;
    line-height: 1.5;
}
.alert-bull { background: var(--green2); border-color: var(--green); color: #a7f3d0; }
.alert-bear { background: var(--red2);   border-color: var(--red);   color: #fca5a5; }
.alert-info { background: var(--blue2);  border-color: var(--blue);  color: #bfdbfe; }
.alert-warn { background: var(--amber2); border-color: var(--amber); color: #fde68a; }

/* ── LIVE DOT ── */
.live-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--green);
    animation: blink 2s ease-in-out infinite;
    margin-right: 6px;
    vertical-align: middle;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

/* ── CONVERTER ── */
.conv-box {
    background: var(--bg2);
    border: 1px solid var(--border2);
    border-radius: 12px;
    padding: 18px;
}
.conv-result {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: var(--green);
    margin-top: 10px;
    text-align: center;
}

/* ── INPUTS ── */
.stTextInput>div>div>input, .stTextArea textarea, .stNumberInput>div>div>input {
    background: var(--card) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
}
.stTextInput>div>div>input:focus, .stTextArea textarea:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 2px rgba(79,142,247,0.15) !important;
}
.stButton>button {
    background: linear-gradient(135deg, #1a3a6e, #2d5fb8) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    transition: all 0.2s !important;
}
.stButton>button:hover { filter: brightness(1.15) !important; transform: translateY(-1px) !important; }
.stSelectbox>div>div { background: var(--card) !important; border-color: var(--border2) !important; color: var(--text) !important; }

#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init():
    for k, v in {
        "chat": [], "result": None, "last_time": None,
        "gemini_key": "", "news_key": "", "history": [],
        "alerts": [], "alert_triggered": []
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()


# ─────────────────────────────────────────────
# GEMINI CALL
# ─────────────────────────────────────────────
def gemini(prompt: str, key: str, system: str = "") -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
    parts = []
    if system:
        parts.append({"text": f"SYSTEM:\n{system}\n\n---\n\n"})
    parts.append({"text": prompt})
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"temperature": 0.25, "maxOutputTokens": 8192}
    }
    try:
        r = requests.post(url, json=payload, timeout=45)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.HTTPError as e:
        sc = r.status_code
        if sc == 403: return "❌ API key invalid or Gemini API not enabled."
        if sc == 429: return "❌ Rate limit hit. Wait 60 seconds and retry."
        if sc == 400: return f"❌ Bad request: {r.text[:200]}"
        return f"❌ HTTP {sc}: {e}"
    except Exception as e:
        return f"❌ Connection error: {e}"


# ─────────────────────────────────────────────
# FETCH BLACK MARKET + RATES
# ─────────────────────────────────────────────
def fetch_rates() -> dict:
    """Fetch official, P2P/crypto, and estimate black market rate."""
    result = {
        "official": None, "coingecko": None, "black_market": None,
        "source_official": "", "source_crypto": "",
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "partial"
    }

    # 1. CoinGecko — USDT/NGN (closest to P2P / black market)
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=ngn,usd",
            timeout=10, headers={"User-Agent": "Mozilla/5.0"}
        )
        if r.status_code == 200:
            d = r.json()
            ngn = d.get("tether", {}).get("ngn")
            if ngn and ngn > 0:
                result["coingecko"] = float(ngn)
                result["source_crypto"] = "CoinGecko (USDT/NGN)"
    except: pass

    # 2. Open Exchange Rates — official USD/NGN
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
        if r.status_code == 200:
            ngn = r.json().get("rates", {}).get("NGN")
            if ngn:
                result["official"] = float(ngn)
                result["source_official"] = "OpenExchangeRates (official USD/NGN)"
    except: pass

    # 3. Fallback official
    if not result["official"]:
        try:
            r = requests.get(
                "https://api.exchangerate-api.com/v4/latest/USD",
                timeout=10
            )
            if r.status_code == 200:
                ngn = r.json().get("rates", {}).get("NGN")
                if ngn:
                    result["official"] = float(ngn)
                    result["source_official"] = "ExchangeRateAPI"
        except: pass

    # 4. Derive black market estimate
    # Nigerian black market typically trades 5–20% above official
    # P2P crypto (CoinGecko) is the best proxy for street rate
    if result["coingecko"]:
        result["black_market"] = result["coingecko"]
        result["black_market_source"] = "CoinGecko USDT/NGN (P2P proxy)"
    elif result["official"]:
        # estimate black market as ~8% above official
        result["black_market"] = round(result["official"] * 1.08, 2)
        result["black_market_source"] = "Estimated (official ×1.08 premium)"

    # Use black market as primary rate
    primary = result["black_market"] or result["official"] or 1620.0
    result["primary"] = primary
    result["status"] = "live" if (result["coingecko"] or result["official"]) else "estimated"

    if result["official"] and result["black_market"]:
        result["spread_pct"] = round(
            ((result["black_market"] - result["official"]) / result["official"]) * 100, 2
        )
    else:
        result["spread_pct"] = None

    return result


# ─────────────────────────────────────────────
# FETCH GLOBAL SIGNALS
# ─────────────────────────────────────────────
def fetch_global_signals(news_key: str = "") -> list:
    """Comprehensive global signals that affect USDT/NGN."""
    signals = []

    # ── LIVE GLOBAL MACRO (free APIs) ──
    # BTC price (crypto sentiment proxy)
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true",
            timeout=10, headers={"User-Agent": "Mozilla/5.0"}
        )
        if r.status_code == 200:
            d = r.json()
            btc = d.get("bitcoin", {})
            eth = d.get("ethereum", {})
            btc_chg = btc.get("usd_24h_change", 0)
            signals.append({
                "category": "Crypto Market",
                "title": f"BTC ${btc.get('usd',0):,.0f} ({btc_chg:+.1f}% 24h) | ETH ${eth.get('usd',0):,.0f}",
                "detail": f"Crypto market sentiment: {'RISK-ON (bullish for NGN demand for USDT)' if btc_chg > 2 else 'RISK-OFF (bearish sentiment)' if btc_chg < -2 else 'NEUTRAL'}. BTC moves affect P2P crypto volume in Nigeria.",
                "impact": "BULLISH" if btc_chg > 2 else "BEARISH" if btc_chg < -2 else "NEUTRAL",
                "source": "CoinGecko Live"
            })
    except: pass

    # Oil price (Nigeria is oil-dependent, ~90% of forex earnings)
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=wrapped-bitcoin&vs_currencies=usd",
            timeout=8, headers={"User-Agent": "Mozilla/5.0"}
        )
    except: pass

    # DXY / USD strength proxy via EUR/USD
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
        if r.status_code == 200:
            rates = r.json().get("rates", {})
            eur = rates.get("EUR", 0)
            gbp = rates.get("GBP", 0)
            signals.append({
                "category": "USD Strength (DXY Proxy)",
                "title": f"EUR/USD: {eur:.4f} | GBP/USD: {gbp:.4f}",
                "detail": ("Strong USD puts pressure on NGN — harder for CBN to defend." if eur < 1.05 else "Weak USD gives NGN breathing room — reduces import pressure." if eur > 1.10 else "USD moderately strong — neutral effect on NGN."),
                "impact": "BEARISH" if eur < 1.05 else "BULLISH" if eur > 1.10 else "NEUTRAL",
                "source": "OpenExchangeRates Live"
            })
            # Emerging market risk gauge
            zar = rates.get("ZAR", 0)
            kes = rates.get("KES", 0)
            signals.append({
                "category": "EM Africa FX Context",
                "title": f"USD/ZAR: {zar:.2f} | USD/KES: {kes:.2f}",
                "detail": "South African Rand and Kenyan Shilling as African EM peers. Broad EM selloff tends to drag NGN down too. Tracks global risk appetite.",
                "impact": "NEUTRAL",
                "source": "OpenExchangeRates Live"
            })
    except: pass

    # ── LIVE NEWS via NewsAPI ──
    if news_key:
        topics = [
            ("Nigeria naira dollar exchange rate 2025", "Nigeria FX"),
            ("CBN central bank Nigeria forex intervention", "CBN Policy"),
            ("Nigeria inflation CPI economy", "Nigeria Macro"),
            ("crude oil price brent WTI today", "Oil Markets"),
            ("US Federal Reserve interest rates dollar", "Fed / USD"),
            ("USDT Tether stablecoin Nigeria crypto", "Crypto / USDT"),
            ("Nigeria remittance diaspora dollar", "Remittances"),
            ("IMF World Bank Nigeria economy", "International Finance"),
            ("Nigeria election politics economy", "Political Risk"),
            ("global risk sentiment emerging markets", "Global EM Risk"),
        ]
        for query, cat in topics[:6]:
            try:
                url = f"https://newsapi.org/v2/everything?q={requests.utils.quote(query)}&sortBy=publishedAt&pageSize=3&language=en&apiKey={news_key}"
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    for a in r.json().get("articles", []):
                        t = a.get("title", "")
                        d = a.get("description", "")
                        if t and d:
                            signals.append({
                                "category": cat,
                                "title": t[:120],
                                "detail": d[:200],
                                "published": a.get("publishedAt", "")[:10],
                                "source": a.get("source", {}).get("name", "News"),
                                "url": a.get("url", ""),
                                "impact": "UNKNOWN"
                            })
            except: pass

    # ── STRUCTURAL SIGNALS (always included) ──
    now = datetime.datetime.now()
    dow = now.weekday()  # 0=Mon
    hour = now.hour

    signals += [
        {
            "category": "Market Microstructure",
            "title": f"Session: {now.strftime('%A')} {hour:02d}:00 WAT",
            "detail": f"{'Business hours — high P2P volume, more price movement.' if 8<=hour<=17 and dow<5 else 'Evening session — moderate retail P2P activity.' if 18<=hour<=22 else 'Weekend — lower liquidity, wider spreads.' if dow>=5 else 'Off-hours — lower volume, price may drift.'}",
            "impact": "NEUTRAL",
            "source": "Market Structure"
        },
        {
            "category": "CBN Policy Framework",
            "title": "CBN Managed Float + FX Unification (2023–present)",
            "detail": "CBN unified official and I&E window rates in 2023. Periodic FX auctions to authorised dealers. Diaspora remittance policy eased. Watch for surprise interventions.",
            "impact": "NEUTRAL",
            "source": "Policy Context"
        },
        {
            "category": "Oil Revenue",
            "title": "Nigeria Oil Dependency: ~90% of FX Earnings",
            "detail": "Nigeria earns most of its USD from crude oil exports. Brent crude above $80/bbl is generally supportive of NGN. OPEC+ cuts affect volume. Pipeline vandalism reduces output.",
            "impact": "NEUTRAL",
            "source": "Macro Structural"
        },
        {
            "category": "Crypto P2P Dynamics",
            "title": "Binance P2P + KuCoin + LocalBitcoins Nigeria",
            "detail": "After CBN Binance ban in 2024, P2P shifted to other platforms. USDT demand surged as Nigerians hedge against inflation. P2P rate = best proxy for true black market rate.",
            "impact": "BULLISH",
            "source": "Crypto Context"
        },
        {
            "category": "Inflation Differential",
            "title": f"Nigeria Inflation ~28–32% vs US ~3% (2025 est.)",
            "detail": "High inflation differential means NGN structurally weakens over time relative to USD. This creates long-term USDT demand pressure. Short-term volatility around MPC meetings.",
            "impact": "BEARISH",
            "source": "Macro Structural"
        },
        {
            "category": "Remittances",
            "title": "Diaspora Remittances ~$20–25B/Year",
            "detail": "Nigerian diaspora sends billions in USD annually. High during festive seasons (Dec, Easter). Increased remittances = more USD supply = NGN strength. IMTOs and fintechs compete on rates.",
            "impact": "NEUTRAL",
            "source": "Macro Structural"
        },
    ]

    return signals


# ─────────────────────────────────────────────
# FULL ANALYSIS
# ─────────────────────────────────────────────
def run_analysis(api_key: str, news_key: str, rates: dict) -> dict:
    signals = fetch_global_signals(news_key)
    now = datetime.datetime.now()

    ctx = ""
    for i, s in enumerate(signals[:25]):
        ctx += f"\n[{i+1}] CATEGORY: {s.get('category','')}\nTITLE: {s.get('title','')}\nDETAIL: {s.get('detail','')[:220]}\nSOURCE: {s.get('source','')}\n"

    official = rates.get("official")
    black = rates.get("black_market") or rates.get("primary", 0)
    spread = rates.get("spread_pct")

    system = """You are a senior FX strategist and crypto market analyst specializing in Nigerian naira (NGN) and emerging market currencies.

You analyze ALL global factors: US Fed policy, oil markets, crypto sentiment, EM contagion, CBN interventions, political risk, inflation dynamics, remittance flows, and P2P crypto market microstructure.

The BLACK MARKET / P2P rate is the MOST IMPORTANT rate for your analysis — this is the real price Nigerians pay for USDT.

Return ONLY valid raw JSON. No markdown. No backticks. No explanation outside the JSON object."""

    prompt = f"""Analyze the USDT/NGN market comprehensively and produce a 24-hour prediction.

RATE DATA:
- Black Market / P2P USDT Rate: ₦{black:,.2f} (PRIMARY — most important)
- Official CBN / I&E Rate: ₦{f"{official:,.2f}" if official else "N/A"}
- Official-to-Black-Market Spread: {f'{spread:.1f}%' if spread else 'N/A'}
- Data Timestamp: {now.strftime('%A %d %B %Y, %H:%M WAT')}
- Market Session: {'Weekday active hours' if 8<=now.hour<=18 and now.weekday()<5 else 'Off-peak / weekend'}

GLOBAL SIGNALS ({len(signals)} total):
{ctx}

ANALYSIS INSTRUCTIONS:
1. Weight the signals by relevance: Oil price > CBN policy > USD strength > crypto sentiment > political risk > remittances
2. Consider both the direction AND magnitude of the predicted move
3. Provide specific price targets based on the black market rate
4. Be honest — if signals are mixed, say NEUTRAL with a tight range
5. Factor in time-of-day and day-of-week liquidity effects

Return ONLY this exact JSON (no markdown, no backticks):
{{
  "black_market_rate": {black},
  "official_rate": {official or 0},
  "spread_pct": {spread or 0},
  "prediction_direction": "BULLISH|BEARISH|NEUTRAL",
  "predicted_low": <number>,
  "predicted_high": <number>,
  "predicted_midpoint": <number>,
  "confidence_score": <0-100>,
  "accuracy_basis": "<why this confidence level — be specific about signal quality>",
  "time_horizon": "24 hours",
  "timestamp": "{now.isoformat()}",
  "executive_summary": "<3 sentence outlook covering direction, key catalyst, and key risk>",
  "trade_recommendation": "<specific recommendation: hold USDT / convert to NGN / wait / buy USDT — with specific reasoning>",
  "best_time_to_convert": "<e.g. Morning weekday session / After CBN close / Weekend>",
  "key_drivers": [
    {{"signal": "<name>", "impact": "BULLISH|BEARISH|NEUTRAL", "weight": "HIGH|MEDIUM|LOW", "detail": "<2 sentence explanation>", "category": "<Oil|CBN|USD|Crypto|Political|Remittance|Inflation|EM Risk>"}},
    {{"signal": "<name>", "impact": "BULLISH|BEARISH|NEUTRAL", "weight": "HIGH|MEDIUM|LOW", "detail": "<2 sentence explanation>", "category": "<category>"}},
    {{"signal": "<name>", "impact": "BULLISH|BEARISH|NEUTRAL", "weight": "HIGH|MEDIUM|LOW", "detail": "<2 sentence explanation>", "category": "<category>"}},
    {{"signal": "<name>", "impact": "BULLISH|BEARISH|NEUTRAL", "weight": "HIGH|MEDIUM|LOW", "detail": "<2 sentence explanation>", "category": "<category>"}},
    {{"signal": "<name>", "impact": "BULLISH|BEARISH|NEUTRAL", "weight": "HIGH|MEDIUM|LOW", "detail": "<2 sentence explanation>", "category": "<category>"}},
    {{"signal": "<name>", "impact": "BULLISH|BEARISH|NEUTRAL", "weight": "HIGH|MEDIUM|LOW", "detail": "<2 sentence explanation>", "category": "<category>"}}
  ],
  "risk_factors": ["<specific risk 1>", "<specific risk 2>", "<specific risk 3>", "<specific risk 4>"],
  "news_sentiment_score": <-100 to 100>,
  "oil_score": <-100 to 100>,
  "usd_strength_score": <-100 to 100>,
  "cbn_policy_score": <-100 to 100>,
  "crypto_sentiment_score": <-100 to 100>,
  "political_risk_score": <-100 to 100>,
  "weekly_outlook": "<brief 1-week directional view>",
  "sources_analyzed": {len(signals)},
  "black_market_premium_analysis": "<analysis of the current spread between official and black market and what it signals>",
  "model": "USDT-NGN-Oracle-v2"
}}"""

    raw = gemini(prompt, api_key, system)

    try:
        clean = raw.strip()
        if "```" in clean:
            parts = clean.split("```")
            for p in parts:
                p = p.strip()
                if p.startswith("json"):
                    p = p[4:].strip()
                if p.startswith("{"):
                    clean = p
                    break
        if not clean.startswith("{"):
            idx = clean.find("{")
            if idx >= 0:
                clean = clean[idx:]
        last = clean.rfind("}")
        if last >= 0:
            clean = clean[:last+1]

        parsed = json.loads(clean)
        parsed["fetch_success"] = True
        parsed["raw_signals"] = signals
        parsed["rates"] = rates
        return parsed
    except:
        return {
            "fetch_success": False,
            "error": "Could not parse AI response",
            "raw_response": raw,
            "rates": rates
        }


# ─────────────────────────────────────────────
# CHAT
# ─────────────────────────────────────────────
def chat(msg: str, api_key: str, ctx: dict) -> str:
    ctx_str = ""
    if ctx:
        ctx_str = f"""
CURRENT ANALYSIS:
- Black Market Rate: ₦{ctx.get('black_market_rate',0):,}
- Official Rate: ₦{ctx.get('official_rate',0):,}
- Spread: {ctx.get('spread_pct',0):.1f}%
- Direction: {ctx.get('prediction_direction','N/A')}
- Range: ₦{ctx.get('predicted_low',0):,.0f}–₦{ctx.get('predicted_high',0):,.0f}
- Confidence: {ctx.get('confidence_score',0)}%
- Recommendation: {ctx.get('trade_recommendation','')}
- Weekly Outlook: {ctx.get('weekly_outlook','')}
- Executive Summary: {ctx.get('executive_summary','')}
"""
    hist = ""
    for m in st.session_state.chat[-8:]:
        hist += f"\n{'User' if m['r']=='u' else 'Oracle'}: {m['c']}"

    sys = """You are the USDT/NGN Oracle — Nigeria's sharpest AI FX analyst.
You speak like a market pro: direct, confident, no fluff. You know P2P rates, Binance dynamics, CBN policy, oil markets, and global macro cold.
Answer in 3-5 sentences unless a breakdown is asked for. Always give a real, specific answer — never hedge without reason.
If asked about the rate, give the number. If asked for advice, give it clearly with reasoning."""

    return gemini(f"{ctx_str}\n\nPrevious chat:{hist}\n\nUser: {msg}\n\nOracle:", api_key, sys)


# ─────────────────────────────────────────────
# CHECK ALERTS
# ─────────────────────────────────────────────
def check_alerts(rate: float):
    triggered = []
    for i, a in enumerate(st.session_state.alerts):
        if a["type"] == "above" and rate >= a["level"] and i not in st.session_state.alert_triggered:
            triggered.append((i, f"🔔 Rate crossed ABOVE ₦{a['level']:,} — now at ₦{rate:,.0f}"))
            st.session_state.alert_triggered.append(i)
        elif a["type"] == "below" and rate <= a["level"] and i not in st.session_state.alert_triggered:
            triggered.append((i, f"🔔 Rate dropped BELOW ₦{a['level']:,} — now at ₦{rate:,.0f}"))
            st.session_state.alert_triggered.append(i)
    return triggered


# ─────────────────────────────────────────────
# RENDER HELPERS
# ─────────────────────────────────────────────
def score_bar(label, score, color):
    norm = (score + 100) / 2
    st.markdown(f"""
    <div class="prog-wrap">
      <div class="prog-label">
        <span style="color:var(--muted2);font-size:12px;">{label}</span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:{color};">{score:+d}</span>
      </div>
      <div class="prog-track">
        <div class="prog-fill" style="width:{norm}%;background:{color};"></div>
      </div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ── SIDEBAR ──
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:700;
    padding:8px 0 18px;border-bottom:1px solid var(--border);margin-bottom:18px;color:var(--text);">
    ⬡ Oracle Config
    </div>""", unsafe_allow_html=True)

    st.markdown('<p style="font-size:11px;color:var(--muted2);margin-bottom:4px;letter-spacing:1px;">GEMINI API KEY <span style="color:var(--red);">★ REQUIRED</span></p>', unsafe_allow_html=True)
    gkey = st.text_input("gkey", value=st.session_state.gemini_key, type="password",
                         placeholder="AIza...", label_visibility="collapsed")
    st.session_state.gemini_key = gkey
    st.markdown('<p style="font-size:10px;color:var(--muted);margin-top:3px;">Free at <a href="https://aistudio.google.com/apikey" style="color:var(--blue);">aistudio.google.com</a></p>', unsafe_allow_html=True)

    st.markdown('<p style="font-size:11px;color:var(--muted2);margin:14px 0 4px;letter-spacing:1px;">NEWS API KEY <span style="color:var(--muted);">(optional)</span></p>', unsafe_allow_html=True)
    nkey = st.text_input("nkey", value=st.session_state.news_key, type="password",
                         placeholder="For live news headlines", label_visibility="collapsed")
    st.session_state.news_key = nkey
    st.markdown('<p style="font-size:10px;color:var(--muted);margin-top:3px;">Free at <a href="https://newsapi.org" style="color:var(--blue);">newsapi.org</a></p>', unsafe_allow_html=True)

    st.markdown("---")
    run_btn = st.button("🔍 Run Full Analysis", use_container_width=True, type="primary")

    st.markdown("---")

    # Price Alerts
    st.markdown('<p style="font-size:11px;color:var(--muted2);letter-spacing:1px;margin-bottom:10px;">🔔 PRICE ALERTS</p>', unsafe_allow_html=True)
    a_level = st.number_input("Alert price (₦)", min_value=100.0, max_value=9999.0,
                               value=1700.0, step=10.0, label_visibility="visible")
    a_type = st.selectbox("Alert when rate goes:", ["above", "below"], label_visibility="visible")
    if st.button("+ Add Alert", use_container_width=True):
        st.session_state.alerts.append({"level": a_level, "type": a_type})
        st.success(f"Alert set: rate {a_type} ₦{a_level:,}")

    if st.session_state.alerts:
        st.markdown('<p style="font-size:11px;color:var(--muted);margin-top:10px;">Active alerts:</p>', unsafe_allow_html=True)
        for i, a in enumerate(st.session_state.alerts):
            col1, col2 = st.columns([3,1])
            with col1:
                st.markdown(f'<span style="font-size:12px;color:var(--text);">{"▲" if a["type"]=="above" else "▼"} ₦{a["level"]:,}</span>', unsafe_allow_html=True)
            with col2:
                if st.button("✕", key=f"del_{i}"):
                    st.session_state.alerts.pop(i)
                    st.rerun()

    st.markdown("---")
    if st.session_state.last_time:
        elapsed = int((datetime.datetime.now() - st.session_state.last_time).total_seconds() // 60)
        st.markdown(f'<p style="font-size:10px;color:var(--muted);">Last updated: {elapsed}m ago</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:10px;color:var(--muted);margin-top:12px;line-height:1.7;
    padding-top:14px;border-top:1px solid var(--border);">
    ⚠️ Not financial advice. AI predictions carry uncertainty. Always DYOR before converting.
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ── RUN ANALYSIS ──
# ─────────────────────────────────────────────
if run_btn:
    if not gkey:
        st.error("Please enter your Gemini API key in the sidebar.")
    else:
        with st.spinner("Fetching black market rate · Gathering global signals · Running AI analysis..."):
            rates = fetch_rates()
            result = run_analysis(gkey, nkey, rates)
            result["rate_data"] = rates
            st.session_state.result = result
            st.session_state.last_time = datetime.datetime.now()
            # Save to history
            if result.get("fetch_success"):
                st.session_state.history.append({
                    "time": datetime.datetime.now().strftime("%H:%M"),
                    "date": datetime.datetime.now().strftime("%d/%m"),
                    "rate": rates.get("primary", 0),
                    "dir": result.get("prediction_direction", "N/A"),
                    "conf": result.get("confidence_score", 0)
                })
        st.rerun()


# ─────────────────────────────────────────────
# ── HEADER ──
# ─────────────────────────────────────────────
st.markdown("""
<div style="padding:8px 0 18px;">
  <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--blue);
  letter-spacing:3px;text-transform:uppercase;margin-bottom:6px;">
    <span class="live-dot"></span>REAL-TIME MARKET INTELLIGENCE
  </div>
  <h1 style="font-family:'IBM Plex Mono',monospace;font-size:30px;font-weight:700;
  margin:0 0 4px;background:linear-gradient(135deg,#dce8f8,#6b84a0);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
    USDT / NGN Oracle
  </h1>
  <p style="color:var(--muted2);font-size:13px;margin:0;">
    Black market · P2P · Global macro · AI-powered · Gemini 2.5
  </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ── MAIN CONTENT ──
# ─────────────────────────────────────────────
if st.session_state.result:
    p = st.session_state.result
    rd = p.get("rates", {})

    # ── ALERT BANNERS ──
    if rd.get("primary"):
        triggered = check_alerts(rd["primary"])
        for _, msg in triggered:
            st.markdown(f'<div class="alert-box alert-warn">{msg}</div>', unsafe_allow_html=True)

    if not p.get("fetch_success"):
        st.error(f"Analysis failed: {p.get('error','Unknown error')}")
        with st.expander("Debug: Raw AI Response"):
            st.text(p.get("raw_response", "")[:3000])
    else:
        direction = p.get("prediction_direction", "NEUTRAL")
        conf = p.get("confidence_score", 0)
        bm_rate = p.get("black_market_rate", rd.get("primary", 0))
        official = p.get("official_rate", rd.get("official", 0))
        spread = p.get("spread_pct", rd.get("spread_pct", 0))
        pred_low = p.get("predicted_low", 0)
        pred_high = p.get("predicted_high", 0)
        pred_mid = p.get("predicted_midpoint", 0)

        # ── TICKER BAR ──
        items = [
            f'<span class="ticker-item">USDT/NGN (P2P) <span class="val">₦{bm_rate:,.0f}</span></span>',
            f'<span class="ticker-item">OFFICIAL <span class="val">₦{official:,.0f}</span></span>',
            f'<span class="ticker-item">SPREAD <span class="{"up" if spread>0 else "dn"}">+{spread:.1f}%</span></span>',
            f'<span class="ticker-item">24H TARGET <span class="{"up" if direction=="BULLISH" else "dn" if direction=="BEARISH" else "val"}">₦{pred_mid:,.0f}</span></span>',
            f'<span class="ticker-item">CONFIDENCE <span class="val">{conf}%</span></span>',
            f'<span class="ticker-item">DIRECTION <span class="{"up" if direction=="BULLISH" else "dn" if direction=="BEARISH" else "val"}">{direction}</span></span>',
            f'<span class="ticker-item">SIGNALS <span class="val">{p.get("sources_analyzed",0)}</span></span>',
        ]
        ticker_html = "".join(items * 2)
        st.markdown(f'<div class="ticker-wrap"><div class="ticker-inner">{ticker_html}</div></div>', unsafe_allow_html=True)

        # ── TOP METRIC CARDS ──
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown(f"""<div class="mcard mcard-green">
            <div class="mcard-label">Black Market Rate</div>
            <div class="mcard-value" style="color:var(--green);">₦{bm_rate:,.0f}</div>
            <div class="mcard-sub">{rd.get("black_market_source","P2P/CoinGecko")}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="mcard mcard-blue">
            <div class="mcard-label">Official Rate</div>
            <div class="mcard-value" style="color:var(--blue);">₦{official:,.0f}</div>
            <div class="mcard-sub">{rd.get("source_official","CBN/NAFEX")}</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            sc = "var(--red)" if spread > 10 else "var(--amber)" if spread > 5 else "var(--green)"
            st.markdown(f"""<div class="mcard mcard-amber">
            <div class="mcard-label">B.Market Premium</div>
            <div class="mcard-value" style="color:{sc};">+{spread:.1f}%</div>
            <div class="mcard-sub">Over official rate</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            dc = "var(--green)" if direction=="BULLISH" else "var(--red)" if direction=="BEARISH" else "var(--amber)"
            darr = "▲" if direction=="BULLISH" else "▼" if direction=="BEARISH" else "◆"
            st.markdown(f"""<div class="mcard mcard-{'green' if direction=='BULLISH' else 'red' if direction=='BEARISH' else 'amber'}">
            <div class="mcard-label">24H Prediction</div>
            <div class="mcard-value" style="color:{dc};">{darr} {direction}</div>
            <div class="mcard-sub">₦{pred_low:,.0f} – ₦{pred_high:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with c5:
            cc = "var(--green)" if conf >= 65 else "var(--amber)" if conf >= 45 else "var(--red)"
            st.markdown(f"""<div class="mcard mcard-purple">
            <div class="mcard-label">AI Confidence</div>
            <div class="mcard-value" style="color:{cc};">{conf}%</div>
            <div class="mcard-sub">{p.get("sources_analyzed",0)} signals analyzed</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── TABS ──
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Analysis", "🌍 Global Signals", "💱 Converter", "📈 History", "💬 Chat"
        ])

        # ══════ TAB 1: ANALYSIS ══════
        with tab1:
            left, right = st.columns([3, 2])

            with left:
                # Summary card
                badge_cls = "dir-bull" if direction=="BULLISH" else "dir-bear" if direction=="BEARISH" else "dir-neu"
                darr2 = "▲" if direction=="BULLISH" else "▼" if direction=="BEARISH" else "◆"
                st.markdown(f"""
                <div class="ocard">
                  <div class="ocard-title">Market Outlook</div>
                  <span class="dir-badge {badge_cls}">{darr2} {direction} — ₦{pred_mid:,.0f} target</span>
                  <p style="color:#b0c8e8;line-height:1.75;font-size:14px;margin:0 0 14px;">
                    {p.get("executive_summary","")}
                  </p>
                  <div style="background:var(--bg2);border-radius:10px;padding:14px 16px;border:1px solid var(--border2);">
                    <div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--blue);margin-bottom:6px;font-family:'IBM Plex Mono',monospace;">TRADE RECOMMENDATION</div>
                    <p style="margin:0;font-size:13px;color:var(--text);line-height:1.6;">{p.get("trade_recommendation","")}</p>
                  </div>
                  <div style="margin-top:12px;display:flex;gap:12px;flex-wrap:wrap;">
                    <div style="background:var(--bg2);border-radius:8px;padding:10px 14px;border:1px solid var(--border);flex:1;">
                      <div style="font-size:9px;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;font-family:'IBM Plex Mono',monospace;">Best Convert Time</div>
                      <div style="font-size:13px;color:var(--amber);margin-top:4px;">{p.get("best_time_to_convert","N/A")}</div>
                    </div>
                    <div style="background:var(--bg2);border-radius:8px;padding:10px 14px;border:1px solid var(--border);flex:1;">
                      <div style="font-size:9px;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;font-family:'IBM Plex Mono',monospace;">Weekly Outlook</div>
                      <div style="font-size:13px;color:var(--text);margin-top:4px;">{p.get("weekly_outlook","N/A")}</div>
                    </div>
                  </div>
                  <p style="margin:12px 0 0;font-size:11px;color:var(--muted);">
                    <span style="font-family:'IBM Plex Mono',monospace;color:var(--amber);">{conf}% confidence</span> — {p.get("accuracy_basis","")}
                  </p>
                </div>""", unsafe_allow_html=True)

                # Black market premium analysis
                st.markdown(f"""
                <div class="ocard">
                  <div class="ocard-title">Black Market Premium Analysis</div>
                  <p style="font-size:13px;color:#b0c8e8;line-height:1.7;margin:0;">{p.get("black_market_premium_analysis","")}</p>
                </div>""", unsafe_allow_html=True)

                # Key drivers
                st.markdown('<div class="ocard"><div class="ocard-title">Key Signal Drivers</div>', unsafe_allow_html=True)
                for d in p.get("key_drivers", []):
                    impact = d.get("impact","NEUTRAL")
                    wt = d.get("weight","MEDIUM")
                    tc = "tag-bull" if impact=="BULLISH" else "tag-bear" if impact=="BEARISH" else "tag-neu"
                    wc = "tag-hi" if wt=="HIGH" else "tag-med" if wt=="MEDIUM" else "tag-lo"
                    st.markdown(f"""
                    <div class="sig-row">
                      <div class="sig-tags">
                        <span class="tag {tc}">{impact}</span>
                        <span class="tag {wc}">{wt}</span>
                        <span class="tag" style="background:rgba(255,255,255,0.04);color:var(--muted2);">{d.get("category","")}</span>
                        <span class="sig-name">{d.get("signal","")}</span>
                      </div>
                      <div class="sig-detail">{d.get("detail","")}</div>
                    </div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with right:
                # Score breakdown
                st.markdown('<div class="ocard"><div class="ocard-title">Signal Scores</div>', unsafe_allow_html=True)
                scores = [
                    ("News Sentiment", p.get("news_sentiment_score",0)),
                    ("Oil Markets", p.get("oil_score",0)),
                    ("USD Strength", p.get("usd_strength_score",0)),
                    ("CBN Policy", p.get("cbn_policy_score",0)),
                    ("Crypto Sentiment", p.get("crypto_sentiment_score",0)),
                    ("Political Risk", p.get("political_risk_score",0)),
                ]
                for lbl, sc in scores:
                    color = "var(--green)" if sc > 20 else "var(--red)" if sc < -20 else "var(--amber)"
                    score_bar(lbl, sc, color)
                st.markdown('</div>', unsafe_allow_html=True)

                # Risk factors
                risks = p.get("risk_factors", [])
                if risks:
                    st.markdown('<div class="ocard"><div class="ocard-title">⚠️ Risk Factors</div>', unsafe_allow_html=True)
                    for r in risks:
                        st.markdown(f'<div class="alert-box alert-warn" style="margin-bottom:8px;">⚡ {r}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Rate comparison table
                st.markdown("""
                <div class="ocard">
                  <div class="ocard-title">Rate Comparison</div>
                  <table class="spread-table">
                    <tr><th>Market</th><th>Rate (₦)</th><th>Status</th></tr>""", unsafe_allow_html=True)

                rows = [
                    ("P2P / Black Market", bm_rate, "PRIMARY", "var(--green)"),
                    ("Official CBN/NAFEX", official, "REFERENCE", "var(--blue)"),
                    ("24H Predicted Low", pred_low, "FORECAST", "var(--muted2)"),
                    ("24H Predicted High", pred_high, "FORECAST", "var(--muted2)"),
                ]
                for name, val, status, color in rows:
                    st.markdown(f'<tr><td>{name}</td><td style="font-family:\'IBM Plex Mono\',monospace;color:{color};">₦{val:,.0f}</td><td style="font-size:11px;color:var(--muted);">{status}</td></tr>', unsafe_allow_html=True)
                st.markdown('</table></div>', unsafe_allow_html=True)

        # ══════ TAB 2: GLOBAL SIGNALS ══════
        with tab2:
            signals = p.get("raw_signals", [])
            categories = list(dict.fromkeys(s.get("category","") for s in signals))

            for cat in categories:
                cat_signals = [s for s in signals if s.get("category") == cat]
                st.markdown(f'<div class="ocard"><div class="ocard-title">📡 {cat}</div>', unsafe_allow_html=True)
                for s in cat_signals:
                    impact = s.get("impact","NEUTRAL")
                    tc = "tag-bull" if impact=="BULLISH" else "tag-bear" if impact=="BEARISH" else "tag-neu" if impact in ("NEUTRAL","UNKNOWN") else "tag-neu"
                    pub = s.get("published","")[:10] if s.get("published") else ""
                    src = s.get("source","")
                    url = s.get("url","")
                    link = f'<a href="{url}" target="_blank" style="color:var(--blue);font-size:11px;">→ Read</a>' if url else ""
                    st.markdown(f"""
                    <div class="sig-row">
                      <div class="sig-tags">
                        <span class="tag {tc}">{impact}</span>
                        <span style="font-size:11px;color:var(--muted);">{src}{' · '+pub if pub else ''}</span>
                        {link}
                      </div>
                      <div class="sig-name" style="font-size:13px;margin-bottom:4px;">{s.get("title","")}</div>
                      <div class="sig-detail">{s.get("detail","")[:250]}</div>
                    </div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # ══════ TAB 3: CONVERTER ══════
        with tab3:
            st.markdown('<div class="ocard"><div class="ocard-title">💱 Currency Converter</div>', unsafe_allow_html=True)

            conv_dir = st.radio("Convert:", ["USDT → NGN", "NGN → USDT"], horizontal=True)
            amt = st.number_input("Amount", min_value=0.0, value=100.0, step=10.0)
            rate_choice = st.radio("Use rate:", ["Black Market (P2P)", "Official Rate", "Predicted Midpoint"], horizontal=True)

            rate_map = {
                "Black Market (P2P)": bm_rate,
                "Official Rate": official,
                "Predicted Midpoint": pred_mid
            }
            used_rate = rate_map[rate_choice]

            if conv_dir == "USDT → NGN":
                converted = amt * used_rate
                st.markdown(f"""
                <div class="conv-box" style="margin-top:12px;">
                  <div style="text-align:center;color:var(--muted2);font-size:13px;margin-bottom:6px;">{amt:,.2f} USDT at ₦{used_rate:,.2f}</div>
                  <div class="conv-result">₦{converted:,.2f}</div>
                  <div style="text-align:center;font-size:11px;color:var(--muted);margin-top:8px;">Using {rate_choice} rate</div>
                </div>""", unsafe_allow_html=True)
            else:
                converted = amt / used_rate if used_rate else 0
                st.markdown(f"""
                <div class="conv-box" style="margin-top:12px;">
                  <div style="text-align:center;color:var(--muted2);font-size:13px;margin-bottom:6px;">₦{amt:,.2f} NGN at ₦{used_rate:,.2f}/USDT</div>
                  <div class="conv-result">{converted:,.4f} USDT</div>
                  <div style="text-align:center;font-size:11px;color:var(--muted);margin-top:8px;">Using {rate_choice} rate</div>
                </div>""", unsafe_allow_html=True)

            # Rate comparison for converter
            st.markdown(f"""
            <div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;">
              <div style="background:var(--bg2);border-radius:8px;padding:12px;text-align:center;border:1px solid var(--border);">
                <div style="font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;">If Black Market</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:16px;color:var(--green);margin-top:4px;">
                  {'₦'+f'{amt*bm_rate:,.0f}' if conv_dir=='USDT → NGN' else f'{amt/bm_rate:.4f} USDT'}
                </div>
              </div>
              <div style="background:var(--bg2);border-radius:8px;padding:12px;text-align:center;border:1px solid var(--border);">
                <div style="font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;">If Official</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:16px;color:var(--blue);margin-top:4px;">
                  {'₦'+f'{amt*official:,.0f}' if conv_dir=='USDT → NGN' else f'{amt/official:.4f} USDT'}
                </div>
              </div>
              <div style="background:var(--bg2);border-radius:8px;padding:12px;text-align:center;border:1px solid var(--border);">
                <div style="font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;">If Predicted</div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:16px;color:var(--amber);margin-top:4px;">
                  {'₦'+f'{amt*pred_mid:,.0f}' if conv_dir=='USDT → NGN' else f'{amt/pred_mid:.4f} USDT' if pred_mid else 'N/A'}
                </div>
              </div>
            </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ══════ TAB 4: HISTORY ══════
        with tab4:
            hist = st.session_state.history
            if len(hist) < 2:
                st.markdown("""
                <div class="ocard" style="text-align:center;padding:40px;">
                  <div style="font-size:32px;margin-bottom:12px;opacity:0.3;">📈</div>
                  <p style="color:var(--muted2);">Run analysis multiple times to build a history log.<br>Each run is tracked here with rate, direction, and confidence.</p>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="ocard"><div class="ocard-title">Analysis History Log</div>', unsafe_allow_html=True)
                st.markdown("""<table class="spread-table">
                <tr><th>Date</th><th>Time</th><th>Black Market Rate</th><th>Direction</th><th>Confidence</th></tr>""", unsafe_allow_html=True)
                for h in reversed(hist):
                    dc = "var(--green)" if h["dir"]=="BULLISH" else "var(--red)" if h["dir"]=="BEARISH" else "var(--amber)"
                    da = "▲" if h["dir"]=="BULLISH" else "▼" if h["dir"]=="BEARISH" else "◆"
                    st.markdown(f"""<tr>
                    <td style="color:var(--muted2);">{h['date']}</td>
                    <td style="font-family:'IBM Plex Mono',monospace;">{h['time']}</td>
                    <td style="font-family:'IBM Plex Mono',monospace;color:var(--green);">₦{h['rate']:,.0f}</td>
                    <td style="color:{dc};font-weight:600;">{da} {h['dir']}</td>
                    <td style="font-family:'IBM Plex Mono',monospace;color:var(--amber);">{h['conf']}%</td>
                    </tr>""", unsafe_allow_html=True)
                st.markdown('</table></div>', unsafe_allow_html=True)

        # ══════ TAB 5: CHAT ══════
        with tab5:
            st.markdown('<div class="ocard"><div class="ocard-title">💬 Ask the Oracle Anything</div>', unsafe_allow_html=True)

            if not st.session_state.chat:
                st.markdown("""
                <div class="chat-a">
                  <div class="chat-badge">⬡ ORACLE</div>
                  I'm your USDT/NGN Oracle. Ask me anything — current rate outlook, when to convert, what's driving the market, CBN news, oil impact, or how to read the signals. I'm grounded in the latest analysis data.
                </div>""", unsafe_allow_html=True)

            for m in st.session_state.chat:
                if m["r"] == "u":
                    st.markdown(f'<div class="chat-u">🧑 {m["c"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-a"><div class="chat-badge">⬡ ORACLE</div>{m["c"]}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # Quick prompts
            st.markdown('<p style="font-size:10px;color:var(--muted);letter-spacing:1px;text-transform:uppercase;margin-top:12px;">Quick Questions</p>', unsafe_allow_html=True)
            qcols = st.columns(2)
            qs = [
                "Should I convert my USDT to naira today?",
                "What's the best time this week to convert?",
                "How is oil price affecting the naira right now?",
                "What would make the naira strengthen suddenly?"
            ]
            clicked = None
            for i, q in enumerate(qs):
                with qcols[i % 2]:
                    if st.button(q, key=f"q{i}", use_container_width=True):
                        clicked = q

            col1, col2 = st.columns([5, 1])
            with col1:
                user_msg = st.text_input("msg", placeholder="Type your question here...", label_visibility="collapsed", key="chat_in")
            with col2:
                send = st.button("Send →", use_container_width=True)

            question = user_msg if (send and user_msg) else clicked

            if question and gkey:
                st.session_state.chat.append({"r": "u", "c": question})
                with st.spinner("Oracle thinking..."):
                    reply = chat(question, gkey, p)
                st.session_state.chat.append({"r": "a", "c": reply})
                st.rerun()
            elif question and not gkey:
                st.warning("Add your Gemini API key in the sidebar first.")

            if st.session_state.chat:
                if st.button("🗑 Clear Chat"):
                    st.session_state.chat = []
                    st.rerun()

# ── EMPTY STATE ──
else:
    st.markdown("""
    <div style="text-align:center;padding:70px 20px 40px;">
      <div style="font-size:60px;margin-bottom:16px;opacity:0.15;font-family:'IBM Plex Mono',monospace;">₦</div>
      <h2 style="font-family:'IBM Plex Mono',monospace;color:#243550;font-size:20px;margin-bottom:10px;">Ready to Analyze</h2>
      <p style="color:#2d4a6a;max-width:520px;margin:0 auto 28px;line-height:1.7;font-size:14px;">
        Add your <strong style="color:var(--blue);">Gemini API key</strong> in the sidebar and click
        <strong style="color:var(--blue);">Run Full Analysis</strong>. The Oracle will fetch the
        black market P2P rate, scan global signals — oil, USD, crypto, CBN, politics —
        and give you an AI-powered 24-hour prediction with confidence scoring.
      </p>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:600px;margin:0 auto;">
        <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px 12px;">
          <div style="font-size:26px;margin-bottom:8px;">🖤</div>
          <div style="font-size:12px;color:var(--muted2);">Black Market Rate</div>
        </div>
        <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px 12px;">
          <div style="font-size:26px;margin-bottom:8px;">🌍</div>
          <div style="font-size:12px;color:var(--muted2);">Global Signals</div>
        </div>
        <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px 12px;">
          <div style="font-size:26px;margin-bottom:8px;">💱</div>
          <div style="font-size:12px;color:var(--muted2);">Smart Converter</div>
        </div>
        <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px 12px;">
          <div style="font-size:26px;margin-bottom:8px;">🔔</div>
          <div style="font-size:12px;color:var(--muted2);">Price Alerts</div>
        </div>
        <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px 12px;">
          <div style="font-size:26px;margin-bottom:8px;">📈</div>
          <div style="font-size:12px;color:var(--muted2);">History Log</div>
        </div>
        <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px 12px;">
          <div style="font-size:26px;margin-bottom:8px;">💬</div>
          <div style="font-size:12px;color:var(--muted2);">AI Chat Oracle</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)