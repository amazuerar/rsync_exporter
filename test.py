import unittest
from Parser import Parser


class TestParser(unittest.TestCase):

    def test_parser(self):
        """
        Testing parser
        """
        log = "2017/09/01 03:10:16 [17161] connect from 2001:db8:4f8:191:1056::2"
        log_dict = {"date": "2017/09/01", "timestamp": "03:10:16", "pid": "[17161]",
                    "description": "connect from 2001:db8:4f8:191:1056::2"}
        p = Parser()
        log_dict_result = p.parse_log(log)
        self.assertEqual(log_dict_result, log_dict)


if __name__ == '__main__':
    unittest.main()
