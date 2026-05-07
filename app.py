import streamlit as st
import feedparser
from datetime import datetime

st.set_page_config(page_title="Startup News AU", layout="wide")

# ---------- AFR-STYLE LIGHT UI ----------
st.markdown("""
<style>
body { background-color: #ffffff; }
.main { background-color: #ffffff; }

.header {
    border-bottom: 1px solid #e5e5e5;
    padding-bottom: 10px;
    margin-bottom: 25px;
}

h1 {
    font-size: 34px;
    font-weight: 700;
}

.section-title {
    font-size: 18px;
    font-weight: 600;
    margin: 20px 0 10px 0;
    border-bottom: 2px solid #000;
    display: inline-block;
}

.card {
    padding: 12px 0;
    border-bottom: 1px solid #eee;
}

.card h3 {
    font-size: 18px;
    margin-bottom: 5px;
}

.card p {
    color: #555;
    font-size: 14px;
}

.meta {
    font-size: 12px;
    color: #999;
}

.read {
    font-size: 13px;
    color: #0b66ff;
    font-weight: 500;
}

.top-list {
    background: #fafafa;
    padding: 15px;
    border: 1px solid #eee;
}

.top-list li {
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="header">
<h1>Australian Startup News</h1>
<p>Funding, venture capital, startups and technology across Australia</p>
</div>
""", unsafe_allow_html=True)

# ---------- RSS SOURCES (EXPANDED) ----------
RSS_FEEDS = [
    "https://www.startupdaily.net/feed/",
    "https://www.smartcompany.com.au/feed/",
    "https://techcrunch.com/tag/australia/feed/",
    "https://www.afr.com/technology/startups/rss",
    "https://www.innovationaus.com/feed/"
]

# ---------- FETCH ARTICLES ----------
@st.cache_data(ttl=600)
def fetch_articles():
    articles = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:10]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": getattr(entry, "summary", ""),
                "source": feed.feed.get("title", "Source"),
                "published": getattr(entry, "published", "")
            })

    # sort by newest if possible
    return articles

articles = fetch_articles()

# ---------- TOP 10 ----------
st.markdown('<div class="section-title">Top 10 Stories</div>', unsafe_allow_html=True)

st.markdown('<div class="top-list">', unsafe_allow_html=True)

for i, a in enumerate(articles[:10]):
    st.markdown(f"""
    <li>
        <a href="{a['link']}" target="_blank"><b>{a['title']}</b></a><br>
        <span class="meta">{a['source']}</span>
    </li>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- LATEST ARTICLES ----------
st.markdown('<div class="section-title">Latest</div>', unsafe_allow_html=True)

for article in articles[10:40]:
    st.markdown(f"""
    <div class="card">
        <h3>{article['title']}</h3>
        <p>{article['summary'][:200]}</p>
        <a class="read" href="{article['link']}" target="_blank">Read more →</a>
        <div class="meta">{article['source']}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<hr style="margin-top:40px" />
<p style="text-align:center; color:#999">Australian Startup News • Built with Streamlit</p>
""", unsafe_allow_html=True)
