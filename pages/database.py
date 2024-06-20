import sqlite3

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
                 image_url10 TEXT DEFAULT '0', ppt_url10 TEXT DEFAULT '0')''')
    conn.commit()
    conn.close()

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

def clear_table():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("DELETE FROM entries")
    conn.commit()
    conn.close()

def get_matching_entries(content1, content2):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    query = "SELECT * FROM entries WHERE content1 LIKE ? AND content2 LIKE ?"
    c.execute(query, ('%' + content1 + '%', '%' + content2 + '%'))
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_entries():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM entries")
    rows = c.fetchall()
    conn.close()
    return rows

def update_entry(content1, content2, image_url, ppt_url, image_url2, ppt_url2, 
                 image_url3, ppt_url3, image_url4, ppt_url4, image_url5, ppt_url5, 
                 image_url6, ppt_url6, image_url7, ppt_url7, image_url8, ppt_url8, 
                 image_url9, ppt_url9, image_url10, ppt_url10):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''UPDATE entries SET content2 = ?, image_url = ?, ppt_url = ?, image_url2 = ?, ppt_url2 = ?, 
                 image_url3 = ?, ppt_url3 = ?, image_url4 = ?, ppt_url4 = ?, image_url5 = ?, ppt_url5 = ?, 
                 image_url6 = ?, ppt_url6 = ?, image_url7 = ?, ppt_url7 = ?, image_url8 = ?, ppt_url8 = ?, 
                 image_url9 = ?, ppt_url9 = ?, image_url10 = ?, ppt_url10 = ? WHERE content1 = ?''', 
              (content2, image_url, ppt_url, image_url2, ppt_url2, 
               image_url3, ppt_url3, image_url4, ppt_url4, image_url5, ppt_url5, 
               image_url6, ppt_url6, image_url7, ppt_url7, image_url8, ppt_url8, 
               image_url9, ppt_url9, image_url10, ppt_url10, content1))
    conn.commit()
    conn.close()
