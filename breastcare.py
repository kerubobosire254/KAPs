"""
BreastCare Kenya — Clinical Decision Support Platform v2.0
Elevated for recruiter showcase | Build54 Hackathon Project
Author: Kerubo Bosire | github.com/kerubobosire254

ZERO API KEYS REQUIRED — Fully offline-capable.
CareBot uses rule-based NLP with a rich clinical knowledge base.

Run:
    pip install streamlit plotly pandas
    streamlit run breastcare.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import re

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BreastCare Kenya",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DESIGN SYSTEM ──────────────────────────────────────────────────────────────
PINK      = "#e91e8c"
PINK_DARK = "#ad1457"
PINK_SOFT = "#fce4ec"
PURPLE    = "#4a148c"
PURPLE_MID= "#7b1fa2"
PURPLE_SOFT="#f3e5f5"
TEAL      = "#00897b"
AMBER     = "#f57c00"
RED       = "#c62828"
GREEN     = "#2e7d32"
BLUE      = "#1565c0"
DARK      = "#1a0a2e"

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

/* Apply font only to text elements — never to SVG/icons */
body, p, h1, h2, h3, h4, h5, h6, span, div, label, button,
input, textarea, select, .stMarkdown, .stText {{
    font-family: 'Plus Jakarta Sans', sans-serif;
}}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(170deg, {DARK} 0%, #2d0a5a 55%, #4a0072 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}}
/* Target only text nodes in sidebar, not SVG arrows */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] .stMarkdown {{
    color: #f3e5f5;
}}
section[data-testid="stSidebar"] .stRadio label {{
    background: rgba(255,255,255,0.05);
    border-radius: 12px; padding: 11px 16px;
    margin: 4px 0; display: block;
    transition: all 0.2s; cursor: pointer;
    font-weight: 600; font-size: .9rem;
    border: 1px solid transparent;
}}
section[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(233,30,140,0.18);
    border-color: rgba(233,30,140,0.4);
}}

/* ── MAIN ── */
.main {{ background: #ffffff; }}
.block-container {{ background: #ffffff; }}

/* ── HERO BANNER ── */
.hero {{
    background: linear-gradient(135deg, {DARK} 0%, #6a0080 40%, {PINK_DARK} 100%);
    border-radius: 20px; padding: 2.5rem 2.8rem;
    color: white; margin-bottom: 1.6rem;
    position: relative; overflow: hidden;
}}
.hero::before {{
    content: "🎗️";
    position: absolute; right: 2rem; top: 50%;
    transform: translateY(-50%);
    font-size: 7rem; opacity: 0.12;
}}
.hero h1 {{ margin: 0; font-size: 2.1rem; font-weight: 900; letter-spacing: -.02em; }}
.hero p  {{ margin: .5rem 0 0; opacity: .88; font-size: 1rem; font-weight: 400; max-width: 70%; }}
.hero .kap-strip {{
    display: flex; gap: 1.6rem; margin-top: 1.4rem; flex-wrap: wrap;
}}
.hero .kap-pill {{
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 50px; padding: 7px 18px;
    font-size: .82rem; font-weight: 700;
}}
.hero .kap-pill span {{ color: #ffb3d9; font-size: 1.05rem; font-weight: 900; }}

/* ── GLASS CARDS ── */
.gcard {{
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 4px 24px rgba(74,20,140,0.10);
    margin-bottom: 1rem;
    border: 1px solid rgba(233,30,140,0.12);
}}
.gcard.red   {{ border-left: 5px solid {RED};   background: rgba(255,235,235,0.9); }}
.gcard.orange{{ border-left: 5px solid {AMBER};  background: rgba(255,248,235,0.9); }}
.gcard.green {{ border-left: 5px solid {GREEN};  background: rgba(235,255,235,0.9); }}
.gcard.blue  {{ border-left: 5px solid {BLUE};   background: rgba(235,245,255,0.9); }}
.gcard.pink  {{ border-left: 5px solid {PINK};   background: rgba(252,228,236,0.9); }}
.gcard.purple{{ border-left: 5px solid {PURPLE}; }}
.gcard h3 {{ margin: 0 0 .4rem; font-size: 1rem; font-weight: 800; color: #1a0a2e; }}
.gcard p  {{ margin: 0; color: #555; font-size: .9rem; }}

/* ── METRIC TILES ── */
.metric-row {{ display: flex; gap: 1rem; margin-bottom: 1.2rem; flex-wrap: wrap; }}
.mtile {{
    flex: 1; min-width: 120px;
    background: white;
    border-radius: 16px; padding: 1.1rem 1.2rem; text-align: center;
    box-shadow: 0 2px 12px rgba(74,20,140,0.09);
    border-top: 4px solid {PINK};
    position: relative; overflow: hidden;
}}
.mtile.t2 {{ border-top-color: {PURPLE_MID}; }}
.mtile.t3 {{ border-top-color: {TEAL}; }}
.mtile.t4 {{ border-top-color: {AMBER}; }}
.mtile.t5 {{ border-top-color: {RED}; }}
.mtile h2 {{ font-size: 2.2rem; margin: 0; font-weight: 900; color: {DARK}; line-height: 1; }}
.mtile p  {{ margin: .3rem 0 0; color: #888; font-size: .78rem; font-weight: 700;
             text-transform: uppercase; letter-spacing: .05em; }}

/* ── RISK BADGE ── */
.risk-badge {{
    display: inline-block; padding: 6px 18px; border-radius: 30px;
    font-weight: 800; font-size: .9rem; letter-spacing: .05em;
    text-transform: uppercase;
}}
.risk-HIGH     {{ background: {RED};   color: white; }}
.risk-MODERATE {{ background: {AMBER}; color: white; }}
.risk-LOW      {{ background: {GREEN}; color: white; }}

/* ── REFERRAL CARDS ── */
.ref-banner {{
    border-radius: 16px; padding: 1.4rem 1.8rem;
    color: white; margin: .6rem 0;
    font-weight: 700; font-size: .95rem;
}}
.ref-URGENT    {{ background: linear-gradient(90deg,#b71c1c,#e53935); }}
.ref-IMAGING   {{ background: linear-gradient(90deg,#0d47a1,#1565c0); }}
.ref-ROUTINE   {{ background: linear-gradient(90deg,#e65100,#f57c00); }}
.ref-EDUCATION {{ background: linear-gradient(90deg,#1b5e20,#2e7d32); }}

/* ── SECTION HEADER ── */
.section-head {{
    font-size: 1.65rem; font-weight: 900; color: {DARK};
    border-bottom: 3px solid {PINK};
    padding-bottom: .4rem; margin-bottom: .3rem;
}}
.section-sub {{ color: {PURPLE_MID}; font-weight: 600; font-size: .88rem; margin-bottom: 1.1rem; }}

/* ── CONNECTION FLOW BANNER ── */
.conn-flow {{
    background: linear-gradient(90deg, {DARK}, #4a0072);
    border-radius: 12px; padding: .9rem 1.3rem;
    color: #f3e5f5; font-size: .87rem; font-weight: 600;
    margin: 1rem 0; border: 1px solid rgba(233,30,140,0.3);
}}
.conn-flow span {{ color: #ff80ab; font-weight: 800; }}

/* ── JOURNEY TIMELINE ── */
.tl-step {{
    display: flex; gap: 14px; align-items: flex-start;
    padding: .75rem 0; border-bottom: 1px dashed #e8d5f5;
}}
.tl-dot {{
    width: 14px; height: 14px; border-radius: 50%; flex-shrink: 0; margin-top: 4px;
}}
.tl-done    {{ background: {GREEN}; }}
.tl-active  {{ background: {AMBER}; box-shadow: 0 0 0 4px rgba(245,124,0,.25); }}
.tl-pending {{ background: #bdbdbd; }}
.tl-urgent  {{ background: {RED};   box-shadow: 0 0 0 4px rgba(198,40,40,.25); }}
.tl-label   {{ font-weight: 800; font-size: .92rem; color: {DARK}; }}
.tl-sub     {{ font-size: .78rem; color: #888; margin-top: 2px; }}

/* ── CHECKLIST ITEMS ── */
.check-item {{
    background: white; border-radius: 10px; padding: .7rem 1rem; margin: .3rem 0;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05); border-left: 4px solid {PINK};
    font-size: .9rem;
}}
.check-item.flag {{ border-color: {RED}; background: #fff5f5; font-weight: 700; }}

/* ── CONNECTIVITY BADGE ── */
.conn-badge {{
    display: inline-block; border-radius: 20px; padding: 5px 16px;
    font-size: .78rem; font-weight: 700; letter-spacing: .03em;
}}
.conn-online  {{ background: rgba(46,125,50,.18); color: #a5d6a7; border: 1.5px solid #a5d6a7; }}
.conn-offline {{ background: rgba(255,193,7,.15);  color: #ffe082; border: 1.5px solid #ffe082; }}

/* ── CAREBOT ── */
.chat-wrap {{
    display: flex; flex-direction: column; gap: .7rem;
    max-height: 500px; overflow-y: auto;
    padding: .5rem .2rem; margin-bottom: 1rem;
    scrollbar-width: thin;
}}
.chat-msg {{ display: flex; gap: .65rem; align-items: flex-start; }}
.chat-msg.user {{ flex-direction: row-reverse; }}
.chat-avatar {{
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}}
.chat-avatar.bot  {{ background: linear-gradient(135deg,{PURPLE},{PINK_DARK}); }}
.chat-avatar.user {{ background: #f3e5f5; }}
.chat-bubble {{
    max-width: 82%; padding: .8rem 1.1rem; border-radius: 16px;
    font-size: .9rem; line-height: 1.6;
}}
.chat-bubble.bot {{
    background: white; color: {DARK};
    border: 1px solid rgba(233,30,140,0.15);
    border-top-left-radius: 4px;
    box-shadow: 0 2px 8px rgba(74,20,140,0.08);
}}
.chat-bubble.user {{
    background: linear-gradient(135deg,{PURPLE},{PINK_DARK});
    color: white; border-top-right-radius: 4px;
}}
.chat-chip-row {{ display: flex; flex-wrap: wrap; gap: .4rem; margin-top: .6rem; }}
.chat-chip {{
    background: {PINK_SOFT}; color: {PINK_DARK};
    border: 1px solid rgba(233,30,140,0.25);
    border-radius: 20px; padding: 5px 13px;
    font-size: .8rem; font-weight: 700; cursor: pointer;
}}

/* ── KAP GAP CHART LABEL ── */
.kap-label {{
    font-size: .75rem; font-weight: 700; color: #888;
    text-transform: uppercase; letter-spacing: .06em;
    margin-bottom: .2rem;
}}

/* ── STORY BANNER ── */
.story-banner {{
    background: linear-gradient(90deg,#880e4f,#4a148c);
    border-radius: 14px; padding: 1.1rem 1.5rem;
    color: white; margin-bottom: 1.1rem;
}}
.story-banner h4 {{ margin: 0 0 .3rem; font-size: 1rem; font-weight: 800; }}
.story-banner p  {{ margin: 0; font-size: .87rem; opacity: .9; }}

/* ── HANDOVER CARD ── */
.handover {{
    background: white; border: 2px solid {PINK};
    border-radius: 16px; padding: 1.5rem 2rem;
    font-family: monospace; font-size: .82rem;
    line-height: 1.9; color: #1a0a2e;
    white-space: pre-wrap;
}}

/* ── ABOUT BADGE ── */
.about-badge {{
    background: rgba(233,30,140,0.12);
    border: 1px solid rgba(233,30,140,0.3);
    border-radius: 12px; padding: .8rem 1rem;
    font-size: .78rem; color: #f3e5f5; line-height: 1.8;
    margin-top: .5rem;
}}

/* ── EXPANDER FIX — prevent arrow/text overlap ── */
details summary {{
    list-style: none;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-weight: 600;
    font-size: .95rem;
    padding: 12px 0;
    user-select: none;
}}
details summary::-webkit-details-marker {{ display: none; }}
/* Make sure Streamlit's built-in expander label has room */
.streamlit-expanderHeader {{
    font-weight: 600 !important;
    font-size: .95rem !important;
}}
/* Prevent SVG icons from inheriting forced colors */
svg, svg * {{
    color: unset !important;
    fill: currentColor;
}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CAREBOT — Rule-Based NLP (Zero API, Fully Offline)
# ══════════════════════════════════════════════════════════════════════════════

CLINICAL_KB = {
    # ── Risk factors ──
    r"risk factor|what causes|cause|cause of breast": {
        "title": "🔴 Key Breast Cancer Risk Factors",
        "body": (
            "**Non-modifiable risks:**\n"
            "• Age ≥50 — risk doubles after menopause\n"
            "• 1st-degree family history — 2× increased risk\n"
            "• BRCA1/BRCA2 gene mutations — up to 72% lifetime risk\n"
            "• Previous breast biopsy with atypical cells\n"
            "• Early menarche (<13 yrs) or late menopause (>55 yrs)\n\n"
            "**Modifiable risks:**\n"
            "• Obesity post-menopause (BMI ≥30)\n"
            "• HRT use >5 years\n"
            "• Alcohol consumption\n"
            "• Nulliparity or first child after age 30\n\n"
            "**Protective factors:** Breastfeeding ≥1 year reduces risk by ~10%."
        )
    },
    r"bse|breast self.?exam|self examination|self-exam": {
        "title": "✋ Breast Self-Examination (BSE) Guide",
        "body": (
            "**Best time:** 7–10 days after start of period (when breasts are least tender).\n"
            "Post-menopausal: same day each month.\n\n"
            "**Standing — Visual Check:**\n"
            "1. Arms at sides — look for size/shape changes, skin dimpling\n"
            "2. Arms raised above head — check contour and nipple symmetry\n"
            "3. Hands on hips, lean forward — check for tethering\n\n"
            "**Lying Down — Palpation:**\n"
            "4. Use flat of 3 middle fingers with circular motion\n"
            "5. Cover entire breast in a systematic pattern (grid or spiral)\n"
            "6. Include axilla (armpit) area\n"
            "7. Gently squeeze nipple — check for discharge\n\n"
            "**Report immediately:** New lump, skin changes, bloody discharge, nipple inversion."
        )
    },
    r"referral|when to refer|urgent refer|refer patient|refer": {
        "title": "🔀 Kenya Referral Criteria (MOH Guidelines)",
        "body": (
            "**URGENT (within 24 hours):**\n"
            "• Hard, fixed or irregular palpable lump\n"
            "• Palpable axillary lymph nodes\n"
            "• Skin tethering or peau d'orange\n"
            "• Ulceration on breast\n"
            "• Nipple retraction (new onset)\n"
            "• Post-menopausal lump (any size)\n\n"
            "**IMAGING (within 2 weeks):**\n"
            "• Nipple discharge (non-milk, unilateral)\n"
            "• Asymmetry or thickening, especially age ≥40\n"
            "• Strong family history (BRCA/2+ relatives)\n\n"
            "**ROUTINE (4–6 weeks):**\n"
            "• Cyclical breast pain without mass\n"
            "• Mild asymmetry, no red flags\n\n"
            "**Source:** Kenya MOH Breast Cancer Referral Pathway, Level 2–3."
        )
    },
    r"staging|stage|stage i|stage ii|stage iii|stage iv|stages": {
        "title": "📊 Breast Cancer Staging",
        "body": (
            "**Stage I:** Tumour ≤2 cm, no lymph node involvement. 5-yr survival ~99%\n"
            "**Stage II:** Tumour 2–5 cm or limited lymph node spread. 5-yr survival ~86%\n"
            "**Stage III:** Tumour >5 cm, multiple nodes, or chest wall involvement. 5-yr survival ~57%\n"
            "**Stage IV (Metastatic):** Spread to distant organs (lung, bone, liver, brain). 5-yr survival ~28%\n\n"
            "⚠️ **Kenya context:** 78% of patients present at Stage III or IV. Early detection at Stage I or II is the mission of BreastCare Kenya."
        )
    },
    r"kap|knowledge|attitude|practice|gap|score|survey|practitioner": {
        "title": "📋 Kenya KAP Survey Findings (n=250)",
        "body": (
            "This platform is built on a KAP survey of 250 Kenyan health practitioners.\n\n"
            "| Domain       | Mean Score | Category   |\n"
            "|:-------------|:----------:|:----------:|\n"
            "| 🧠 Knowledge  |   54.7%    |    Poor    |\n"
            "| 💬 Attitude   |   65.2%    |  Neutral   |\n"
            "| 🏥 Practice   | **29.2%**  | **Critical** |\n\n"
            "**By profession (practice scores):**\n"
            "• Community Health Workers: 12.7%\n"
            "• Nurses: 27%\n"
            "• Clinical Officers: 31%\n"
            "• Doctors: 44%\n\n"
            "The 36-point attitude–practice gap is the problem BreastCare Kenya solves."
        )
    },
    r"lump|breast lump|lump in breast|felt a lump": {
        "title": "🔍 Assessing a Breast Lump",
        "body": (
            "**Concerning features (refer urgently):**\n"
            "• Hard, irregular, non-tender, fixed to underlying tissue\n"
            "• Skin tethering or dimpling overlying the lump\n"
            "• Associated axillary lymph nodes\n"
            "• Nipple retraction or discharge\n\n"
            "**Less concerning (but still assess):**\n"
            "• Soft, smooth, mobile, well-defined (may be fibroadenoma/cyst)\n"
            "• Tender — often benign, but still needs evaluation\n\n"
            "**Always:** Document size, shape, mobility, tenderness, and skin changes.\n"
            "Use the Risk Assessment module to calculate a score and determine the referral pathway."
        )
    },
    r"nipple|nipple discharge|discharge": {
        "title": "💧 Nipple Discharge — Assessment Guide",
        "body": (
            "**Concerning (refer for imaging/biopsy):**\n"
            "• Bloody or blood-stained discharge\n"
            "• Unilateral, single duct discharge\n"
            "• Spontaneous (without squeezing)\n"
            "• Associated with a lump\n\n"
            "**Less concerning:**\n"
            "• Bilateral, multi-duct, milky or green\n"
            "• Only on squeezing\n"
            "• In premenopausal women on OCP (common variant)\n\n"
            "**Important:** Any nipple discharge in a post-menopausal woman should be referred."
        )
    },
    r"mammogram|mammography|ultrasound|imaging|scan": {
        "title": "🖼️ Breast Imaging in Kenya",
        "body": (
            "**Mammography:**\n"
            "• Gold standard for women ≥40 years\n"
            "• Sensitivity 77–95%, specificity ~90%\n"
            "• Annual screening recommended for high-risk women aged 40–74\n"
            "• Available at KNH, Coast General, Aga Khan, Nairobi Hospital\n\n"
            "**Ultrasound:**\n"
            "• Preferred for women <40 (dense breast tissue)\n"
            "• Good for distinguishing cyst vs solid mass\n"
            "• Widely available at county hospitals\n\n"
            "**Barriers in Kenya:** Cost (KES 2,000–8,000), limited machines in rural areas, low referral rates by practitioners."
        )
    },
    r"treatment|chemotherapy|surgery|radiation|hormone therapy|tamoxifen|chemo": {
        "title": "💊 Breast Cancer Treatment Overview",
        "body": (
            "Treatment depends on stage, receptor status, and patient preference.\n\n"
            "**Surgery:** Lumpectomy (breast-conserving) or mastectomy\n"
            "**Chemotherapy:** Neoadjuvant (before surgery) or adjuvant (after)\n"
            "**Radiotherapy:** After lumpectomy; sometimes after mastectomy\n"
            "**Hormone therapy:** For ER/PR-positive tumours (e.g. Tamoxifen, Letrozole)\n"
            "**Targeted therapy:** Trastuzumab (Herceptin) for HER2-positive disease\n\n"
            "**Kenya context:** Treatment is available at national/county referral hospitals. NHIF covers some costs. Advocate strongly for early referral — Stage I treatment costs 10× less than Stage IV."
        )
    },
    r"follow.?up|after referral|what next|next step": {
        "title": "🔔 Follow-Up Protocol",
        "body": (
            "**After Urgent Referral:**\n"
            "• Contact facility to confirm appointment made\n"
            "• Follow up with patient within 48 hours\n"
            "• If no response in 72 hours — escalate to community health worker\n\n"
            "**After Imaging Referral:**\n"
            "• Book follow-up in 2 weeks to review results\n"
            "• Call patient the day before their imaging appointment\n\n"
            "**After Routine/Education:**\n"
            "• Schedule return in 4–6 weeks\n"
            "• Ensure BSE technique demonstrated before leaving\n\n"
            "Use the **Follow-Up Tracker** module to log all patients automatically."
        )
    },
    r"prevention|prevent|reduce risk|reduce my risk": {
        "title": "🛡️ Breast Cancer Prevention",
        "body": (
            "**Lifestyle modifications that reduce risk:**\n"
            "• Maintain healthy weight (BMI 18.5–24.9)\n"
            "• Exercise ≥150 min/week of moderate activity\n"
            "• Limit alcohol — even 1 drink/day increases risk 7–10%\n"
            "• Avoid smoking\n"
            "• Breastfeed if possible (≥1 year is protective)\n\n"
            "**Screening (early detection, not prevention):**\n"
            "• Monthly BSE from age 20\n"
            "• Clinical breast exam every 1–3 years (age 20–39)\n"
            "• Annual mammogram from age 40 (or earlier if high risk)\n\n"
            "**Note:** Screening does not prevent cancer — it finds it early when it's most treatable."
        )
    },
    r"hello|hi|hey|good morning|good afternoon|greet": {
        "title": "👋 Hello!",
        "body": "I'm **CareBot**, your offline clinical support assistant for BreastCare Kenya.\n\nI can answer questions about:\n• 🔴 Risk factors & KAP survey findings\n• ✋ BSE technique\n• 🔀 Referral criteria & pathways\n• 📊 Cancer staging\n• 🖼️ Imaging options in Kenya\n• 💊 Treatment overview\n• 🔔 Follow-up protocols\n\nType your question or tap one of the quick buttons below."
    },
}

QUICK_QUESTIONS = [
    "How do I perform a BSE?",
    "When should I refer urgently?",
    "What does the KAP data show?",
    "What are the breast cancer stages?",
    "What imaging is available in Kenya?",
    "How do I assess a breast lump?",
    "What are the key risk factors?",
]

def carebot_respond(user_text: str) -> str:
    """Rule-based NLP using regex pattern matching against clinical KB."""
    text = user_text.lower().strip()
    for pattern, response in CLINICAL_KB.items():
        if re.search(pattern, text):
            return f"### {response['title']}\n\n{response['body']}"
    # Fallback
    return (
        "I don't have a specific answer for that, but I can help with:\n\n"
        "• **BSE technique** — type 'how do I do a BSE?'\n"
        "• **Referral criteria** — type 'when should I refer?'\n"
        "• **Risk factors** — type 'what are the risk factors?'\n"
        "• **Staging** — type 'what are the stages?'\n"
        "• **KAP findings** — type 'what does the KAP data show?'\n\n"
        "Or use the **Risk Assessment** module to evaluate a patient right now."
    )


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE — single source of truth
# ══════════════════════════════════════════════════════════════════════════════

def init_state():
    if "active_patient" not in st.session_state:
        st.session_state.active_patient = {}
    if "checklist_symptoms" not in st.session_state:
        st.session_state.checklist_symptoms = {
            "lump": False, "nipple_dc": False, "skin_changes": False,
            "nipple_invert": False, "axillary": False, "ulceration": False,
            "breast_pain": False, "asymmetry": False,
        }
    if "assessment_red_flags" not in st.session_state:
        st.session_state.assessment_red_flags = []
    if "assessment_context" not in st.session_state:
        st.session_state.assessment_context = {}
    if "last_referral" not in st.session_state:
        st.session_state.last_referral = {}
    if "grace_demo" not in st.session_state:
        st.session_state.grace_demo = False
    if "checklist_step" not in st.session_state:
        st.session_state.checklist_step = 1
    if "_nav_idx" not in st.session_state:
        st.session_state["_nav_idx"] = 0
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "bot", "text": carebot_respond("hello")}
        ]
    if "reassess_patient" not in st.session_state:
        st.session_state.reassess_patient = {}

    if "patients" not in st.session_state:
        today = datetime.today()
        st.session_state.patients = [
            {"id": "PT-001", "name": "Grace Wanjiku", "age": 42, "county": "Nairobi",
             "facility": "Kenyatta National Hospital", "practitioner": "Nurse Achieng",
             "risk": "HIGH", "referral": "Urgent",
             "next_due": (today - timedelta(days=3)).strftime("%Y-%m-%d"),
             "status": "Overdue", "notes": "Palpable lump, nipple discharge",
             "journey": [
                 {"step": "Risk Assessment", "ts": (today - timedelta(days=10)).strftime("%d %b %Y"),
                  "detail": "Score 75 · HIGH RISK", "done": True},
                 {"step": "Screening Checklist", "ts": (today - timedelta(days=10)).strftime("%d %b %Y"),
                  "detail": "3 red flags detected", "done": True},
                 {"step": "Referral Generated", "ts": (today - timedelta(days=10)).strftime("%d %b %Y"),
                  "detail": "Urgent referral to oncology", "done": True},
                 {"step": "Follow-Up Due", "ts": (today - timedelta(days=3)).strftime("%d %b %Y"),
                  "detail": "Overdue — no response", "done": False, "urgent": True},
                 {"step": "Re-Assessment", "ts": "Pending", "detail": "Not yet done", "done": False},
             ]},
            {"id": "PT-002", "name": "Fatuma Hassan", "age": 35, "county": "Mombasa",
             "facility": "Coast General Hospital", "practitioner": "Dr. Mwenda",
             "risk": "MODERATE", "referral": "Imaging",
             "next_due": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
             "status": "Pending", "notes": "Family history positive",
             "journey": [
                 {"step": "Risk Assessment", "ts": (today - timedelta(days=5)).strftime("%d %b %Y"),
                  "detail": "Score 40 · MODERATE RISK", "done": True},
                 {"step": "Referral Generated", "ts": (today - timedelta(days=5)).strftime("%d %b %Y"),
                  "detail": "Imaging — mammogram ordered", "done": True},
                 {"step": "Follow-Up Due", "ts": (today + timedelta(days=2)).strftime("%d %b %Y"),
                  "detail": "Upcoming", "done": False},
             ]},
            {"id": "PT-003", "name": "Esther Chebet", "age": 28, "county": "Uasin Gishu",
             "facility": "Moi Teaching Hospital", "practitioner": "Clinical Officer Ruto",
             "risk": "LOW", "referral": "Education",
             "next_due": (today + timedelta(days=30)).strftime("%Y-%m-%d"),
             "status": "Scheduled", "notes": "Routine screening",
             "journey": [
                 {"step": "Risk Assessment", "ts": (today - timedelta(days=2)).strftime("%d %b %Y"),
                  "detail": "Score 10 · LOW RISK", "done": True},
                 {"step": "Education Provided", "ts": (today - timedelta(days=2)).strftime("%d %b %Y"),
                  "detail": "BSE demonstrated", "done": True},
                 {"step": "Follow-Up Due", "ts": (today + timedelta(days=30)).strftime("%d %b %Y"),
                  "detail": "Annual screening scheduled", "done": False},
             ]},
            {"id": "PT-004", "name": "Mary Auma", "age": 55, "county": "Kisumu",
             "facility": "Kisumu County Hospital", "practitioner": "Nurse Otieno",
             "risk": "HIGH", "referral": "Urgent",
             "next_due": (today - timedelta(days=7)).strftime("%Y-%m-%d"),
             "status": "Overdue", "notes": "Post-menopausal, skin changes",
             "journey": [
                 {"step": "Risk Assessment", "ts": (today - timedelta(days=14)).strftime("%d %b %Y"),
                  "detail": "Score 82 · HIGH RISK", "done": True},
                 {"step": "Screening Checklist", "ts": (today - timedelta(days=14)).strftime("%d %b %Y"),
                  "detail": "5 red flags detected", "done": True},
                 {"step": "Referral Generated", "ts": (today - timedelta(days=14)).strftime("%d %b %Y"),
                  "detail": "Urgent — called ahead", "done": True},
                 {"step": "Follow-Up Due", "ts": (today - timedelta(days=7)).strftime("%d %b %Y"),
                  "detail": "7 days overdue", "done": False, "urgent": True},
             ]},
            {"id": "PT-005", "name": "Jane Muthoni", "age": 48, "county": "Kiambu",
             "facility": "Thika Level 5", "practitioner": "Dr. Kamau",
             "risk": "MODERATE", "referral": "Routine",
             "next_due": (today + timedelta(days=14)).strftime("%Y-%m-%d"),
             "status": "Pending", "notes": "Asymmetric density on self-exam",
             "journey": [
                 {"step": "Risk Assessment", "ts": (today - timedelta(days=3)).strftime("%d %b %Y"),
                  "detail": "Score 30 · MODERATE RISK", "done": True},
                 {"step": "Follow-Up Due", "ts": (today + timedelta(days=14)).strftime("%d %b %Y"),
                  "detail": "Routine follow-up", "done": False},
             ]},
        ]

    if "screenings" not in st.session_state:
        counties = ["Nairobi", "Mombasa", "Kisumu", "Kiambu", "Nakuru", "Uasin Gishu", "Homa Bay"]
        facilities = ["Public Hospital", "Health Centre", "Private Hospital", "Dispensary", "Community"]
        professions = ["Nurse", "Clinical Officer", "Doctor/Medical Officer", "Midwife", "Community Health Worker"]
        random.seed(42)
        rows = []
        for _ in range(120):
            d = datetime.today() - timedelta(days=random.randint(0, 89))
            rows.append({
                "date": d.strftime("%Y-%m-%d"),
                "month": d.strftime("%b %Y"),
                "county": random.choice(counties),
                "facility": random.choice(facilities),
                "profession": random.choice(professions),
                "risk": random.choices(["HIGH", "MODERATE", "LOW"], weights=[15, 35, 50])[0],
                "referral": random.choices(["Urgent", "Imaging", "Routine", "Education"],
                                           weights=[12, 20, 30, 38])[0],
                "followed_up": random.choices([True, False], weights=[55, 45])[0],
            })
        st.session_state.screenings = pd.DataFrame(rows)

    if "_connectivity" not in st.session_state:
        try:
            import urllib.request
            urllib.request.urlopen("https://dns.google", timeout=2)
            st.session_state._connectivity = ("conn-online", "🟢 Online")
        except Exception:
            st.session_state._connectivity = ("conn-offline", "🟡 Offline — cached data active")


init_state()


def log_journey(patient_id, step, detail, done=True, urgent=False):
    for i, p in enumerate(st.session_state.patients):
        if p["id"] == patient_id:
            if "journey" not in st.session_state.patients[i]:
                st.session_state.patients[i]["journey"] = []
            st.session_state.patients[i]["journey"].append({
                "step": step, "ts": datetime.today().strftime("%d %b %Y"),
                "detail": detail, "done": done, "urgent": urgent,
            })


def compute_risk(lump, nipple_dc, skin_changes, nipple_invert, axillary,
                 ulceration, breast_pain, fam_hist, menopause, menarche,
                 parity, hrt, prev_biopsy, obesity, breastfed, age):
    s = 0
    if ulceration:  s += 40
    if axillary:    s += 30
    if skin_changes: s += 25
    if nipple_invert: s += 20
    if lump:         s += 20
    if nipple_dc:    s += 15
    if breast_pain:  s += 5
    if fam_hist == "2+ relatives or BRCA known": s += 25
    elif fam_hist == "1st-degree relative":       s += 15
    if menopause == "Post-menopausal (>5 yrs)":   s += 15
    elif menopause == "Post-menopausal (<5 yrs)":  s += 8
    if menarche == "<13 years (early)": s += 8
    if parity == "Nulliparous or first child ≥30": s += 8
    if hrt:        s += 8
    if prev_biopsy: s += 10
    if obesity:    s += 5
    if breastfed:  s -= 8
    if age >= 50:  s += 15
    elif age >= 40: s += 8
    elif age >= 35: s += 4
    if s >= 50 or ulceration or (lump and axillary) or (lump and skin_changes):
        risk = "HIGH"
    elif s >= 25:
        risk = "MODERATE"
    else:
        risk = "LOW"
    return min(s, 100), risk


def generate_handover(patient, risk, score, referral, red_flags, practitioner, county, facility):
    today_str = datetime.today().strftime("%d %B %Y %H:%M")
    rf_text = "\n".join([f"  • {f}" for f in red_flags]) if red_flags else "  • None identified"
    if referral == "Urgent":
        ref_instructions = "URGENT: Refer to oncology/surgical unit within 24 hours.\nCall facility ahead. Document in-charge notified."
    elif referral == "Imaging":
        ref_instructions = "IMAGING: Bilateral mammogram or ultrasound within 2 weeks.\nProvide written imaging request."
    elif referral == "Routine":
        ref_instructions = "ROUTINE: Reassess in 4-6 weeks. Educate on BSE."
    else:
        ref_instructions = "EDUCATION: BSE technique demonstrated. Annual screening scheduled."
    return f"""
═══════════════════════════════════════════════════════
  BREASTCARE KENYA — CLINICAL HANDOVER SUMMARY
  Generated: {today_str}
═══════════════════════════════════════════════════════

PATIENT         : {patient.get('name','—')}
AGE             : {patient.get('age','—')} years
COUNTY          : {county}
FACILITY        : {facility}
PRACTITIONER    : {practitioner}

───────────────────────────────────────────────────────
RISK ASSESSMENT
───────────────────────────────────────────────────────
Risk Score      : {score} / 100
Risk Level      : {risk}
Referral Action : {referral}

RED FLAGS IDENTIFIED:
{rf_text}

───────────────────────────────────────────────────────
REFERRAL INSTRUCTIONS
───────────────────────────────────────────────────────
{ref_instructions}

───────────────────────────────────────────────────────
DISCLAIMER
This is a clinical decision SUPPORT tool. All referral
and treatment decisions remain the responsibility of the
treating practitioner. Not a substitute for clinical
judgement.
═══════════════════════════════════════════════════════
    """.strip()


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

st.sidebar.markdown(f"""
<div style='text-align:center;padding:1.2rem 0 .6rem;'>
  <div style='font-size:2.4rem;'>🎗️</div>
  <div style='font-size:1.25rem;font-weight:900;color:#f3e5f5;letter-spacing:.01em;'>
    BreastCare Kenya</div>
  <div style='font-size:.76rem;color:#ce93d8;margin-top:.2rem;font-weight:600;'>
    Clinical Decision Support Platform</div>
</div>
<hr style='border-color:rgba(255,255,255,0.1);margin:.5rem 0 1rem;'>
""", unsafe_allow_html=True)

# Active patient banner
ap = st.session_state.active_patient
if ap.get("name"):
    rc = RED if ap.get("risk") == "HIGH" else AMBER if ap.get("risk") == "MODERATE" else GREEN
    st.sidebar.markdown(f"""
    <div style='background:rgba(255,255,255,0.07);border-radius:12px;padding:.85rem 1rem;
         margin-bottom:.9rem;border-left:3px solid {rc};'>
      <div style='font-size:.7rem;color:#ce93d8;font-weight:700;text-transform:uppercase;
           letter-spacing:.07em;'>Active Patient</div>
      <div style='font-weight:800;font-size:.95rem;color:#f3e5f5;margin-top:.25rem;'>
        👩🏾 {ap["name"]}</div>
      <div style='font-size:.77rem;color:#ce93d8;'>{ap.get("county","")} · {ap.get("facility","")}</div>
      <span style='background:{rc};color:white;border-radius:10px;padding:2px 9px;
           font-weight:700;font-size:.68rem;margin-top:.35rem;display:inline-block;'>
        {ap.get("risk","—")} RISK
      </span>
    </div>
    """, unsafe_allow_html=True)

nav_options = [
    "🏠 Home",
    "🩺 Risk Assessment",
    "✅ Screening Checklist",
    "🔀 Referral Intelligence",
    "🔔 Follow-Up Tracker",
    "📊 Analytics Dashboard",
    "🤖 CareBot",
]

module = st.sidebar.radio("", nav_options, index=st.session_state["_nav_idx"])
st.session_state["_nav_idx"] = nav_options.index(module)

st.sidebar.markdown("<hr style='border-color:rgba(255,255,255,0.1);margin:1rem 0;'>", unsafe_allow_html=True)

cc, ct = st.session_state._connectivity
st.sidebar.markdown(
    f"<div style='text-align:center;'><span class='conn-badge {cc}'>{ct}</span></div>",
    unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div class='about-badge' style='margin-top:.9rem;'>
  <strong style='color:#ff80ab;'>Built by Kerubo Bosire</strong><br>
  Build54 Hackathon · Solo builder<br>
  BSc Actuarial Science · JKUAT<br>
  KAP dataset: n=250 Kenyan practitioners<br>
  <br>
  <a href="https://github.com/kerubobosire254" style="color:#ff80ab;">
    github.com/kerubobosire254</a>
</div>
<div style='font-size:.72rem;color:#9e7dbc;text-align:center;margin-top:.8rem;line-height:1.8;'>
  Calibrated from Kenya KAP literature<br>2013–2024 · Synthetic demo data<br>
  <em>Not a substitute for clinical judgement</em>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 0 — HOME
# ══════════════════════════════════════════════════════════════════════════════

if "Home" in module:
    st.markdown(f"""
    <div class="hero">
      <h1>🎗️ BreastCare Kenya</h1>
      <p>A fully connected, offline-first clinical decision support platform for breast cancer
      screening — built for Kenyan frontline health practitioners.</p>
      <div class="kap-strip">
        <div class="kap-pill">🇰🇪 <span>78%</span> of patients present at Stage III or IV</div>
        <div class="kap-pill">📋 <span>250</span> practitioners surveyed</div>
        <div class="kap-pill">🏥 Practice score: <span>29.2%</span> — critical gap</div>
        <div class="kap-pill">🤖 <span>Zero</span> API keys needed</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KAP gap visualization
    col_kap, col_info = st.columns([1.2, 1])
    with col_kap:
        st.markdown("#### 📊 The KAP Gap — Why This App Exists")
        kap_data = {
            "Domain": ["🧠 Knowledge", "💬 Attitude", "🏥 Practice"],
            "Score": [54.7, 65.2, 29.2],
            "Category": ["Poor", "Neutral", "Critical"],
        }
        df_kap = pd.DataFrame(kap_data)
        fig_kap = go.Figure()
        colors = [PURPLE_MID, TEAL, RED]
        for i, row in df_kap.iterrows():
            fig_kap.add_trace(go.Bar(
                x=[row["Domain"]], y=[row["Score"]],
                name=row["Domain"],
                marker_color=colors[i],
                text=[f"{row['Score']}%"],
                textposition="outside",
                textfont=dict(size=16, color=colors[i]),
            ))
        # 36-point gap annotation
        fig_kap.add_shape(type="line", x0=-.5, x1=2.5, y0=65.2, y1=65.2,
                          line=dict(color=TEAL, width=1.5, dash="dot"))
        fig_kap.add_annotation(x=2, y=47, text="36-point<br>gap", showarrow=False,
                                font=dict(color=RED, size=13, family="Plus Jakarta Sans"),
                                bgcolor="rgba(198,40,40,0.08)", bordercolor=RED,
                                borderwidth=1, borderpad=5)
        fig_kap.update_layout(
            showlegend=False, template="plotly_white",
            yaxis=dict(range=[0, 85], title="Mean Score (%)", showgrid=True, gridcolor="#f0e6ff"),
            xaxis=dict(showgrid=False),
            margin=dict(t=10, b=10, l=0, r=0),
            font=dict(family="Plus Jakarta Sans"),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            height=300,
        )
        st.plotly_chart(fig_kap, use_container_width=True)
        st.markdown("""
        <div class='gcard pink' style='margin-top:-.4rem;'>
          <p>Practitioners <strong>know</strong> about breast cancer. They <strong>want</strong> to act.
          But practice scores are critically low — especially Community Health Workers (12.7%) and
          Nurses (27%). This is not a knowledge problem. It is a <strong>point-of-care support problem.</strong>
          <br><br>BreastCare Kenya closes this gap.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("#### 🔗 6 Connected Modules")
        modules_info = [
            ("🩺", "Risk Assessment", "Weighted score (0–100), risk level, red flags, follow-up date"),
            ("✅", "Screening Checklist", "5-step clinical workflow, symptoms pre-loaded from assessment"),
            ("🔀", "Referral Intelligence", "Evidence-weighted decision: Urgent / Imaging / Routine / Education"),
            ("🔔", "Follow-Up Tracker", "Auto-populated, journey timeline per patient, overdue alerts"),
            ("📊", "Analytics Dashboard", "Live data, county breakdown, referral trends, CSV export"),
            ("🤖", "CareBot", "Offline AI assistant — no API needed, rule-based clinical NLP"),
        ]
        for icon, name, desc in modules_info:
            st.markdown(f"""
            <div class='gcard' style='padding:.85rem 1.1rem;margin-bottom:.5rem;'>
              <div style='display:flex;gap:.7rem;align-items:flex-start;'>
                <span style='font-size:1.3rem;'>{icon}</span>
                <div>
                  <div style='font-weight:800;font-size:.92rem;color:{DARK};'>{name}</div>
                  <div style='font-size:.8rem;color:#666;margin-top:.15rem;'>{desc}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Overdue patients alert
    overdue = [p for p in st.session_state.patients
               if p.get("next_due", "9999") < datetime.today().strftime("%Y-%m-%d")
               and p.get("status") != "Done"]
    if overdue:
        st.markdown("---")
        st.markdown(f"#### 🚨 {len(overdue)} Overdue Patient(s) Need Attention")
        for p in overdue:
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.markdown(f"""
                <div class='gcard red' style='padding:.8rem 1rem;'>
                  <strong>{p['name']}</strong> · {p['county']} · {p['facility']}<br>
                  <span style='font-size:.82rem;color:#c62828;'>Due: {p['next_due']} · {p['referral']} referral</span>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("📋 View", key=f"home_view_{p['id']}"):
                    st.session_state["_nav_idx"] = nav_options.index("🔔 Follow-Up Tracker")
                    st.rerun()

    # Quick start CTA
    st.markdown("---")
    st.markdown("#### 🚀 Quick Start")
    qc1, qc2, qc3 = st.columns(3)
    with qc1:
        if st.button("🩺 New Assessment", use_container_width=True):
            st.session_state["_nav_idx"] = nav_options.index("🩺 Risk Assessment")
            st.session_state.grace_demo = False
            st.session_state.reassess_patient = {}
            st.rerun()
    with qc2:
        if st.button("🎬 Run Grace's Demo", use_container_width=True):
            st.session_state.grace_demo = True
            st.session_state["_nav_idx"] = nav_options.index("🩺 Risk Assessment")
            st.rerun()
    with qc3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state["_nav_idx"] = nav_options.index("📊 Analytics Dashboard")
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1 — RISK ASSESSMENT
# ══════════════════════════════════════════════════════════════════════════════

elif "Risk Assessment" in module:
    st.markdown('<div class="section-head">🩺 Quick Breast Cancer Risk Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Complete the form · Risk calculated instantly · Patient context flows to all modules</div>', unsafe_allow_html=True)

    reassess = st.session_state.get("reassess_patient", {})
    if reassess:
        st.markdown(f"""
        <div class="conn-flow">
          🔄 <span>Re-Assessment</span> — continuing care for
          <span>{reassess.get("name","")}</span> ·
          Previous risk: <span>{reassess.get("risk","")}</span>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🎬 Hackathon Demo — Follow Grace's Journey", expanded=st.session_state.grace_demo):
        st.markdown("""
        <div class="story-banner">
          <h4>👩🏾 Meet Grace Wanjiku — 42, Nairobi</h4>
          <p>A mother of three who almost ignored a lump she found three months ago.
          She was told "come back if it gets worse." Three months later she returned — Stage III.
          With BreastCare Kenya, that first visit flags HIGH RISK in under 2 minutes.</p>
        </div>
        """, unsafe_allow_html=True)
        ca, cb = st.columns(2)
        if ca.button("🚀 Pre-fill Grace's Case", use_container_width=True):
            st.session_state.grace_demo = True
            st.session_state.reassess_patient = {}
            st.rerun()
        if cb.button("🔄 Clear / New Patient", use_container_width=True):
            st.session_state.grace_demo = False
            st.session_state.reassess_patient = {}
            st.rerun()

    grace = st.session_state.grace_demo
    pf_name   = reassess.get("name",    "Grace Wanjiku" if grace else "")
    pf_age    = reassess.get("age",     42 if grace else 40)
    pf_county = reassess.get("county",  "Nairobi")
    pf_fac    = reassess.get("facility","Health Centre")
    pf_prac   = reassess.get("practitioner", "Nurse Achieng" if grace else "")

    if grace and not reassess:
        st.info("👩🏾 **Grace's case loaded.** Review and click Calculate Risk.")

    with st.form("risk_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Patient Information**")
            p_name = st.text_input("Patient Name", value=pf_name, placeholder="e.g. Grace Wanjiku")
            p_age  = st.number_input("Age (years)", 18, 90, value=int(pf_age))
            counties_list = ["Nairobi","Mombasa","Kisumu","Kiambu","Nakuru","Uasin Gishu","Homa Bay","Other"]
            fac_list      = ["Public Hospital","Health Centre","Private Hospital","Dispensary","Community"]
            ci = counties_list.index(pf_county) if pf_county in counties_list else 0
            fi = fac_list.index(pf_fac) if pf_fac in fac_list else 0
            p_county   = st.selectbox("County", counties_list, index=ci)
            p_facility = st.selectbox("Facility", fac_list, index=fi)
            practitioner = st.text_input("Practitioner Name", value=pf_prac, placeholder="Your name")

        with c2:
            st.markdown("**Symptoms & Signs**")
            lump         = st.checkbox("Palpable breast lump",             value=True if grace else False)
            nipple_dc    = st.checkbox("Nipple discharge (non-milk)",      value=True if grace else False)
            skin_changes = st.checkbox("Skin changes (peau d'orange, dimpling)", value=False)
            nipple_invert= st.checkbox("Nipple inversion / retraction",   value=False)
            axillary     = st.checkbox("Axillary lymph node enlargement", value=True if grace else False)
            breast_pain  = st.checkbox("Persistent unexplained breast pain", value=True if grace else False)
            ulceration   = st.checkbox("Ulceration / open wound on breast", value=False)

        with c3:
            st.markdown("**Risk Factors**")
            fam_hist  = st.selectbox("Family history",
                                     ["None","1st-degree relative","2+ relatives or BRCA known"],
                                     index=1 if grace else 0)
            menarche  = st.selectbox("Age at first period", ["≥13 years (normal)","<13 years (early)"])
            menopause = st.selectbox("Menopausal status",
                                     ["Pre-menopausal","Post-menopausal (<5 yrs)","Post-menopausal (>5 yrs)"])
            parity    = st.selectbox("Parity", ["Parous, first child <30","Nulliparous or first child ≥30"])
            breastfed = st.checkbox("Breastfed ≥1 year (protective)", value=True if grace else False)
            hrt       = st.checkbox("Current HRT / OCP use (>5 yrs)", value=False)
            prev_biopsy = st.checkbox("Previous abnormal breast biopsy", value=False)
            obesity   = st.checkbox("BMI ≥30 / obesity", value=False)

        submitted = st.form_submit_button("🔍 Calculate Risk & Generate Recommendation",
                                          use_container_width=True)

    if submitted:
        score, risk = compute_risk(
            lump, nipple_dc, skin_changes, nipple_invert, axillary, ulceration,
            breast_pain, fam_hist, menopause, menarche, parity, hrt,
            prev_biopsy, obesity, breastfed, p_age
        )
        if risk == "HIGH":
            referral   = "Urgent"
            ref_action = "Refer IMMEDIATELY to oncology/surgical unit. Do not delay. Document and call ahead."
            ref_class  = "red"
        elif risk == "MODERATE":
            referral   = "Imaging" if (lump or axillary) else "Routine"
            ref_action = ("Order mammogram/ultrasound within 2 weeks."
                          if referral == "Imaging" else "Follow-up in 4–6 weeks. Educate on BSE.")
            ref_class  = "orange"
        else:
            referral   = "Education"
            ref_action = "Provide BSE education. Schedule annual screening."
            ref_class  = "green"

        red_flags = [s for s, v in {
            "Palpable lump": lump, "Nipple discharge": nipple_dc,
            "Skin changes": skin_changes, "Nipple inversion": nipple_invert,
            "Axillary nodes": axillary, "Ulceration": ulceration,
        }.items() if v]

        next_due = (datetime.today() + timedelta(
            days=1 if risk=="HIGH" else 14 if risk=="MODERATE" else 365
        )).strftime("%Y-%m-%d")

        # ── Write to session state ──
        st.session_state.active_patient = {
            "name": p_name, "age": p_age, "county": p_county,
            "facility": p_facility, "practitioner": practitioner,
            "risk": risk, "score": score, "referral": referral,
        }
        st.session_state.assessment_red_flags = red_flags
        st.session_state.assessment_context = {
            "risk": risk, "score": score, "fam_hist": fam_hist,
            "menopause": menopause,
            "age_group": "50+" if p_age >= 50 else "35–49" if p_age >= 35 else "<35",
            "post_meno": menopause != "Pre-menopausal",
        }
        st.session_state.checklist_symptoms = {
            "lump": lump, "nipple_dc": nipple_dc, "skin_changes": skin_changes,
            "nipple_invert": nipple_invert, "axillary": axillary,
            "ulceration": ulceration, "breast_pain": breast_pain, "asymmetry": False,
        }
        st.session_state.checklist_step = 1

        # ── Results ──
        st.markdown("---")
        st.markdown("### 📋 Assessment Result")

        sc_color = RED if risk=="HIGH" else AMBER if risk=="MODERATE" else GREEN
        ri_icon  = "🚨" if referral=="Urgent" else "🖼️" if referral=="Imaging" else "📅" if referral=="Routine" else "📚"

        rc1, rc2 = st.columns([1, 2])
        with rc1:
            # Score gauge
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={"x": [0,1], "y": [0,1]},
                number={"font": {"size": 42, "family": "Plus Jakarta Sans", "color": sc_color}},
                gauge={
                    "axis": {"range": [0,100], "tickfont": {"size":10}},
                    "bar": {"color": sc_color},
                    "steps": [
                        {"range": [0,25],  "color": "#e8f5e9"},
                        {"range": [25,50], "color": "#fff3e0"},
                        {"range": [50,100],"color": "#ffebee"},
                    ],
                    "threshold": {"line": {"color": sc_color, "width": 4},
                                  "thickness": .85, "value": score},
                }
            ))
            fig_g.update_layout(height=220, margin=dict(t=10,b=10,l=10,r=10),
                                 paper_bgcolor="rgba(0,0,0,0)",
                                 font=dict(family="Plus Jakarta Sans"))
            st.plotly_chart(fig_g, use_container_width=True)

            st.markdown(f"""
            <div class="gcard {ref_class}" style='text-align:center;'>
              <span class='risk-badge risk-{risk}'>{risk} RISK</span><br><br>
              <div class='ref-banner ref-{referral}'>{ri_icon} {referral} Referral</div>
            </div>
            """, unsafe_allow_html=True)

        with rc2:
            st.markdown(f"""
            <div class="gcard blue">
              <h3>Recommended Action</h3>
              <p style='font-size:1rem;color:#0d47a1;font-weight:700;'>{ref_action}</p>
              <p style='margin-top:.6rem;'>Practitioner: <strong>{practitioner or 'Not recorded'}</strong> ·
              Follow-up due: <strong>{next_due}</strong></p>
            </div>
            """, unsafe_allow_html=True)

            if red_flags:
                fl_html = "".join([f"<li style='margin:.3rem 0;'>⚠️ {f}</li>" for f in red_flags])
                st.markdown(f"""
                <div class="gcard red">
                  <h3>🚩 Red Flags Detected ({len(red_flags)})</h3>
                  <ul style='margin:.4rem 0 0;padding-left:1.2rem;'>{fl_html}</ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="gcard green"><h3>✅ No Red Flags Identified</h3>
                <p>Continue with standard screening pathway.</p></div>
                """, unsafe_allow_html=True)

            # Handover summary
            with st.expander("📄 Generate Clinical Handover Summary"):
                ho_text = generate_handover(
                    st.session_state.active_patient, risk, score,
                    referral, red_flags, practitioner, p_county, p_facility
                )
                st.markdown(f"<div class='handover'>{ho_text}</div>", unsafe_allow_html=True)
                st.download_button("⬇️ Download Handover (.txt)",
                                   ho_text, file_name=f"handover_{p_name.replace(' ','_')}.txt",
                                   mime="text/plain")

        # Save patient
        if p_name:
            pid = f"PT-{len(st.session_state.patients)+1:03d}"
            st.session_state.patients.append({
                "id": pid, "name": p_name, "age": p_age, "county": p_county,
                "facility": p_facility, "practitioner": practitioner,
                "risk": risk, "referral": referral, "next_due": next_due,
                "status": "Urgent" if risk=="HIGH" else "Pending",
                "notes": ", ".join(red_flags) if red_flags else "No red flags",
                "journey": [{
                    "step": "Risk Assessment",
                    "ts": datetime.today().strftime("%d %b %Y"),
                    "detail": f"Score {score} · {risk} RISK",
                    "done": True, "urgent": risk == "HIGH",
                }],
            })
            st.session_state.active_patient["id"] = pid
            st.session_state.screenings = pd.concat([
                st.session_state.screenings,
                pd.DataFrame([{
                    "date": datetime.today().strftime("%Y-%m-%d"),
                    "month": datetime.today().strftime("%b %Y"),
                    "county": p_county, "facility": p_facility,
                    "profession": practitioner or "Unknown",
                    "risk": risk, "referral": referral, "followed_up": False,
                }])
            ], ignore_index=True)

        st.markdown("""
        <div class="conn-flow">
          ✅ Assessment complete. <span>Next:</span> Proceed to Screening Checklist —
          symptoms are already filled in for this patient.
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"➡️ Continue to Screening Checklist for {p_name or 'Patient'}",
                     use_container_width=True):
            st.session_state["_nav_idx"] = nav_options.index("✅ Screening Checklist")
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2 — SCREENING CHECKLIST
# ══════════════════════════════════════════════════════════════════════════════

elif "Screening Checklist" in module:
    st.markdown('<div class="section-head">✅ Guided Screening Checklist</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Step-by-step workflow · Symptoms pre-filled from Risk Assessment · Red flags auto-detected</div>', unsafe_allow_html=True)

    ap = st.session_state.active_patient
    if ap.get("name"):
        st.markdown(f"""
        <div class="conn-flow">
          🔗 <span>Connected from Risk Assessment</span> —
          examining <span>{ap["name"]}</span> ·
          Risk: <span>{ap.get("risk","—")}</span> · Symptoms pre-loaded
        </div>
        """, unsafe_allow_html=True)

    cs = st.session_state.checklist_symptoms
    rf_from_assessment = st.session_state.assessment_red_flags

    steps = {
        1: ("📋 History Taking", [
            "Chief complaint documented",
            "Duration of symptoms recorded",
            "Previous breast conditions / biopsies noted",
            "Menstrual & reproductive history taken",
            "Family history (1st & 2nd degree) documented",
            "Medication history (HRT, OCP) reviewed",
            "Alcohol / smoking history noted",
        ]),
        2: ("👁️ Visual Inspection", [
            "Breast symmetry assessed — note asymmetry",
            "Skin surface checked: peau d'orange, dimpling",
            "Nipple position & symmetry checked",
            "Areola colour changes noted",
            "Visible lump or contour change observed",
            "Arms raised — repeat inspection",
            "Hands on hips (pectoral contraction) — repeat",
        ]),
        3: ("🖐️ Palpation (patient supine)", [
            "Systematic pattern chosen (spiral / radial / grid)",
            "All 4 quadrants palpated with 3-finger technique",
            "Tail of Spence (axillary extension) palpated",
            "Areola & nipple gently compressed",
            "Nipple discharge — colour & consistency noted",
            "Lump characteristics: size, shape, mobility, tenderness",
        ]),
        4: ("🔍 Lymph Node Examination", [
            "Axillary nodes — anterior, posterior, medial",
            "Supraclavicular nodes palpated",
            "Infraclavicular nodes palpated",
            "Node size, consistency, mobility noted",
            "Bilateral comparison performed",
        ]),
        5: ("🚩 Red Flag Detection & Decision", [
            "Hard, irregular, fixed lump present?",
            "Skin tethering or dimpling present?",
            "Bloody or spontaneous nipple discharge?",
            "Nipple retraction (new)?",
            "Axillary nodes enlarged / fixed?",
            "Ulceration or skin breakdown?",
            "Post-menopausal patient with any lump?",
        ]),
    }

    flag_map = {
        0: cs.get("lump", False),
        2: cs.get("skin_changes", False),
        3: cs.get("nipple_invert", False),
        4: cs.get("axillary", False),
        5: cs.get("ulceration", False),
    }

    step = st.session_state.checklist_step
    cp, cm, cn = st.columns([1, 4, 1])
    with cp:
        if st.button("← Back") and step > 1:
            st.session_state.checklist_step -= 1
            st.rerun()
    with cm:
        st.progress(step / len(steps))
        st.markdown(f"**Step {step} of {len(steps)}**")
    with cn:
        if st.button("Next →") and step < len(steps):
            st.session_state.checklist_step += 1
            st.rerun()

    title, items = steps[step]
    st.markdown(f"### {title}")

    if step == 5 and rf_from_assessment:
        st.info(f"🔗 **Pre-highlighted from Risk Assessment:** {', '.join(rf_from_assessment)}")

    checked = []
    for i, item in enumerate(items):
        pre = flag_map.get(i, False) if step == 5 else False
        val = st.checkbox(item, value=pre, key=f"chk_{step}_{i}")
        is_flag = (step == 5)
        css  = "check-item flag" if (is_flag and val) else "check-item"
        icon = "🚩" if (is_flag and val) else "✔️" if val else "○"
        st.markdown(f'<div class="{css}">{icon} {item}</div>', unsafe_allow_html=True)
        checked.append(val)

    st.markdown(f"<br>**{sum(checked)}/{len(items)} items completed**", unsafe_allow_html=True)

    tips = {
        1: "💡 Ensure patient privacy and explain each step before proceeding.",
        2: "💡 Adequate lighting essential. Ask patient to disrobe to waist.",
        3: "💡 Use pads of fingers — not tips. Apply light, medium, and firm pressure.",
        4: "💡 Stand on same side as axilla. Support patient's arm throughout.",
        5: "💡 Red flags must be documented and acted on immediately.",
    }
    st.info(tips[step])

    if step == 5:
        rf_count = sum(checked)
        if rf_count >= 3:
            st.error(f"🚨 **{rf_count} red flags — URGENT REFERRAL required.**")
        elif rf_count >= 1:
            st.warning(f"⚠️ **{rf_count} red flag(s) — imaging within 2 weeks.**")
        else:
            st.success("✅ No red flags — educate on BSE and schedule annual follow-up.")

        st.markdown("""
        <div class="conn-flow">
          🔗 Checklist complete. <span>Symptoms auto-filled</span> in Referral Intelligence.
          One click to generate the referral decision.
        </div>
        """, unsafe_allow_html=True)

        if ap.get("id"):
            log_journey(ap["id"], "Screening Checklist",
                        f"{rf_count} red flag(s) detected", done=True, urgent=rf_count >= 3)

        if st.button("➡️ Continue to Referral Intelligence", use_container_width=True):
            st.session_state["_nav_idx"] = nav_options.index("🔀 Referral Intelligence")
            st.rerun()

    if st.button("🔄 Restart Checklist"):
        st.session_state.checklist_step = 1
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 3 — REFERRAL INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════

elif "Referral" in module:
    st.markdown('<div class="section-head">🔀 Referral Intelligence Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Symptoms auto-filled from Screening Checklist · Evidence-based referral decision · Kenya MOH pathway</div>', unsafe_allow_html=True)

    ap  = st.session_state.active_patient
    cs  = st.session_state.checklist_symptoms
    ctx = st.session_state.assessment_context

    if ap.get("name"):
        st.markdown(f"""
        <div class="conn-flow">
          🔗 <span>Connected from Screening Checklist</span> —
          generating referral for <span>{ap["name"]}</span> · Risk context carried forward
        </div>
        """, unsafe_allow_html=True)

    rc1, rc2 = st.columns(2)
    with rc1:
        st.markdown("**Clinical Signs** *(pre-filled from Screening Checklist)*")
        s_lump     = st.checkbox("🔴 Palpable breast lump",        value=cs.get("lump",     False))
        s_axillary = st.checkbox("🔴 Axillary lymphadenopathy",    value=cs.get("axillary", False))
        s_skin     = st.checkbox("🟠 Skin changes / dimpling",     value=cs.get("skin_changes", False))
        s_nipple_i = st.checkbox("🟠 Nipple inversion (new)",      value=cs.get("nipple_invert", False))
        s_nipple_d = st.checkbox("🟠 Nipple discharge (non-milk)", value=cs.get("nipple_dc", False))
        s_ulcer    = st.checkbox("🔴 Ulceration / wound on breast",value=cs.get("ulceration", False))
        s_pain     = st.checkbox("🟡 Breast pain (persistent)",    value=cs.get("breast_pain", False))
        s_asymm    = st.checkbox("🟡 Breast asymmetry (new)",      value=cs.get("asymmetry", False))

    with rc2:
        st.markdown("**Patient Context** *(carried from Risk Assessment)*")
        age_options = ["<35 years", "35–49 years", "50+ years"]
        age_default = age_options.index(ctx["age_group"]) if ctx.get("age_group") in age_options else 0
        age_grp  = st.selectbox("Age group", age_options, index=age_default)
        fhx_opts = ["None", "1st-degree relative", "Strong / BRCA"]
        fhx_map  = {"None": 0, "1st-degree relative": 1, "2+ relatives or BRCA known": 2}
        fhx_def  = fhx_map.get(ctx.get("fam_hist", "None"), 0)
        fhx      = st.selectbox("Family history", fhx_opts, index=min(fhx_def, 2))
        prev_ca  = st.checkbox("Personal history of any cancer")
        post_meno= st.checkbox("Post-menopausal", value=ctx.get("post_meno", False))
        rapid_chg= st.checkbox("Rapid change in size / appearance")

    if st.button("🔀 Generate Referral Decision", use_container_width=True):
        u, img, r, e = 0, 0, 0, 0
        if s_lump:     u += 3; img += 2
        if s_axillary: u += 4
        if s_ulcer:    u += 5
        if s_skin:     u += 3; img += 2
        if s_nipple_i: u += 2; img += 2
        if s_nipple_d: u += 1; img += 3
        if rapid_chg:  u += 2
        if prev_ca:    u += 3
        if fhx == "Strong / BRCA":      u += 2; img += 2
        elif fhx == "1st-degree relative": img += 2; r += 1
        if post_meno and s_lump: u += 2
        if age_grp == "50+ years": img += 1
        if s_pain and not s_lump: r += 2; e += 1
        if s_asymm and not s_lump: img += 1; r += 1
        if not any([s_lump, s_axillary, s_skin, s_nipple_i, s_nipple_d, s_ulcer]): e += 3

        scores   = {"Urgent": u, "Imaging": img, "Routine": r, "Education": e}
        decision = max(scores, key=scores.get)

        ref_details = {
            "Urgent": ("🚨", RED, "Refer within 24 hours to oncology/surgical unit.",
                       ["Contact facility before sending patient",
                        "Provide written referral letter",
                        "Ensure patient has transport support",
                        "Document and notify in-charge"]),
            "Imaging": ("🖼️", BLUE, "Mammogram and/or ultrasound within 2 weeks.",
                        ["Bilateral mammogram if ≥40 years",
                         "Ultrasound if <40 or dense breasts",
                         "Provide written imaging request",
                         "Book follow-up to review results"]),
            "Routine": ("📅", AMBER, "Reassess within 4–6 weeks.",
                        ["Educate patient on BSE",
                         "Document current findings",
                         "Book follow-up before patient leaves",
                         "Advise return if symptoms worsen"]),
            "Education": ("📚", GREEN, "No acute clinical concern identified.",
                          ["Demonstrate BSE technique",
                           "Provide take-home BSE card",
                           "Discuss annual screening schedule",
                           "Advise on risk reduction"]),
        }
        icon, clr, headline, actions = ref_details[decision]
        next_due = (datetime.today() + timedelta(
            days=1 if decision=="Urgent" else 14 if decision=="Imaging" else 42 if decision=="Routine" else 365
        )).strftime("%Y-%m-%d")

        actions_html = "".join([f"<li style='margin:.4rem 0;'>{a}</li>" for a in actions])
        st.markdown("---")
        st.markdown(f"""
        <div class="ref-banner ref-{decision}">
          <div style='font-size:1.8rem;'>{icon}</div>
          <div style='font-size:1.35rem;font-weight:900;margin:.2rem 0;'>{decision} Referral</div>
          <div style='font-size:.95rem;opacity:.92;'>{headline}</div>
        </div>
        """, unsafe_allow_html=True)

        act_col, chart_col = st.columns([1, 1])
        with act_col:
            st.markdown(f"""
            <div class="gcard">
              <h3>📋 Action Steps</h3>
              <ul style='margin:.4rem 0;padding-left:1.3rem;font-size:.92rem;color:#333;'>
                {actions_html}
              </ul>
            </div>
            """, unsafe_allow_html=True)

        with chart_col:
            fig_s = px.bar(
                x=list(scores.keys()), y=list(scores.values()),
                color=list(scores.keys()),
                color_discrete_map={"Urgent": RED, "Imaging": BLUE, "Routine": AMBER, "Education": GREEN},
                template="plotly_white",
                labels={"x": "Decision", "y": "Evidence Score"},
                title="Evidence weighting"
            )
            fig_s.update_layout(showlegend=False, font_family="Plus Jakarta Sans",
                                 margin=dict(t=40,b=0,l=0,r=0), height=220,
                                 plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_s, use_container_width=True)

        if decision in ["Urgent", "Imaging"]:
            st.warning("⚠️ **KAP gap alert:** Only 12–20% of cases meeting urgent criteria in Kenya are actually referred. This patient meets the threshold — please act.")

        # Save referral
        st.session_state.last_referral = {
            "decision": decision, "next_due": next_due,
            "patient": ap.get("name", "Unknown"),
            "patient_id": ap.get("id", ""),
            "risk": ap.get("risk", "MODERATE"),
            "county": ap.get("county", ""),
            "facility": ap.get("facility", ""),
            "practitioner": ap.get("practitioner", ""),
            "age": ap.get("age", 0),
        }
        if ap.get("id"):
            log_journey(ap["id"], "Referral Generated",
                        f"{decision} referral · due {next_due}",
                        done=True, urgent=decision == "Urgent")

        st.markdown("""
        <div class="conn-flow">
          🔗 Referral generated. <span>One click</span> to save to Follow-Up Tracker.
        </div>
        """, unsafe_allow_html=True)

        pat_name = ap.get("name", "Patient")
        if st.button(f"➡️ Save Referral & Create Follow-Up for {pat_name}", use_container_width=True):
            lr = st.session_state.last_referral
            found = False
            for i, p in enumerate(st.session_state.patients):
                if p["id"] == lr["patient_id"]:
                    st.session_state.patients[i]["referral"]  = lr["decision"]
                    st.session_state.patients[i]["next_due"]  = lr["next_due"]
                    st.session_state.patients[i]["status"]    = "Urgent" if lr["decision"]=="Urgent" else "Pending"
                    found = True
            if not found and lr["patient"]:
                st.session_state.patients.append({
                    "id": f"PT-{len(st.session_state.patients)+1:03d}",
                    "name": lr["patient"], "age": lr["age"],
                    "county": lr["county"], "facility": lr["facility"],
                    "practitioner": lr["practitioner"], "risk": lr["risk"],
                    "referral": lr["decision"], "next_due": lr["next_due"],
                    "status": "Urgent" if lr["decision"]=="Urgent" else "Pending",
                    "notes": "Auto-saved from Referral Intelligence",
                    "journey": [{"step": "Referral Generated",
                                  "ts": datetime.today().strftime("%d %b %Y"),
                                  "detail": f"{lr['decision']} · due {lr['next_due']}",
                                  "done": True}],
                })
            st.success(f"✅ Referral saved. {lr['patient']} is now in the Follow-Up Tracker.")
            st.session_state["_nav_idx"] = nav_options.index("🔔 Follow-Up Tracker")
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 4 — FOLLOW-UP TRACKER
# ══════════════════════════════════════════════════════════════════════════════

elif "Follow-Up" in module:
    st.markdown('<div class="section-head">🔔 Smart Follow-Up Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">All patients from Risk Assessment appear here · Overdue auto-detected · Full journey timeline per patient</div>', unsafe_allow_html=True)

    today = datetime.today().strftime("%Y-%m-%d")

    def auto_status(row):
        if row["next_due"] < today and row.get("status") not in ("Done",):
            return "Overdue"
        return row.get("status", "Pending")

    patients = st.session_state.patients.copy()
    for p in patients:
        p["status"] = auto_status(p)

    # Summary tiles
    total    = len(patients)
    overdue  = sum(1 for p in patients if p["status"] == "Overdue")
    high_r   = sum(1 for p in patients if p["risk"] == "HIGH")
    done_cnt = sum(1 for p in patients if p["status"] == "Done")

    st.markdown(f"""
    <div class="metric-row">
      <div class="mtile"><h2>{total}</h2><p>Total Patients</p></div>
      <div class="mtile t5"><h2 style="color:{RED};">{overdue}</h2><p>Overdue</p></div>
      <div class="mtile t4"><h2 style="color:{AMBER};">{high_r}</h2><p>High Risk</p></div>
      <div class="mtile t3"><h2 style="color:{GREEN};">{done_cnt}</h2><p>Completed</p></div>
    </div>
    """, unsafe_allow_html=True)

    # Filters
    fc1, fc2, fc3 = st.columns(3)
    f_status = fc1.selectbox("Filter by Status", ["All","Overdue","Pending","Scheduled","Done","Urgent"])
    f_risk   = fc2.selectbox("Filter by Risk",   ["All","HIGH","MODERATE","LOW"])
    f_county = fc3.selectbox("Filter by County", ["All"] + sorted(set(p["county"] for p in patients)))

    filtered = [p for p in patients
                if (f_status == "All" or p["status"] == f_status)
                and (f_risk   == "All" or p["risk"]   == f_risk)
                and (f_county == "All" or p["county"] == f_county)]

    st.markdown(f"**{len(filtered)} patient(s) shown**")
    st.markdown("---")

    for p in filtered:
        stat_col = RED if p["status"] == "Overdue" else AMBER if p["status"] == "Urgent" else \
                   GREEN if p["status"] == "Done" else "#888"
        risk_col = RED if p["risk"] == "HIGH" else AMBER if p["risk"] == "MODERATE" else GREEN

        status_icon = "🚨" if p["status"] in ("Overdue", "Urgent") else "✅" if p["status"] == "Done" else "🔔"
        status_label = "OVERDUE" if p["status"] == "Overdue" else p["status"]
        expander_label = f"{p['name']}  ·  {p['county']}  ·  {status_icon} {status_label}"
        with st.expander(expander_label):
            col_info, col_journey = st.columns([1, 1.2])

            with col_info:
                st.markdown(f"""
                <div class="gcard" style='padding:.9rem 1.1rem;'>
                  <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div>
                      <div style='font-weight:800;font-size:1rem;color:{DARK};'>{p["name"]}</div>
                      <div style='font-size:.82rem;color:#666;margin-top:.2rem;'>
                        Age {p["age"]} · {p["county"]} · {p["facility"]}</div>
                      <div style='font-size:.8rem;color:#666;'>{p.get("practitioner","—")}</div>
                    </div>
                    <span class='risk-badge risk-{p["risk"]}'>{p["risk"]}</span>
                  </div>
                  <div style='margin-top:.7rem;font-size:.82rem;'>
                    <span style='background:{stat_col};color:white;border-radius:8px;
                         padding:3px 10px;font-weight:700;'>{p["status"]}</span>
                    &nbsp; Referral: <strong>{p["referral"]}</strong>
                    &nbsp; Due: <strong>{p["next_due"]}</strong>
                  </div>
                  <div style='margin-top:.5rem;font-size:.8rem;color:#777;'>
                    📝 {p.get("notes","—")}</div>
                </div>
                """, unsafe_allow_html=True)

                # Actions
                a1, a2, a3 = st.columns(3)
                pid = p["id"]
                if a1.button("✅ Mark Done", key=f"done_{pid}"):
                    for i, pt in enumerate(st.session_state.patients):
                        if pt["id"] == pid:
                            st.session_state.patients[i]["status"] = "Done"
                    st.rerun()
                if a2.button("📅 +2 Weeks", key=f"resc_{pid}"):
                    for i, pt in enumerate(st.session_state.patients):
                        if pt["id"] == pid:
                            nd = datetime.strptime(pt["next_due"], "%Y-%m-%d") + timedelta(weeks=2)
                            st.session_state.patients[i]["next_due"] = nd.strftime("%Y-%m-%d")
                    st.rerun()
                if a3.button("🚨 Flag Urgent", key=f"urg_{pid}"):
                    for i, pt in enumerate(st.session_state.patients):
                        if pt["id"] == pid:
                            st.session_state.patients[i]["status"] = "Urgent"
                    st.rerun()

                if st.button("🔄 Start Re-Assessment", key=f"reass_{pid}", use_container_width=True):
                    st.session_state.reassess_patient = {
                        "name": p["name"], "age": p["age"], "county": p["county"],
                        "facility": p["facility"], "practitioner": p.get("practitioner",""),
                        "risk": p["risk"], "last_seen": p["next_due"],
                    }
                    st.session_state.grace_demo = False
                    st.session_state["_nav_idx"] = nav_options.index("🩺 Risk Assessment")
                    st.rerun()

            with col_journey:
                st.markdown("**Patient Journey Timeline**")
                journey = p.get("journey", [])
                if journey:
                    st.markdown('<div class="tl-wrap">', unsafe_allow_html=True)
                    for step in journey:
                        dot_cls = ("tl-urgent" if step.get("urgent") else
                                   "tl-done" if step.get("done") else
                                   "tl-pending")
                        st.markdown(f"""
                        <div class="tl-step">
                          <div class="tl-dot {dot_cls}"></div>
                          <div>
                            <div class="tl-label">{step["step"]}</div>
                            <div class="tl-sub">{step["ts"]} · {step["detail"]}</div>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.caption("No journey events recorded.")

    # Manual add
    st.markdown("---")
    with st.expander("➕ Add Patient Manually"):
        with st.form("manual_add"):
            mc1, mc2, mc3 = st.columns(3)
            m_name    = mc1.text_input("Patient Name")
            m_age     = mc2.number_input("Age", 18, 90, 35)
            m_county  = mc3.selectbox("County",
                           ["Nairobi","Mombasa","Kisumu","Kiambu","Nakuru","Uasin Gishu","Homa Bay","Other"])
            m_risk    = mc1.selectbox("Risk Level", ["HIGH","MODERATE","LOW"])
            m_ref     = mc2.selectbox("Referral", ["Urgent","Imaging","Routine","Education"])
            m_due     = mc3.text_input("Due Date (YYYY-MM-DD)", datetime.today().strftime("%Y-%m-%d"))
            m_notes   = st.text_area("Notes", height=60)
            if st.form_submit_button("Add Patient", use_container_width=True):
                st.session_state.patients.append({
                    "id": f"PT-{len(st.session_state.patients)+1:03d}",
                    "name": m_name or "Unknown", "age": m_age, "county": m_county,
                    "facility": "Manually added", "practitioner": "—",
                    "risk": m_risk, "referral": m_ref, "next_due": m_due,
                    "status": "Pending", "notes": m_notes,
                    "journey": [{"step": "Added manually",
                                  "ts": datetime.today().strftime("%d %b %Y"),
                                  "detail": f"{m_risk} risk · {m_ref}",
                                  "done": True}],
                })
                st.success(f"✅ {m_name or 'Patient'} added to tracker.")
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 5 — ANALYTICS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

elif "Analytics" in module:
    st.markdown('<div class="section-head">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Live from session data · KAP insights · County breakdown · Referral trends</div>', unsafe_allow_html=True)

    df = st.session_state.screenings.copy()
    total_s  = len(df)
    high_s   = (df["risk"] == "HIGH").sum()
    urgent_s = (df["referral"] == "Urgent").sum()
    fu_rate  = int(df["followed_up"].mean() * 100)

    # New this session
    today_str = datetime.today().strftime("%Y-%m-%d")
    new_today = (df["date"] == today_str).sum()
    if new_today:
        st.success(f"🎉 **{new_today} new screening(s)** added in this session — charts updated in real time.")

    st.markdown(f"""
    <div class="metric-row">
      <div class="mtile"><h2>{total_s}</h2><p>Total Screenings</p></div>
      <div class="mtile t5"><h2 style="color:{RED};">{high_s}</h2><p>High Risk Cases</p></div>
      <div class="mtile t4"><h2 style="color:{AMBER};">{urgent_s}</h2><p>Urgent Referrals</p></div>
      <div class="mtile t3"><h2 style="color:{GREEN};">{fu_rate}%</h2><p>Follow-Up Rate</p></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🗺️ By County", "👩‍⚕️ By Profession", "📋 KAP Insights"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            trend = df.groupby("month").size().reset_index(name="Screenings")
            fig_t = px.line(trend, x="month", y="Screenings",
                            title="Screenings Over Time",
                            markers=True, template="plotly_white",
                            color_discrete_sequence=[PINK])
            fig_t.update_layout(font_family="Plus Jakarta Sans", margin=dict(t=40,b=0,l=0,r=0),
                                  plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_t, use_container_width=True)
        with col2:
            risk_c = df["risk"].value_counts().reset_index()
            risk_c.columns = ["Risk","Count"]
            fig_r = px.pie(risk_c, values="Count", names="Risk",
                           color="Risk",
                           color_discrete_map={"HIGH": RED, "MODERATE": AMBER, "LOW": GREEN},
                           title="Risk Distribution", template="plotly_white",
                           hole=.45)
            fig_r.update_layout(font_family="Plus Jakarta Sans",
                                  margin=dict(t=40,b=0,l=0,r=0),
                                  paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_r, use_container_width=True)

        # Referral breakdown
        ref_c = df["referral"].value_counts().reset_index()
        ref_c.columns = ["Referral", "Count"]
        fig_ref = px.bar(ref_c, x="Referral", y="Count",
                         color="Referral",
                         color_discrete_map={"Urgent": RED, "Imaging": BLUE,
                                              "Routine": AMBER, "Education": GREEN},
                         template="plotly_white", title="Referral Decisions")
        fig_ref.update_layout(showlegend=False, font_family="Plus Jakarta Sans",
                               margin=dict(t=40,b=0,l=0,r=0),
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_ref, use_container_width=True)

    with tab2:
        cnt_df = df.groupby("county").agg(
            Screenings=("risk","count"),
            High_Risk=("risk", lambda x: (x=="HIGH").sum()),
            Urgent=("referral", lambda x: (x=="Urgent").sum()),
        ).reset_index()
        fig_county = px.bar(cnt_df.sort_values("Screenings", ascending=True),
                            x="Screenings", y="county", orientation="h",
                            color="High_Risk", color_continuous_scale=["#e8f5e9",RED],
                            template="plotly_white", title="Screenings by County (color = High Risk count)",
                            labels={"county":"County"})
        fig_county.update_layout(font_family="Plus Jakarta Sans",
                                   margin=dict(t=40,b=0,l=0,r=0),
                                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_county, use_container_width=True)

        # Follow-up compliance by county
        fu_county = df.groupby("county")["followed_up"].mean().reset_index()
        fu_county.columns = ["county", "fu_rate"]
        fu_county["fu_rate"] = (fu_county["fu_rate"] * 100).round(1)
        fig_fu = px.bar(fu_county.sort_values("fu_rate"),
                        x="fu_rate", y="county", orientation="h",
                        template="plotly_white", title="Follow-Up Compliance by County (%)",
                        color="fu_rate", color_continuous_scale=["#ffebee", GREEN],
                        labels={"fu_rate": "Follow-up Rate (%)", "county": "County"})
        fig_fu.update_layout(font_family="Plus Jakarta Sans",
                              margin=dict(t=40,b=0,l=0,r=0),
                              plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_fu, use_container_width=True)

    with tab3:
        prof_df = df.groupby("profession").agg(
            Screenings=("risk","count"),
            High_Risk=("risk", lambda x: (x=="HIGH").sum()),
        ).reset_index()
        fig_prof = px.bar(prof_df.sort_values("Screenings"),
                          x="Screenings", y="profession", orientation="h",
                          color="High_Risk", color_continuous_scale=["#f3e5f5", PURPLE],
                          template="plotly_white", title="Screenings by Profession",
                          labels={"profession": "Profession"})
        fig_prof.update_layout(font_family="Plus Jakarta Sans",
                                margin=dict(t=40,b=0,l=0,r=0),
                                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_prof, use_container_width=True)

    with tab4:
        st.markdown("#### The KAP Gap — Research Foundation")
        kap_col1, kap_col2 = st.columns(2)
        with kap_col1:
            # Waterfall-style gap chart
            categories = ["Attitude (Potential)", "Knowledge", "Practice (Actual)"]
            values     = [65.2, 54.7, 29.2]
            bar_cols   = [TEAL, PURPLE_MID, RED]
            fig_gap = go.Figure()
            for cat, val, col in zip(categories, values, bar_cols):
                fig_gap.add_trace(go.Bar(x=[cat], y=[val], name=cat,
                                          marker_color=col,
                                          text=[f"{val}%"], textposition="outside",
                                          textfont=dict(size=15, color=col)))
            fig_gap.add_shape(type="line", x0=-.5, x1=2.5, y0=65.2, y1=65.2,
                               line=dict(color=TEAL, width=1.5, dash="dot"))
            fig_gap.add_annotation(x=2, y=47,
                                    text="36-point<br>attitude→practice gap",
                                    showarrow=True, arrowhead=2, arrowcolor=RED,
                                    font=dict(color=RED, size=12, family="Plus Jakarta Sans"),
                                    bgcolor="rgba(198,40,40,0.08)", bordercolor=RED,
                                    borderpad=6)
            fig_gap.update_layout(showlegend=False, template="plotly_white",
                                   yaxis=dict(range=[0,80], title="Mean Score (%)"),
                                   xaxis=dict(showgrid=False),
                                   font_family="Plus Jakarta Sans",
                                   margin=dict(t=10,b=10,l=0,r=0), height=300,
                                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_gap, use_container_width=True)

        with kap_col2:
            # Practice scores by profession
            practice_data = {
                "Profession": ["Doctor", "Clinical Officer", "Midwife", "Nurse", "CHW"],
                "Practice Score": [44, 31, 29, 27, 12.7],
            }
            df_prac = pd.DataFrame(practice_data)
            fig_prac = px.bar(df_prac.sort_values("Practice Score"),
                               x="Practice Score", y="Profession", orientation="h",
                               color="Practice Score",
                               color_continuous_scale=[RED, AMBER, GREEN],
                               range_color=[0, 50],
                               template="plotly_white",
                               title="Practice Scores by Profession (%)",
                               text="Practice Score")
            fig_prac.update_traces(texttemplate="%{text}%", textposition="outside")
            fig_prac.update_layout(showlegend=False, font_family="Plus Jakarta Sans",
                                    margin=dict(t=40,b=0,l=0,r=0), height=300,
                                    coloraxis_showscale=False,
                                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_prac, use_container_width=True)

        st.markdown(f"""
        <div class="gcard pink">
          <h3>💡 The Core Insight</h3>
          <p>Community Health Workers score only <strong>12.7% on practice</strong> despite having
          <strong>65%+ on attitude</strong>. They want to act. They just don't have the tools.
          <br><br>
          BreastCare Kenya is built specifically for this gap — a structured, offline,
          point-of-care decision support system for frontline practitioners in under-resourced settings.</p>
        </div>
        """, unsafe_allow_html=True)

    # CSV export
    st.markdown("---")
    csv_data = df.to_csv(index=False)
    st.download_button("⬇️ Export All Screening Data (CSV)",
                        csv_data, file_name="breastcare_screenings.csv", mime="text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 6 — CAREBOT (Rule-Based NLP, Zero API)
# ══════════════════════════════════════════════════════════════════════════════

elif "CareBot" in module:
    st.markdown('<div class="section-head">🤖 CareBot — Clinical AI Assistant</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">Offline-first · Zero API keys · Rule-based clinical NLP · Available from any module</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="gcard" style='margin-bottom:1rem;padding:.9rem 1.2rem;'>
      <div style='display:flex;align-items:center;gap:.7rem;'>
        <div style='background:linear-gradient(135deg,{PURPLE},{PINK_DARK});border-radius:50%;
             width:38px;height:38px;display:flex;align-items:center;justify-content:center;
             font-size:1.1rem;flex-shrink:0;'>🤖</div>
        <div>
          <div style='font-weight:800;font-size:.95rem;color:{DARK};'>BreastCare AI — CareBot</div>
          <div style='font-size:.78rem;color:#888;'>
            Powered by rule-based clinical NLP · Works fully offline · No API required
          </div>
        </div>
        <div style='margin-left:auto;'>
          <span style='background:rgba(46,125,50,0.12);color:{GREEN};border:1.5px solid {GREEN};
               border-radius:20px;padding:4px 14px;font-size:.75rem;font-weight:700;'>
            🟢 Offline Ready
          </span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat history — render each message with st.markdown so formatting works properly
    for msg in st.session_state.chat_history:
        role   = msg["role"]
        text   = msg["text"]
        avatar = "🤖" if role == "bot" else "👩🏾"
        bg     = "white" if role == "bot" else f"linear-gradient(135deg,{PURPLE},{PINK_DARK})"
        color  = DARK   if role == "bot" else "white"
        border = f"1px solid rgba(233,30,140,0.15)" if role == "bot" else "none"
        align  = "flex-start" if role == "bot" else "flex-end"
        av_bg  = f"linear-gradient(135deg,{PURPLE},{PINK_DARK})" if role == "bot" else "#f3e5f5"

        col_left, col_right = st.columns([1, 20]) if role == "bot" else st.columns([20, 1])

        if role == "bot":
            with col_left:
                st.markdown(f"""
                <div style='background:{av_bg};border-radius:50%;width:36px;height:36px;
                     display:flex;align-items:center;justify-content:center;
                     font-size:1.1rem;margin-top:4px;'>{avatar}</div>
                """, unsafe_allow_html=True)
            with col_right:
                st.markdown(f"""
                <div style='background:{bg};color:{color};border:{border};
                     border-radius:16px;border-top-left-radius:4px;
                     padding:.8rem 1.1rem;font-size:.9rem;line-height:1.6;
                     box-shadow:0 2px 8px rgba(74,20,140,0.08);margin-bottom:.5rem;'>
                """, unsafe_allow_html=True)
                st.markdown(text)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            with col_left:
                st.markdown(f"""
                <div style='background:{bg};color:{color};border:{border};
                     border-radius:16px;border-top-right-radius:4px;
                     padding:.8rem 1.1rem;font-size:.9rem;line-height:1.6;
                     margin-bottom:.5rem;text-align:right;'>
                     {text}
                </div>
                """, unsafe_allow_html=True)
            with col_right:
                st.markdown(f"""
                <div style='background:{av_bg};border-radius:50%;width:36px;height:36px;
                     display:flex;align-items:center;justify-content:center;
                     font-size:1.1rem;margin-top:4px;'>{avatar}</div>
                """, unsafe_allow_html=True)

    # Quick question chips
    st.markdown("**Quick questions:**")
    chip_cols = st.columns(4)
    for i, q in enumerate(QUICK_QUESTIONS):
        if chip_cols[i % 4].button(q, key=f"chip_{i}"):
            st.session_state.chat_history.append({"role": "user",   "text": q})
            st.session_state.chat_history.append({"role": "bot",    "text": carebot_respond(q)})
            st.rerun()

    # Input
    with st.form("chat_form", clear_on_submit=True):
        ci1, ci2 = st.columns([5, 1])
        user_input = ci1.text_input("", placeholder="Ask about BSE, referral criteria, staging, KAP data...",
                                     label_visibility="collapsed")
        sent = ci2.form_submit_button("Send", use_container_width=True)
        if sent and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "text": user_input})
            st.session_state.chat_history.append({"role": "bot",  "text": carebot_respond(user_input)})
            st.rerun()

    if st.button("🔄 Clear Chat"):
        st.session_state.chat_history = [
            {"role": "bot", "text": carebot_respond("hello")}
        ]
        st.rerun()

    # Coverage info
    with st.expander("📚 CareBot Knowledge Base — Topics Covered"):
        topics = [
            ("🔴 Risk Factors", "Non-modifiable & modifiable risks, BRCA, family history, protective factors"),
            ("✋ BSE Technique", "Step-by-step guide, visual & palpation, what to report"),
            ("🔀 Referral Criteria", "Kenya MOH pathway: Urgent / Imaging / Routine / Education"),
            ("📊 Staging", "Stage I–IV, survival rates, Kenya context"),
            ("🖼️ Imaging", "Mammography vs ultrasound, availability in Kenya, cost"),
            ("💊 Treatment", "Surgery, chemo, radiotherapy, hormone therapy, HER2"),
            ("📋 KAP Data", "Survey findings, profession breakdown, the 36-point gap"),
            ("💧 Nipple Discharge", "Concerning vs benign features, when to refer"),
            ("🔍 Lump Assessment", "Concerning vs reassuring features, documentation"),
            ("🔔 Follow-Up Protocols", "Post-referral steps, escalation, tracker usage"),
            ("🛡️ Prevention", "Lifestyle, screening schedules, early detection"),
        ]
        for t, desc in topics:
            st.markdown(f"**{t}** — {desc}")