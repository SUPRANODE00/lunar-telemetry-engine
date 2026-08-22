import hashlib
import json
import sqlite3

DB_NAME = 'capsule_blockstore.db'

def init_store():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocks 
        (cid TEXT PRIMARY KEY, data TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

def add_block(content):
    cid = 'bafy' + hashlib.sha256(content.encode('utf-8')).hexdigest()[:48]
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO blocks (cid, data) VALUES (?, ?)', (cid, content))
    conn.commit()
    conn.close()
    return cid

if __name__ == '__main__':
    init_store()
    payload = json.dumps({'node': 'SUPRANODE-00-RIVERA', 'status': 'INVERTED-STORAGE'})
    test_cid = add_block(payload)
    print(f'[+] Local block stored successfully. Generated CID: {test_cid}')
