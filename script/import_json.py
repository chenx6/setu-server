from sqlite3 import connect
from json import loads

if __name__ == "__main__":
    conn = connect("instance/url.db")
    cursor = conn.cursor()
    with open("instance/s1_pictures.json", 'r') as f:
        lst = loads(f.read())
    for i in lst:
        try:
            cursor.execute(
                "INSERT INTO picture_url (url, source) VALUES (?, ?)", (i, 2))
        except Exception as e:
            print(i, e)
    conn.commit()
