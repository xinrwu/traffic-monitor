import re

class LogInfo(object):


    def __init__(self, data):
        """Parse Common Log Format string into separate fields.

        Args:
            data (str): Common Log Format string
        Raises:
            ValueError: If data is not in Common Log Format
        """
        self.log_data = dict()
        self._parse_data(data)

    def get_ip(self):
        """Returns the ip address.
        """
        return self.log_data["ip_address"]

    def get_datetime(self):
        """Returns the date and time concatenated.
        """
        return self.log_data["datetime"]

    def get_status(self):
        """Returns the status code.
        """
        return self.log_data["status"]

    def get_resource(self):
        """Returns the resource.
        """
        return self.log_data["resource"]

    def get_section(self):
        """Returns the section the web page is from.
        """
        return self.log_data["section"]

    def get_bytes(self):
        """Returns the size of object in bytes returned to the client.
        """
        return self.log_data["bytes"]

    def get_data(self):
        """Returns the data parsed as a dictionary from the line in log file.
        """
        return self.log_data

    def _parse_data(self, data):
        pattern = re.compile(r'([(\d\.)]+) ' # ip address
                             r'- - ' # user-identifier and userid
                             r'\[(.*?) ([\+|\-][\d]+)\] ' # datetime, timezone
                             r'"([A-z]+) ([\S]+) ([A-z]+\/[\d.]+)" ' # method, source, HTTP protocol
                             r'(\d+) ' # HTTP status code
                             r'([\d|-]+)') # size of object returned to the client
        match = pattern.match(data)
        if match is None:
            raise ValueError(data)
        self.log_data["ip_address"] = match.group(1)
        self.log_data["datetime"] = match.group(2)
        self.log_data["zone"] = match.group(3)
        self.log_data["method"] = match.group(4)
        self.log_data["resource"] = match.group(5)
        self.log_data["section"] = self._make_section(self.log_data["resource"])
        self.log_data["protocol"] = match.group(6)
        self.log_data["status"] = match.group(7)
        self.log_data["bytes"] = match.group(8)

    def _make_section(self, resource):
        sections = resource.split('/')
        if len(sections) <= 2:
            return '/'
        else:
            return sections[1]
