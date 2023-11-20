CREATE_TODO_LIST_TABLE = """
CREATE TABLE IF NOT EXISTS TodoList (
    id integer PRIMARY KEY,
    text text NOT NULL,
    level integer NOT NULL,
    done integer DEFAULT 0
);
"""
DEL_TODO_LIST_TABLE = "DROP TABLE TodoList;"


ADD_TODO = "INSERT INTO TodoList (text, level) VALUES (?, ?)"
GET_TODO_LIST = "SELECT * FROM TodoList WHERE done = ?"
DONE_TODO = "UPDATE TodoList SET done = ? WHERE id = ?"
