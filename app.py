import streamlit as st
import feedparser
import requests
from collections import Counter
import re

st.set_page_config(page_title="Startup News AU", layout="wide")

# ---------- LIGHT THEME STYLING ----------
st.markdown("""
<style>
body { background-color: #f7f9fc; }
.main { background-color: #f7f9fc; }

.hero {
    background: white;
    padding: 24px;
    border-radius: 16px;
    margin-bottom: 25px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.card {
    background: white;
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: 0.2s ease;
}

.card:hover { transform: translateY(-2px); }

.source { font-size: 12px; color: #888; }
.readmore { color: #0b66ff; font-weight: 600; }
.category { font-size: 12px; color: #0b66ff; margin-bottom: 6px; }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
<h1>🇦🇺 Startup News Australia</h1>
<p>Funding, startups, venture capital & tech across Australia</p>
</div>
""", unsafe_allow_html=True)

# ---------- RSS SOURCES (REAL AU SOURCES) ----------
RSS_FEEDS = [
    "https://www.startupdaily.net/feed/",
    "https://www.smartcompany.com.au/feed/",
    "https://techcrunch.com/tag/australia/feed/"
]

# ---------- FETCH RSS ----------
@st.cache_data(ttl=600)
def fetch_rss():
    articles = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:10]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "description": getattr(entry, "summary", ""),
                "source": feed.feed.get("title", "Source")
            })

    return articles

articles = fetch_rss()

# ---------- CATEGORY TAGGING ----------
def categorize(text):
    text = text.lower()

    if "fund" in text or "raise" in text:
        return "Funding"
    if "ai" in text:
        return "AI"
    if "fintech" in text:
        return "Fintech"
    return "Startup"

# ---------- TRENDING STARTUPS ----------
def extract_names(articles):
    words = []

    for a in articles:
        found = re.findall(r"\b[A-Z][a-zA-Z]+\b", a["title"])
        words.extend(found)

    common = Counter(words).most_common(5)
    return [w[0] for w in common]

trending = extract_names(articles)

# ---------- SIDEBAR ----------
st.sidebar.title("🔥 Trending Startups")
for t in trending:
    st.sidebar.write(f"• {t}")

# ---------- FEATURED ----------
if articles:
    featured = articles[0]

    st.markdown("### Featured")

    st.markdown(f"""
    <div class="card">
        <div class="category">{categorize(featured['title'])}</div>
        <h2>{featured['title']}</h2>
        <p>{featured['description'][:200]}</p>
        <a class="readmore" href="{featured['link']}" target="_blank">Read full article →</a>
        <div class="source">{featured['source']}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------- GRID ----------
st.markdown("### Latest News")

cols = st.columns(2)

for i, article in enumerate(articles[1:]):
    col = cols[i % 2]

    with col:
        st.markdown(f"""
        <div class="card">
            <div class="category">{categorize(article['title'])}</div>
            <h3>{article['title']}</h3>
            <p>{article['description'][:150]}</p>
            <a class="readmore" href="{article['link']}" target="_blank">Read more →</a>
            <div class="source">{article['source']}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<hr style="margin-top:40px" />
<p style="text-align:center; color:#999">Free Australian Startup News Aggregator • Built with Streamlit</p>
""", unsafe_allow_html=True)
