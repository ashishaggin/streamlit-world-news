import streamlit as st
import requests
import time

# === Your NewsAPI key ===
NEWS_API_KEY = "47557e4ea0bb4d0c9a941ed4ea74d43d"

# === Page config ===
st.set_page_config(page_title="World News", layout="wide")
st.title("📰 Top World News")
st.caption(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# === Function to fetch top news ===
@st.cache_data(ttl=3600)
def get_top_news():
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=10&category=general&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])
        return articles
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

# === Refresh Button ===
if st.button("🔄 Refresh News"):
    st.cache_data.clear()

# === Display News ===
news = get_top_news()
if not news:
    st.warning("No news available at the moment.")
else:
    for i, article in enumerate(news, 1):
        st.subheader(f"{i}. {article.get('title', 'No title')}")
        st.write(f"**Source**: {article.get('source', {}).get('name', 'Unknown')}")
        st.write(article.get('description', ''))
        if article.get('url'):
            st.markdown(f"[🔗 Read more]({article['url']})", unsafe_allow_html=True)
        st.markdown("---")
