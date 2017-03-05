import unittest
from LogMonitor import LogMonitor

class LogInfoTests(unittest.TestCase):

    def setUp(self):
        self.test_data = ['222.64.146.118 - - [19/Jun/2005:06:45:17 +0200] "GET /wximages/wxwidgets02-small.png HTTP/1.1" 200 12468 "http://blog.vckbase.com/bastet/" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; TencentTraveler )"',
                    '218.84.191.50 - - [19/Jun/2005:06:46:05 +0200] "GET /wximages/wxwidgets02-small.png HTTP/1.1" 200 12468 "http://blog.vckbase.com/bastet/" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"',
                    '202.201.245.20 - - [19/Jun/2005:06:47:37 +0200] "GET /wximages/wxwidgets02-small.png HTTP/1.1" 200 12468 "http://blog.vckbase.com/bastet/" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"',
                    '138.243.201.10 - - [19/Jun/2005:06:48:40 +0200] "GET /wiki.pl?WxWidgets_Bounties HTTP/1.1" 200 8873 "http://www.wxwidgets.org/toolbar.htm" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.7.7) Gecko/20050414 Firefox/1.0.3"',
                    '68.251.52.253 - - [19/Jun/2005:06:50:49 +0200] "GET /wiki.pl?WxWidgets_Compared_To_Other_Toolkits HTTP/1.1" 200 19476 "http://www.google.com/search?q=wxWidget+designer" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.8) Gecko/20050511 Firefox/1.0.4"',
                    '68.251.52.253 - - [19/Jun/2005:06:50:49 +0200] "GET /wxwiki.css HTTP/1.1" 200 1540 "http://wiki.wxwidgets.org/wiki.pl?WxWidgets_Compared_To_Other_Toolkits" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.8) Gecko/20050511 Firefox/1.0.4"',
                    '68.251.52.253 - - [19/Jun/2005:06:50:49 +0200] "GET /wximages/wxwidgets02-small.png HTTP/1.1" 200 12468 "http://wiki.wxwidgets.org/wiki.pl?WxWidgets_Compared_To_Other_Toolkits" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.8) Gecko/20050511 Firefox/1.0.4"',
                    '68.251.52.253 - - [19/Jun/2005:06:50:50 +0200] "GET /favicon.ico HTTP/1.1" 200 3262 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.8) Gecko/20050511 Firefox/1.0.4"',
                    '61.177.31.179 - - [19/Jun/2005:06:52:36 +0200] "GET /wximages/wxwidgets02-small.png HTTP/1.1" 200 12468 "http://blog.vckbase.com/bastet/" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)"',
                    '216.148.248.43 - - [19/Jun/2005:06:53:14 +0200] "GET / HTTP/1.0" 200 3369 "-" "Mozilla/4.0 (compatible;)"',
                    '216.148.248.43 - - [19/Jun/2005:06:53:14 +0200] "GET /aa/bb/cc/dd/efg.ab HTTP/1.0" 300 3369 "-" "Mozilla/4.0 (compatible;)"']
        self.monitor = LogMonitor(3)

    def test_alert_change_low_to_high(self):
        self.monitor.add(self.test_data[4])
        self.monitor.add(self.test_data[5])
        self.monitor.add(self.test_data[6])
        self.assertFalse(self.monitor.alert)
        self.monitor.add(self.test_data[7])
        self.assertTrue(self.monitor.alert)

    def test_alert_change_high_to_low(self):
        self.monitor.add(self.test_data[4])
        self.monitor.add(self.test_data[5])
        self.monitor.add(self.test_data[6])
        self.monitor.add(self.test_data[7])
        self.assertTrue(self.monitor.alert)
        self.monitor.add(self.test_data[9])
        self.assertFalse(self.monitor.alert)

    def test_status_update(self):
        for data in self.test_data:
            self.monitor.add(data)
        status = {"200": 10, "300": 1}
        self.assertEqual(status, self.monitor.get_status_stats())


    def test_section_update(self):
        for data in self.test_data:
            self.monitor.add(data)
        sections = {"/": 5, "wximages": 5, "aa": 1}
        self.assertEqual(sections, self.monitor.get_section_stats())


def main():
    unittest.main()

if __name__ == '__main__':
    main()