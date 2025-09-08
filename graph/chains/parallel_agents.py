from graph.chains.classification import qa_chain
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict
import os
import sqlite3

load_dotenv()

Project_Path = os.getenv("PROJECT_PATH")
docs_path = Path(Project_Path+"/assets/unstructured")

conn = sqlite3.connect('common_context.db')
cur = conn.cursor()

def class_entry(result: Dict):
    keys = list(result.keys())

    for key in keys:
        class_name = result[key]["result"]
        key = int(key)
        print(f"Class name: {class_name}", type(class_name))
        cur.execute("UPDATE context SET Class = ? WHERE S_Num = ?", (class_name, key))
        conn.commit()

        cur.execute("SELECT S_Num, File_Name, Collection_Name, Agent_Name, Class FROM context WHERE S_Num = ?;", (key,))
        row = cur.fetchone()
        print(row)

def parallel_agents():
    cur.execute("DROP TABLE IF EXISTS context;")
    cur.execute("""
        CREATE TABLE context (
            S_Num           INTEGER PRIMARY KEY,
            File_Name       TEXT,
            Collection_Name TEXT,
            Agent_Name      TEXT,
            Class           TEXT
        );
    """)
    conn.commit()

    length = sum(1 for _ in docs_path.iterdir())
    batch_size = 7

    qa_chains = {}
    results = []

    start = 0
    while start + batch_size <= length:
        qa_chains[f"qa_{start}_{batch_size}"] = qa_chain(batch_size, start)

        chains = qa_chains[f"qa_{start}_{batch_size}"]
        query = {"query": "Classify."}
        result = chains.invoke(query)
        class_entry(result)
        results.append(result)
        start += batch_size

    remainder = length - start
    if remainder > 0:
        qa_chains[f"qa_{start}_{remainder}"] = qa_chain(remainder, start)

        chains = qa_chains[f"qa_{start}_{remainder}"]
        query = {"query": "Classify."}
        result = chains.invoke(query)
        class_entry(result)
        results.append(result)

    cur.execute("SELECT * FROM context WHERE S_Num >= ?;", (start,))
    _preview_rows = cur.fetchall()

    conn.close()

    return results

if __name__ == "__main__":
    cur.execute("SELECT Class FROM context;")
    rows = cur.fetchall()  # fetclone() for single row
    conn.close()
    print(rows)