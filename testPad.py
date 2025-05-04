import sqlite3
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("INSERT OR REPLACE INTO users (phone, carrier) VALUES (?, ?)", ("7828822311", "vmobile.ca"))
conn.commit()

