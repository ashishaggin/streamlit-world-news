import streamlit as st
import requests
import time
import os

# === Page Setup ===
st.set_page_config(page_title="🌍 Top World News", layout="wide")
st.title("🌍 Top World News")
st.caption(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# === Load API Key from Streamlit Secrets ===
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# === Function to Fetch Top Headlines ===
@st.cache_data(ttl=3600)
def get_top_news():
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"language=en&"
        f"pageSize=10&"
        f"apiKey={NEWS_API_KEY}"
    )
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("status") != "ok":
            st.error(f"❌ NewsAPI error: {data.get('message', 'Unknown error')}")
            return []

        return data.get("articles", [])

    except Exception as e:
        st.error(f"⚠️ Error fetching news: {e}")
        return []

# === Manual Refresh Button ===
if st.button("🔄 Refresh News"):
    st.cache_data.clear()
    st.rerun()  # ✅ updated from st.experimental_rerun()

# === Display News ===
news = get_top_news()
if not news:
    st.warning("⚠️ No news available at the moment.")
else:
    for i, article in enumerate(news, 1):
        st.subheader(f"{i}. {article.get('title', 'No title')}")
        st.write(f"**Source**: {article.get('source', {}).get('name', 'Unknown')}")
        st.write(article.get('description', ''))
        if article.get('url'):
            st.markdown(f"[🔗 Read more]({article['url']})", unsafe_allow_html=True)
        st.markdown("---")
