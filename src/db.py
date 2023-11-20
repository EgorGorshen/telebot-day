import sqlite3, os
from src.db_requests import (
    ADD_TODO,
    CREATE_TODO_LIST_TABLE,
    DEL_TODO_LIST_TABLE,
    DONE_TODO,
    GET_TODO_LIST,
)
from src.logger import Logger
from src.utils import Level


db_log = Logger("db_log", "log/db.log")
DEVELOP = bool(os.getenv("DEVELOP", False))


@db_log.class_log
class DB:
    def __init__(self, db_path=":memory:") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        if DEVELOP:
            self._del()
        self._init()

    def _init(self):
        self._init_todo_list_table()

    def _del(self):
        self._del_todo_list_table()

    def _init_todo_list_table(self) -> None:
        if self._db_exist():
            return
        cursor = self.conn.cursor()
        cursor.execute(CREATE_TODO_LIST_TABLE)
        self.conn.commit()

    def _db_exist(self):
        if self.db_path == ":memory:":
            return False
        if os.path.exists(self.db_path):
            return True
        return False

    def _del_todo_list_table(self):
        if not self._db_exist():
            return
        cursor = self.conn.cursor()
        cursor.execute(DEL_TODO_LIST_TABLE)
        self.conn.commit()

    def add_todo(self, text: str, level: Level):
        cursor = self.conn.cursor()
        cursor.execute(ADD_TODO, (text, level))
        self.conn.commit()

    def get_todo_list(self, with_done: bool = False):
        cursor = self.conn.cursor()
        cursor.execute(GET_TODO_LIST, (with_done,))
        return cursor.fetchall()

    def change_status_todo(self, todo_id: int, done: bool = True):
        cursor = self.conn.cursor()
        cursor.execute(DONE_TODO, (todo_id, done))
        self.conn.commit()
