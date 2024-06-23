import streamlit as st

st.title("Streamlit URL 링크 추가 예제")

# Markdown을 사용하여 URL 링크 추가
st.markdown("[Streamlit 홈페이지](https://streamlit.io)")

# HTML을 사용하여 URL 링크 추가
st.markdown('<a href="https://streamlit.io" target="_blank">Streamlit 홈페이지</a>', unsafe_allow_html=True)

# st.write를 사용하여 URL 링크 추가
st.write("[Streamlit 홈페이지](https://streamlit.io)")
