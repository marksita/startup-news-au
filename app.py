import streamlit as st
import requests

st.set_page_config(page_title="Startup News AU", layout="wide")

st.title("🇦🇺 Australian Startup News")

query = st.text_input("Search startup news", "startup Australia")

API_KEY = st.secrets["GNEWS_API_KEY"]

@st.cache_data(ttl=600)
def fetch_news(query):
    url = f"https://gnews.io/api/v4/search?q={query}&lang=en&country=au&max=10&apikey={API_KEY}"
    res = requests.get(url)
    data = res.json()
    return data.get("articles", [])

articles = fetch_news(query)

if not articles:
    st.warning("No articles found")
else:
    for a in articles:
        st.subheader(a["title"])

        if a.get("image"):
            st.image(a["image"])

        st.write(a.get("description", ""))

        st.markdown(f"[Read more]({a['url']})")

        st.caption(a["source"]["name"])
        st.divider()
