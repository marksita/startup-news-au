import streamlit as st
import feedparser

st.set_page_config(page_title="Startup News AU", layout="wide")

# ---------- MODERN NEWS UI ----------
st.markdown("""
<style>
body { background-color: #f5f7fb; }

.header {
    padding: 20px 0;
    border-bottom: 1px solid #eaeaea;
}

.title {
    font-size: 34px;
    font-weight: 700;
}

.subtitle {
    color: #666;
    margin-top: 4px;
}

.card {
    background: white;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
}

.card-body {
    padding: 14px;
}

.category {
    font-size: 12px;
    font-weight: 600;
    color: #0b66ff;
    margin-bottom: 6px;
}

.card h3 {
    font-size: 18px;
    margin-bottom: 6px;
}

.card p {
    font-size: 14px;
    color: #555;
}

.meta {
    font-size: 12px;
    color: #888;
    margin-top: 8px;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    margin: 20px 0;
}

.top-list {
    background: white;
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.top-item {
    display: flex;
    gap: 10px;
    margin-bottom: 12px;
}

.top-number {
    font-weight: 700;
    font-size: 18px;
    color: #999;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="header">
<div class="title">STARTUP NEWS AU</div>
<div class="subtitle">Australia’s Home of Startup & Innovation News</div>
</div>
""", unsafe_allow_html=True)

# ---------- SOURCES ----------
RSS_FEEDS = [
    "https://www.startupdaily.net/feed/",
    "https://www.smartcompany.com.au/feed/",
    "https://techcrunch.com/tag/australia/feed/",
    "https://www.innovationaus.com/feed/",
    "https://www.businessinsider.com.au/feed"
]

# ---------- FETCH ----------
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
                "image": entry.get("media_content", [{}])[0].get("url") if entry.get("media_content") else None,
                "source": feed.feed.get("title", "Source")
            })
    return articles

articles = fetch_articles()

# ---------- GRID ----------
st.markdown('<div class="section-title">Latest News</div>', unsafe_allow_html=True)

cols = st.columns(3)

for i, a in enumerate(articles[:9]):
    col = cols[i % 3]

    with col:
        st.markdown(f"""
        <div class="card">
            {f'<img src="{a["image"]}" />' if a.get("image") else ''}
            <div class="card-body">
                <div class="category">Startup</div>
                <h3>{a['title']}</h3>
                <p>{a['summary'][:100]}</p>
                <div class="meta">{a['source']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------- TOP 10 ----------
st.markdown('<div class="section-title">Top 10 Stories</div>', unsafe_allow_html=True)

st.markdown('<div class="top-list">', unsafe_allow_html=True)

for i, a in enumerate(articles[:10]):
    st.markdown(f"""
    <div class="top-item">
        <div class="top-number">{i+1}</div>
        <div>
            <a href="{a['link']}" target="_blank"><b>{a['title']}</b></a><br>
            <span class="meta">{a['source']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<hr style="margin-top:40px" />
<p style="text-align:center; color:#999">© 2026 Startup News AU</p>
""", unsafe_allow_html=True)
