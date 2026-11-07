"""Offline tests for the SQL safety checks (no database or API key needed).

Run from the project root:  python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dashboard"))

from sql_guard import check_sql, prepare_sql, validate_sql  # noqa: E402

SAFE_QUERIES = [
    "SELECT * FROM vw_school_directory WHERE province = 'Harare';",
    "SELECT school_name, o_level_rank FROM vw_school_directory WHERE o_level_rank IS NOT NULL ORDER BY o_level_rank ASC LIMIT 10;",
    "SELECT school_name, official_website FROM vw_school_directory WHERE official_website IS NOT NULL;",
    "SELECT province, COUNT(*) AS schools FROM vw_school_directory GROUP BY province ORDER BY schools DESC;",
    "select count(*) from vw_school_directory where city = 'Bulawayo'",
    # words that look dangerous but only appear inside a text value are fine
    "SELECT school_name FROM vw_school_directory WHERE school_name ILIKE '%do%' OR school_name ILIKE '%create%';",
    "SELECT school_name FROM vw_school_directory WHERE school_name = 'St John''s College';",
]

UNSAFE_QUERIES = {
    "drop table": "DROP TABLE vw_school_directory;",
    "delete": "DELETE FROM vw_school_directory;",
    "second statement": "SELECT * FROM vw_school_directory; DROP TABLE schools;",
    "other table": "SELECT * FROM pg_user, vw_school_directory;",
    "join other table": "SELECT * FROM vw_school_directory JOIN pg_shadow ON true;",
    "view name hidden in a comment": "SELECT * FROM schools /* vw_school_directory */",
    "view name hidden after a line comment": "SELECT * FROM schools -- vw_school_directory",
    "server function": "SELECT pg_sleep(30) FROM vw_school_directory;",
    "file function": "SELECT pg_read_file('/etc/passwd') FROM vw_school_directory;",
    "select into creates a table": "SELECT * INTO backup_copy FROM vw_school_directory;",
    "union with another table": "SELECT school_name FROM vw_school_directory UNION SELECT usename FROM pg_user;",
    "copy to program": "SELECT 1; COPY (SELECT 1) TO PROGRAM 'id';",
    "no from clause": "SELECT 1;",
    "subquery in from": "SELECT * FROM (SELECT * FROM schools) s, vw_school_directory;",
    "quoted identifier": 'SELECT * FROM "vw_school_directory";',
    "empty": "   ",
}


class SafeQueryTests(unittest.TestCase):
    def test_normal_queries_are_accepted(self):
        for sql in SAFE_QUERIES:
            with self.subTest(sql=sql):
                self.assertTrue(validate_sql(sql), check_sql(sql)[1])


class UnsafeQueryTests(unittest.TestCase):
    def test_dangerous_queries_are_rejected(self):
        for name, sql in UNSAFE_QUERIES.items():
            with self.subTest(case=name):
                self.assertFalse(validate_sql(sql))

    def test_reason_is_given_when_rejected(self):
        ok, reason = check_sql("DROP TABLE x;")
        self.assertFalse(ok)
        self.assertTrue(reason)

    def test_non_string_input_is_rejected(self):
        self.assertFalse(validate_sql(None))


class PrepareSqlTests(unittest.TestCase):
    def test_row_limit_is_added_and_semicolon_removed(self):
        sql = prepare_sql("SELECT * FROM vw_school_directory WHERE province = 'Harare';", max_rows=50)
        self.assertEqual(
            sql,
            "SELECT * FROM (SELECT * FROM vw_school_directory WHERE province = 'Harare') AS limited_result LIMIT 50",
        )

    def test_unsafe_sql_raises(self):
        with self.assertRaises(ValueError):
            prepare_sql("DROP TABLE vw_school_directory;")


if __name__ == "__main__":
    unittest.main()
