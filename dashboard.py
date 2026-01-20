import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.title("Stock Market Intelligence Agent")
st.caption("welcome,")

col1, col2 = st.columns(2)
with col1:
    if st.button("Refresh latest"):
        pass
with col2:
    if st.button("Generate new report now"):
        try:
            requests.get(f"{API}/brief?force=true", timeout=300)
        except Exception:
            pass

st.subheader("Latest Market Summary")
try:
    r = requests.get(f"{API}/brief", timeout=150)
    data = r.json()
    st.write(f"Source: `{data.get('source')}`")
    if data.get("created_at"):
        st.write(f"Created at (UTC): `{data.get('created_at')}`")
    st.text(data["report"])
except Exception as e:
    st.error(f"Agent not running or request failed: {e}")

st.divider()
st.subheader("History (most recent first)")
try:
    r = requests.get(f"{API}/history?limit=30", timeout=30)
    items = r.json().get("items", [])
    for it in items:
        with st.expander(f"#{it['id']} — {it['created_at']}"):
            st.text(it["report"])
except Exception as e:
    st.warning(f"Could not load history: {e}")