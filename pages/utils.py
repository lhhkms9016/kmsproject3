import streamlit as st
import requests

def is_valid_image_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200 and 'image' in response.headers['Content-Type']:
            return True
        else:
            return False
    except:
        return False

def display_image_from_url(image_url):
    if image_url:
        st.image(image_url, caption='이미지', use_column_width=True)
    else:
        st.write('이미지가 없습니다.')

def data_editor_with_db(df, key_prefix):
    from database import insert_entry, clear_table
    if st.button(f"데이터베이스에 저장 ({key_prefix})", key=f"{key_prefix}_save_button"):
        clear_table()  # 테이블을 비움
        for index, row in df.iterrows():
            insert_entry(row['Content1'], row['Content2'], row['Image URL'], row['PPT URL'], row['Image URL2'], row['PPT URL2'], 
                         row['Image URL3'], row['PPT URL3'], row['Image URL4'], row['PPT URL4'], row['Image URL5'], row['PPT URL5'], 
                         row['Image URL6'], row['PPT URL6'], row['Image URL7'], row['PPT URL7'], row['Image URL8'], row['PPT URL8'], 
                         row['Image URL9'], row['PPT URL9'], row['Image URL10'], row['PPT URL10'])
        st.success("데이터가 성공적으로 데이터베이스에 저장되었습니다.")
        st.experimental_rerun()  # 페이지를 새로 고침하여 최신 데이터 반영
