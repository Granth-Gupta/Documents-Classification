import sqlite3

conn = sqlite3.connect('common_context.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS context;")
#
cur.execute("""
CREATE TABLE context (
  File_Name TEXT PRIMARY KEY,
  Collection_Name TEXT,
  Agent_Name TEXT,
  Class TEXT
);
""")

# cur.execute("INSERT INTO context (File_Name, Collection_Name, Agent_Name, Class) VALUES (?,?,?,?);",
#             ('File5.pdf','vectors_9','agent_2','C++'))
# cur.execute("INSERT INTO context (File_Name, Collection_Name, Agent_Name, Class) VALUES (?,?,?,?);",
#             ('File2.pdf','vectors_6','agent_1','langchain'))

# conn.commit()

# cur.execute("SELECT * FROM context;")
# print(cur.fetchall())
#
# cur.execute("SELECT Collection_Name FROM context where Agent_Name == 'agent_1'")
# a = cur.fetchall()
# print(a[0][0], type(a[0][0]))

conn.close()
