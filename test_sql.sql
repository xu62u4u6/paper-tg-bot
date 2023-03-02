CREATE TABLE user_info (
    chat_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    user_name TEXT,
    created_at DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE msg (
    msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    raw_text TEXT NOT NULL,
    translated_text TEXT,
    received_time TIMESTAMP NOT NULL,
    created_at DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(chat_id) REFERENCES user_info(chat_id)
);