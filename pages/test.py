import streamlit as st
import sqlite3
import pandas as pd
import requests

# 데이터베이스 초기화 함수
def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, content1 TEXT DEFAULT '0', content2 TEXT DEFAULT '0', image_url TEXT DEFAULT '0', ppt_url TEXT DEFAULT '0')''')
    conn.commit()
    conn.close()

# 데이터베이스에 값 삽입 함수
def insert_entry(content1, content2, image_url, ppt_url):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("INSERT INTO entries (content1, content2, image_url, ppt_url) VALUES (?, ?, ?, ?)", (content1, content2, image_url, ppt_url))
    conn.commit()
    conn.close()

# 데이터베이스 테이블 비우기 함수
def clear_table():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("DELETE FROM entries")
    conn.commit()
    conn.close()

# 데이터베이스에서 조건에 맞는 항목 조회 함수
def get_matching_entries(content1, content2):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    query = "SELECT * FROM entries WHERE content1 LIKE ? AND content2 LIKE ?"
    c.execute(query, ('%' + content1 + '%', '%' + content2 + '%'))
    rows = c.fetchall()
    conn.close()
    return rows

# 데이터베이스에서 모든 항목 조회 함수
def get_all_entries():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM entries")
    rows = c.fetchall()
    conn.close()
    return rows

# 데이터베이스 업데이트 함수
def update_entry(content1, content2, image_url, ppt_url):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("UPDATE entries SET content2 = ?, image_url = ?, ppt_url = ? WHERE content1 = ?", (content2, image_url, ppt_url, content1))
    conn.commit()
    conn.close()

# 이미지 URL 유효성 검사 함수
def is_valid_image_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200 and 'image' in response.headers['Content-Type']:
            return True
        else:
            return False
    except:
        return False

# 이미지 URL을 받아서 해당 이미지를 표시하는 함수
def display_image_from_url(image_url):
    if image_url:
        st.image(image_url, caption='이미지', use_column_width=True)
        # 이미지 클릭 시 확대 가능한 링크 생성
        st.markdown(f"[이미지 확대 보기]({image_url})")
    else:
        st.write('이미지가 없습니다.')

# 데이터베이스에 데이터 삽입 및 편집 기능
def data_editor_with_db(df, key_prefix):
    if st.button(f"데이터베이스에 저장 ({key_prefix})", key=f"{key_prefix}_save_button"):
        clear_table()  # 테이블을 비움
        for index, row in df.iterrows():
            insert_entry(row['Content1'], row['Content2'], row['Image URL'], row['PPT_URL'])
        st.success("데이터가 성공적으로 데이터베이스에 저장되었습니다.")

# Streamlit 앱 메인 함수
def app2():
    st.title('제안목차')

    # 초기화 함수 호출 (한 번만 호출되도록 개선)
    if 'initialized' not in st.session_state:
        init_db()
        st.session_state.initialized = True

    tabs = st.tabs(["Tab1", "Tab2"])

    with tabs[0]:
        st.header("Tab1")

        # 모든 항목을 테이블로 표시
        if 'all_entries' not in st.session_state:
            st.session_state.all_entries = get_all_entries()
        
        if 'filtered_entries' in st.session_state:
            df = pd.DataFrame(st.session_state.filtered_entries, columns=['ID', 'Content1', 'Content2', 'Image URL', 'PPT_URL'])
        else:
            df = pd.DataFrame(st.session_state.all_entries, columns=['ID', 'Content1', 'Content2', 'Image URL', 'PPT_URL'])

        with st.expander("데이터 테이블 보기"):
            edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor_tab1")
            # 데이터베이스에 데이터 삽입 및 편집 기능 추가
            data_editor_with_db(edited_df, key_prefix='tab1')

            if not edited_df.empty:
                selected_row = edited_df.iloc[0]
                st.session_state.selected_entry_id = selected_row['ID']
                st.session_state.selected_entry_content1 = selected_row['Content1']
                st.session_state.selected_entry_content2 = selected_row['Content2']
                st.session_state.selected_entry_image_url = selected_row['Image URL']
                st.session_state.selected_entry_ppt_url = selected_row['PPT_URL']
            else:
                st.session_state.selected_entry_id = None
                st.session_state.selected_entry_content1 = None
                st.session_state.selected_entry_content2 = None
                st.session_state.selected_entry_image_url = None
                st.session_state.selected_entry_ppt_url = None

        st.sidebar.header("조회 기능")
        st.sidebar.write('조회할 값을 입력하고 조회 버튼을 누르세요 (컬럼 1과 컬럼 2 기준).')
        search_input1 = st.sidebar.text_input('조회할 값 (Content1):')
        search_input2 = st.sidebar.text_input('조회할 값 (Content2):')

        if st.sidebar.button('조회'):
            if search_input1 or search_input2:
                entries = get_matching_entries(search_input1, search_input2)
                if entries:
                    st.session_state.filtered_entries = entries
                    st.experimental_rerun()  # 페이지를 새로 고침하여 최신 데이터 반영
                else:
                    st.sidebar.write('매칭되는 값이 없습니다.')
                    st.session_state.pop('filtered_entries', None)
            else:
                st.session_state.pop('filtered_entries', None)
                st.experimental_rerun()

        # 조회된 값을 text_input에 표시
        tab1_input1 = st.text_input('조회된 값 (Content1):', key='selected_user_input1_tab1', value=st.session_state.get('selected_entry_content1', ''))
        tab1_input2 = st.text_input('조회된 값 (Content2):', key='selected_user_input2_tab1', value=st.session_state.get('selected_entry_content2', ''))
        tab1_input3 = st.text_input('조회된 값 (이미지 URL):', key='selected_user_input3_tab1', value=st.session_state.get('selected_entry_image_url', ''))
        tab1_input4 = st.text_input('조회된 값 (PPT URL):', key='selected_user_input4_tab1', value=st.session_state.get('selected_entry_ppt_url', ''))
        
        # 수정 버튼 추가
        if st.button("수정"):
            update_entry(tab1_input1, tab1_input2, tab1_input3, tab1_input4)
            st.success("데이터가 성공적으로 수정되었습니다.")
            st.session_state.all_entries = get_all_entries()  # 최신 데이터를 불러와서 업데이트
            st.experimental_rerun()  # 페이지를 새로 고침하여 최신 데이터 반영

        # 이미지 표시
        display_image_from_url(st.session_state.get('selected_entry_image_url', ''))

    with tabs[1]:
        st.header("Tab2")

# if __name__ == "__main__":
#     app()
