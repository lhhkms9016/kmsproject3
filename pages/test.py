import streamlit as st
import sqlite3
import pandas as pd
import requests

# 데이터베이스 초기화 함수
def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, content1 TEXT DEFAULT '0', content2 TEXT DEFAULT '0', image_url TEXT DEFAULT '0', ppt_url TEXT DEFAULT '0', 
                 image_url2 TEXT DEFAULT '0', ppt_url2 TEXT DEFAULT '0', 
                 image_url3 TEXT DEFAULT '0', ppt_url3 TEXT DEFAULT '0',
                 image_url4 TEXT DEFAULT '0', ppt_url4 TEXT DEFAULT '0',
                 image_url5 TEXT DEFAULT '0', ppt_url5 TEXT DEFAULT '0',
                 image_url6 TEXT DEFAULT '0', ppt_url6 TEXT DEFAULT '0',
                 image_url7 TEXT DEFAULT '0', ppt_url7 TEXT DEFAULT '0',
                 image_url8 TEXT DEFAULT '0', ppt_url8 TEXT DEFAULT '0',
                 image_url9 TEXT DEFAULT '0', ppt_url9 TEXT DEFAULT '0',
                 image_url10 TEXT DEFAULT '0', ppt_url10 TEXT DEFAULT '0'
                 )''')
    conn.commit()
    conn.close()


# 데이터베이스에 값 삽입 함수
def insert_entry(content1, content2, image_url, ppt_url, image_url2, ppt_url2, 
                 image_url3, ppt_url3, image_url4, ppt_url4, image_url5, ppt_url5, 
                 image_url6, ppt_url6, image_url7, ppt_url7, image_url8, ppt_url8, 
                 image_url9, ppt_url9, image_url10, ppt_url10):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''INSERT INTO entries (content1, content2, image_url, ppt_url, image_url2, ppt_url2, 
                 image_url3, ppt_url3, image_url4, ppt_url4, image_url5, ppt_url5, 
                 image_url6, ppt_url6, image_url7, ppt_url7, image_url8, ppt_url8, 
                 image_url9, ppt_url9, image_url10, ppt_url10) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (content1, content2, image_url, ppt_url, image_url2, ppt_url2, 
               image_url3, ppt_url3, image_url4, ppt_url4, image_url5, ppt_url5, 
               image_url6, ppt_url6, image_url7, ppt_url7, image_url8, ppt_url8, 
               image_url9, ppt_url9, image_url10, ppt_url10))
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
def update_entry(content1, content2, image_url, ppt_url, image_url2, ppt_url2, 
                 image_url3, ppt_url3, image_url4, ppt_url4, image_url5, ppt_url5, 
                 image_url6, ppt_url6, image_url7, ppt_url7, image_url8, ppt_url8, 
                 image_url9, ppt_url9, image_url10, ppt_url10):  
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("UPDATE entries SET content2 = ?, image_url = ?, ppt_url = ?, image_url2 = ?, ppt_url2 = ?, image_url3 = ?, ppt_url3 = ?, image_url4 = ?, ppt_url4 = ?, image_url5 = ?, ppt_url5 = ?, image_url6 = ?, ppt_url6 = ?, image_url7 = ?, ppt_url7 = ?, image_url8 = ?, ppt_url8 = ?, image_url9 = ?, ppt_url9 = ?, image_url10 = ?, ppt_url10 = ? WHERE content1 = ?",  
              (content2, image_url, ppt_url, image_url2, ppt_url2, image_url3, ppt_url3, image_url4, ppt_url4, image_url5, ppt_url5, image_url6, ppt_url6, image_url7, ppt_url7, image_url8, ppt_url8, image_url9, ppt_url9, image_url10, ppt_url10, content1))  
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
    else:
        st.write('이미지가 없습니다.')

# 데이터베이스에 데이터 삽입 및 편집 기능
def data_editor_with_db(df, key_prefix):
    if st.button(f"데이터베이스에 저장 ({key_prefix})", key=f"{key_prefix}_save_button"):
        clear_table()  # 테이블을 비움
        for index, row in df.iterrows():
            insert_entry(row['Content1'], row['Content2'], row['Image URL'], row['PPT URL'], row['Image URL2'], row['PPT URL2'], 
                         row['Image URL3'], row['PPT URL3'], row['Image URL4'], row['PPT URL4'], row['Image URL5'], row['PPT URL5'], 
                         row['Image URL6'], row['PPT URL6'], row['Image URL7'], row['PPT URL7'], row['Image URL8'], row['PPT URL8'], 
                         row['Image URL9'], row['PPT URL9'], row['Image URL10'], row['PPT URL10'])  
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
            df = pd.DataFrame(st.session_state.filtered_entries, columns=['ID', 'Content1', 'Content2', 'Image URL', 'PPT URL', 'Image URL2', 'PPT URL2', 
                                                                           'Image URL3', 'PPT URL3', 'Image URL4', 'PPT URL4', 'Image URL5', 'PPT URL5', 
                                                                           'Image URL6', 'PPT URL6', 'Image URL7', 'PPT URL7', 'Image URL8', 'PPT URL8', 
                                                                           'Image URL9', 'PPT URL9', 'Image URL10', 'PPT URL10'])  
        else:
            df = pd.DataFrame(st.session_state.all_entries, columns=['ID', 'Content1', 'Content2', 'Image URL', 'PPT URL', 'Image URL2', 'PPT URL2', 
                                                                      'Image URL3', 'PPT URL3', 'Image URL4', 'PPT URL4', 'Image URL5', 'PPT URL5', 
                                                                      'Image URL6', 'PPT URL6', 'Image URL7', 'PPT URL7', 'Image URL8', 'PPT URL8', 
                                                                      'Image URL9', 'PPT URL9', 'Image URL10', 'PPT URL10'])  

        with st.expander("데이터 테이블 보기"):
            edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor_tab1")
            data_editor_with_db(edited_df, key_prefix='tab1')

            if not edited_df.empty:
                selected_row = edited_df.iloc[0]
                st.session_state.selected_entry_id = selected_row['ID']
                st.session_state.selected_entry_content1 = selected_row['Content1']
                st.session_state.selected_entry_content2 = selected_row['Content2']
                st.session_state.selected_entry_image_url = selected_row['Image URL']
                st.session_state.selected_entry_ppt_url = selected_row['PPT URL']
                st.session_state.selected_entry_image_url2 = selected_row['Image URL2']
                st.session_state.selected_entry_ppt_url2 = selected_row['PPT URL2']
                st.session_state.selected_entry_image_url3 = selected_row['Image URL3']  # 추가된 변수
                st.session_state.selected_entry_ppt_url3 = selected_row['PPT URL3']  # 추가된 변수
                st.session_state.selected_entry_image_url4 = selected_row['Image URL4']  # 추가된 변수
                st.session_state.selected_entry_ppt_url4 = selected_row['PPT URL4']  # 추가된 변수
                st.session_state.selected_entry_image_url5 = selected_row['Image URL5']  # 추가된 변수
                st.session_state.selected_entry_ppt_url5 = selected_row['PPT URL5']  # 추가된 변수
                st.session_state.selected_entry_image_url6 = selected_row['Image URL6']  # 추가된 변수
                st.session_state.selected_entry_ppt_url6 = selected_row['PPT URL6']  # 추가된 변수
                st.session_state.selected_entry_image_url7 = selected_row['Image URL7']  # 추가된 변수
                st.session_state.selected_entry_ppt_url7 = selected_row['PPT URL7']  # 추가된 변수
                st.session_state.selected_entry_image_url8 = selected_row['Image URL8']  # 추가된 변수
                st.session_state.selected_entry_ppt_url8 = selected_row['PPT URL8']  # 추가된 변수
                st.session_state.selected_entry_image_url9 = selected_row['Image URL9']  # 추가된 변수
                st.session_state.selected_entry_ppt_url9 = selected_row['PPT URL9']  # 추가된 변수
                st.session_state.selected_entry_image_url10 = selected_row['Image URL10']  # 추가된 변수
                st.session_state.selected_entry_ppt_url10 = selected_row['PPT URL10']  # 추가된 변수
            else:
                st.session_state.selected_entry_id = None
                st.session_state.selected_entry_content1 = None
                st.session_state.selected_entry_content2 = None
                st.session_state.selected_entry_image_url = None
                st.session_state.selected_entry_ppt_url = None
                st.session_state.selected_entry_image_url2 = None
                st.session_state.selected_entry_ppt_url2 = None
                st.session_state.selected_entry_image_url3 = None  # 추가된 변수
                st.session_state.selected_entry_ppt_url3 = None  # 추가된 변수
                st.session_state.selected_entry_image_url4 = None  # 추가된 변수
                st.session_state.selected_entry_ppt_url4 = None  # 추가된 변수
                st.session_state.selected_entry_image_url5 = None  # 추가된 변수
                st.session_state.selected_entry_ppt_url5 = None  # 추가된 변수
                st.session_state.selected_entry_image_url6 = None  # 추가된 변수
                st.session_state.selected_entry_ppt_url6 = None  # 추가된 변수
                st.session_state.selected_entry_image_url7 = None  # 추가된 변수
                st.session_state.selected_entry_ppt_url7 = None  # 추가된 변수
                st.session_state.selected_entry_image_url8 = None  # 추가된 변수
                st.session_state.selected_entry_ppt_url8 = None  # 추가된 변수
                st.session_state.selected_entry_image_url9 = None  # 추가된 변수
                st.session_state.selected_entry_ppt_url9 = None  # 추가된 변수
                st.session_state.selected_entry_image_url10 = None  # 추가된 변수
                st.session_state.selected_entry_ppt_url10 = None  # 추가된 변수

        st.sidebar.header("조회 기능")
        st.sidebar.write('조회할 값을 입력하고 조회 버튼을 누르세요 (컬럼 1과 컬럼 2 기준).')
        search_input1 = st.sidebar.text_input('조회할 값 (Content1):')
        search_input2 = st.sidebar.text_input('조회할 값 (Content2):')

        if st.sidebar.button('조회'):
            if search_input1 or search_input2:
                entries = get_matching_entries(search_input1, search_input2)
                if entries:
                    st.session_state.filtered_entries = entries
                    st.experimental_rerun()
                else:
                    st.sidebar.write('매칭되는 값이 없습니다.')
                    st.session_state.pop('filtered_entries', None)
            else:
                st.session_state.pop('filtered_entries', None)
                st.experimental_rerun()

        tab1_input1 = st.text_input('조회된 값 (Content1):', key='selected_user_input1_tab1', value=st.session_state.get('selected_entry_content1', ''))
        tab1_input2 = st.text_input('조회된 값 (Content2):', key='selected_user_input2_tab1', value=st.session_state.get('selected_entry_content2', ''))

        with st.expander("제안서 보기"):
            col1, col2 = st.columns([4, 1])
            with col1:
                tab1_input3 = st.text_input('조회된 값 (이미지 URL):', key='selected_user_input3_tab1', value=st.session_state.get('selected_entry_image_url', ''))
            with col2:
                image_url = st.session_state.get('selected_entry_image_url', '')
                if image_url:
                    st.markdown(f"[이미지 확대 보기]({image_url})")

            col3, col4 = st.columns([4, 1])
            with col3:
                tab1_input4 = st.text_input('조회된 값 (PPT URL):', key='selected_user_input4_tab1', value=st.session_state.get('selected_entry_ppt_url', ''))
            with col4:
                ppt_url = st.session_state.get('selected_entry_ppt_url', '')
                if ppt_url:
                    st.markdown(f"[PPT 링크 열기]({ppt_url})")

            display_image_from_url(st.session_state.get('selected_entry_image_url', ''))

            col5, col6 = st.columns([4, 1])
            with col5:
                tab1_input5 = st.text_input('조회된 값 (이미지 URL2):', key='selected_user_input5_tab1', value=st.session_state.get('selected_entry_image_url2', ''))
            with col6:
                image_url2 = st.session_state.get('selected_entry_image_url2', '')
                if image_url2:
                    st.markdown(f"[이미지 확대 보기]({image_url2})")

            col7, col8 = st.columns([4, 1])
            with col7:
                tab1_input6 = st.text_input('조회된 값 (PPT URL2):', key='selected_user_input6_tab1', value=st.session_state.get('selected_entry_ppt_url2', ''))
            with col8:
                ppt_url2 = st.session_state.get('selected_entry_ppt_url2', '')
                if ppt_url2:
                    st.markdown(f"[PPT 링크 열기]({ppt_url2})")
        
            display_image_from_url(st.session_state.get('selected_entry_image_url2', ''))

            col9, col10 = st.columns([4, 1])
            with col9:
                tab1_input7 = st.text_input('조회된 값 (이미지 URL3):', key='selected_user_input7_tab1', value=st.session_state.get('selected_entry_image_url3', ''))  # 추가된 필드
            with col10:
                image_url3 = st.session_state.get('selected_entry_image_url3', '')
                if image_url3:
                    st.markdown(f"[이미지 확대 보기]({image_url3})")

            col11, col12 = st.columns([4, 1])
            with col11:
                tab1_input8 = st.text_input('조회된 값 (PPT URL3):', key='selected_user_input8_tab1', value=st.session_state.get('selected_entry_ppt_url3', ''))  # 추가된 필드
            with col12:
                ppt_url3 = st.session_state.get('selected_entry_ppt_url3', '')
                if ppt_url3:
                    st.markdown(f"[PPT 링크 열기]({ppt_url3})")

            display_image_from_url(st.session_state.get('selected_entry_image_url3', ''))

            col13, col14 = st.columns([4, 1])
            with col13:
                tab1_input9 = st.text_input('조회된 값 (이미지 URL4):', key='selected_user_input9_tab1', value=st.session_state.get('selected_entry_image_url4', ''))  # 추가된 필드
            with col14:
                image_url4 = st.session_state.get('selected_entry_image_url4', '')
                if image_url4:
                    st.markdown(f"[이미지 확대 보기]({image_url4})")

            col15, col16 = st.columns([4, 1])
            with col15:
                tab1_input10 = st.text_input('조회된 값 (PPT URL4):', key='selected_user_input10_tab1', value=st.session_state.get('selected_entry_ppt_url4', ''))  # 추가된 필드
            with col16:
                ppt_url4 = st.session_state.get('selected_entry_ppt_url4', '')
                if ppt_url4:
                    st.markdown(f"[PPT 링크 열기]({ppt_url4})")

            display_image_from_url(st.session_state.get('selected_entry_image_url4', ''))  # 추가된 함수 호출

            col17, col18 = st.columns([4, 1])
            with col17:
                tab1_input11 = st.text_input('조회된 값 (이미지 URL5):', key='selected_user_input11_tab1', value=st.session_state.get('selected_entry_image_url5', ''))  # 추가된 필드
            with col18:
                image_url5 = st.session_state.get('selected_entry_image_url5', '')
                if image_url5:
                    st.markdown(f"[이미지 확대 보기]({image_url5})")

            col19, col20 = st.columns([4, 1])
            with col19:
                tab1_input12 = st.text_input('조회된 값 (PPT URL5):', key='selected_user_input12_tab1', value=st.session_state.get('selected_entry_ppt_url5', ''))  # 추가된 필드
            with col20:
                ppt_url5 = st.session_state.get('selected_entry_ppt_url5', '')
                if ppt_url5:
                    st.markdown(f"[PPT 링크 열기]({ppt_url5})")

            display_image_from_url(st.session_state.get('selected_entry_image_url5', ''))  # 추가된 함수 호출

            col21, col22 = st.columns([4, 1])
            with col21:
                tab1_input13 = st.text_input('조회된 값 (이미지 URL6):', key='selected_user_input13_tab1', value=st.session_state.get('selected_entry_image_url6', ''))  # 추가된 필드
            with col22:
                image_url6 = st.session_state.get('selected_entry_image_url6', '')
                if image_url6:
                    st.markdown(f"[이미지 확대 보기]({image_url6})")

            col23, col24 = st.columns([4, 1])
            with col23:
                tab1_input14 = st.text_input('조회된 값 (PPT URL6):', key='selected_user_input14_tab1', value=st.session_state.get('selected_entry_ppt_url6', ''))  # 추가된 필드
            with col24:
                ppt_url6 = st.session_state.get('selected_entry_ppt_url6', '')
                if ppt_url6:
                    st.markdown(f"[PPT 링크 열기]({ppt_url6})")
        
            display_image_from_url(st.session_state.get('selected_entry_image_url6', ''))  # 추가된 함수 호출

            col25, col26 = st.columns([4, 1])
            with col25:
                tab1_input15 = st.text_input('조회된 값 (이미지 URL7):', key='selected_user_input15_tab1', value=st.session_state.get('selected_entry_image_url7', ''))  # 추가된 필드
            with col26:
                image_url7 = st.session_state.get('selected_entry_image_url7', '')
                if image_url7:
                    st.markdown(f"[이미지 확대 보기]({image_url7})")

            col27, col28 = st.columns([4, 1])
            with col27:
                tab1_input16 = st.text_input('조회된 값 (PPT URL7):', key='selected_user_input16_tab1', value=st.session_state.get('selected_entry_ppt_url7', ''))  # 추가된 필드
            with col28:
                ppt_url7 = st.session_state.get('selected_entry_ppt_url7', '')
                if ppt_url7:
                    st.markdown(f"[PPT 링크 열기]({ppt_url7})")

            display_image_from_url(st.session_state.get('selected_entry_image_url7', ''))  # 추가된 함수 호출

            col29, col30 = st.columns([4, 1])
            with col29:
                tab1_input17 = st.text_input('조회된 값 (이미지 URL8):', key='selected_user_input17_tab1', value=st.session_state.get('selected_entry_image_url8', ''))  # 추가된 필드
            with col30:
                image_url8 = st.session_state.get('selected_entry_image_url8', '')
                if image_url8:
                    st.markdown(f"[이미지 확대 보기]({image_url8})")

            col31, col32 = st.columns([4, 1])
            with col31:
                tab1_input18 = st.text_input('조회된 값 (PPT URL8):', key='selected_user_input18_tab1', value=st.session_state.get('selected_entry_ppt_url8', ''))  # 추가된 필드
            with col32:
                ppt_url8 = st.session_state.get('selected_entry_ppt_url8', '')
                if ppt_url8:
                    st.markdown(f"[PPT 링크 열기]({ppt_url8})")

            display_image_from_url(st.session_state.get('selected_entry_image_url8', ''))  # 추가된 함수 호출

            col33, col34 = st.columns([4, 1])
            with col33:
                tab1_input19 = st.text_input('조회된 값 (이미지 URL9):', key='selected_user_input19_tab1', value=st.session_state.get('selected_entry_image_url9', ''))  # 추가된 필드
            with col34:
                image_url9 = st.session_state.get('selected_entry_image_url9', '')
                if image_url9:
                    st.markdown(f"[이미지 확대 보기]({image_url9})")

            col35, col36 = st.columns([4, 1])
            with col35:
                tab1_input20 = st.text_input('조회된 값 (PPT URL9):', key='selected_user_input20_tab1', value=st.session_state.get('selected_entry_ppt_url9', ''))  # 추가된 필드
            with col36:
                ppt_url9 = st.session_state.get('selected_entry_ppt_url9', '')
                if ppt_url9:
                    st.markdown(f"[PPT 링크 열기]({ppt_url9})")

            display_image_from_url(st.session_state.get('selected_entry_image_url9', ''))  # 추가된 함수 호출

            col37, col38 = st.columns([4, 1])
            with col37:
                tab1_input21 = st.text_input('조회된 값 (이미지 URL10):', key='selected_user_input21_tab1', value=st.session_state.get('selected_entry_image_url10', ''))  # 추가된 필드
            with col38:
                image_url10 = st.session_state.get('selected_entry_image_url10', '')
                if image_url10:
                    st.markdown(f"[이미지 확대 보기]({image_url10})")

            col39, col40 = st.columns([4, 1])
            with col39:
                tab1_input22 = st.text_input('조회된 값 (PPT URL10):', key='selected_user_input22_tab1', value=st.session_state.get('selected_entry_ppt_url10', ''))  # 추가된 필드
            with col40:
                ppt_url10 = st.session_state.get('selected_entry_ppt_url10', '')
                if ppt_url10:
                    st.markdown(f"[PPT 링크 열기]({ppt_url10})")

            display_image_from_url(st.session_state.get('selected_entry_image_url10', ''))  # 추가된 함수 호출

        # 수정 버튼 추가
        if st.button("수정"):
            update_entry(tab1_input1, tab1_input2, tab1_input3, tab1_input4, tab1_input5, tab1_input6, tab1_input7, tab1_input8, 
                         tab1_input9, tab1_input10, tab1_input11, tab1_input12, tab1_input13, tab1_input14, tab1_input15, tab1_input16, 
                         tab1_input17, tab1_input18, tab1_input19, tab1_input20, tab1_input21, tab1_input22)  
            st.success("데이터가 성공적으로 수정되었습니다.")
            st.session_state.all_entries = get_all_entries()
            st.experimental_rerun()

    with tabs[1]:
        st.header("Tab2")

# if __name__ == "__main__":
#     app2()
