import unittest
from LogInfo import LogInfo

class LogInfoTests(unittest.TestCase):

    def setUp(self):
        mock_log = dict()
        mock_log["ip_address"] = "222.64.146.118"
        mock_log["datetime"] = "19/Jun/2005:06:44:17"
        mock_log["zone"] = "+0200"
        mock_log["method"] = "GET"
        mock_log["resource"] = "/wximages/wxwidgets02-small.png"
        mock_log["section"] = "wximages"
        mock_log["protocol"] = "HTTP/1.1"
        mock_log["status"] = "200"
        mock_log["bytes"] = "12468"
        self.mock_log = mock_log
        mock_data = ('222.64.146.118 - - [19/Jun/2005:06:44:17 +0200] '
                     '"GET /wximages/wxwidgets02-small.png HTTP/1.1" 200 12468 '
                     '"http://blog.vckbase.com/bastet/" "Mozilla/4.0 '
                     '(compatible; MSIE 6.0; Windows NT 5.1; SV1; TencentTraveler )"'
                    )
        self.mock_data = mock_data

    def test_parse_data(self):
        log = LogInfo(self.mock_data)
        self.assertEqual(log.log_data, self.mock_log)
        with self.assertRaises(ValueError):
            LogInfo("")

def main():
    unittest.main()

if __name__ == '__main__':
    main()
    