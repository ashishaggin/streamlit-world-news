import streamlit as st
import requests
import time
import os

st.set_page_config(page_title="India & US Economy News", layout="wide")
st.title("🌏 India & US Economy News")

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# === Refresh every 1 hour ===
st.caption(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
countdown = st.empty()

for remaining in range(3600, 0, -1):
    mins, secs = divmod(remaining, 60)
    countdown.markdown(f"⏳ Auto-refresh in: **{mins:02d}:{secs:02d}**", unsafe_allow_html=True)
    time.sleep(1)
    if remaining == 1:
        st.experimental_rerun()

# === Function to fetch filtered news ===
@st.cache_data(ttl=3600)
def get_top_news():
    keywords = "India OR Indian economy OR RBI OR US economy OR Federal Reserve OR inflation OR GDP OR Powell"
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={keywords}&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"pageSize=10&"
        f"apiKey={NEWS_API_KEY}"
    )
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("articles", [])
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

# === Refresh Button ===
if st.button("🔄 Refresh Now"):
    st.cache_data.clear()
    st.experimental_rerun()

# === Display News ===
news = get_top_news()
if not news:
    st.warning("No news available at the moment.")
else:
    for i, article in enumerate(news, 1):
        st.subheader(f"{i}. {article.get('title', 'No title')}")
        st.write(f"**Source**: {article.get('source', {}).get('name', '')}")
        st.write(article.get('description', ''))
        if article.get('url'):
            st.markdown(f"[🔗 Read more]({article['url']})", unsafe_allow_html=True)
        st.markdown("---")
