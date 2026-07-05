import random
import faker
import json

fake = faker.Faker()


class CLF:
    def __init__(self):
        self.clientIP = fake.ipv4()
        self.remoteLogName = "-"
        self.username = random.choice([fake.user_name(), "-"])
        self.method = random.choice(["GET", "POST", "PUT", "DELETE"])
        self.category = random.choice(["blog", "products", "test", "explore"])
        self.path = fake.uri_path(deep=random.randint(1, 3))
        self.requestLine = f"{self.method} /{self.category}/{self.path}.html HTTP/1.1"
        self.responseCode = random.choice([200, 301, 302, 404, 500])
        self.size = int(round(random.triangular(100, 5000, 250), 0))
        self.logEntry = f"{self.clientIP} {self.remoteLogName} {self.username} {self.requestLine} {self.responseCode} {self.size}"
        match self.responseCode:
            case 200:
                self.logLevel = 20
            case 301 | 302:
                self.logLevel = 30
            case 404:
                self.logLevel = 40
            case 500:
                self.logLevel = 50

    def generate_log_entry(self):
        return self.logEntry, self.logLevel


class RFC5424:
    def __init__(self):
        self.facility = random.randint(0, 23)
        self.severity = random.randint(0, 7)
        self.prival = str(int(self.facility) * 8 + int(self.severity))
        self.tag = random.choice(["ftp", "httpd", "mail"])
        self.logEntry = f"{fake.domain_name()} requested by {fake.ipv4_public()}"
        match self.severity:
            case 0 | 1 | 2:
                self.logLevel = 50
            case 3:
                self.logLevel = 40
            case 4:
                self.logLevel = 30
            case 5:
                self.logLevel = 20
            case 6 | 7:
                self.logLevel = 10

    def generate_log_entry(self):
        return self.logEntry, self.logLevel, self.prival, self.tag


class JSON:
    def __init__(self):
        self.username = fake.user_name()
        self.ip = fake.ipv4_public()
        self.logEntry = f"User {self.username} logged in from {self.ip}"
        self.logLevel = random.choice([10, 20, 30, 40, 50])

    def generate_log_entry(self):
        return json.loads(f"""
        {{"msg": "{self.logEntry}", "level": {self.logLevel}, "sourceip": "{self.ip}",
        "username": "{self.username}"}}
        """)


class stockTX:
    def __init__(self):
        self.traderID = random.sample(
            ["Gavin", "Tracey", "Simon", "Dylan", "Gertrude"], 2
        )
        self.stockSymbol = random.choice(["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"])
        self.transactionType = random.sample(["BUY", "SELL"], 2)
        self.quantity = random.randint(1, 100)
        self.price = round(random.uniform(100, 1500), 4)
        self.logEntry = (
            f"{self.traderID[0]} performed action {self.transactionType[0]}, {self.traderID[1]} performed action {self.transactionType[1]} "
            f"for {self.quantity} shares of {self.stockSymbol} at ${self.price} each"
        )
        match (self.quantity):
            case i if i > 80:
                self.logLevel = 30
            case _:
                self.logLevel = 20

    def generate_log_entry(self):
        return json.loads(f"""
        {{"msg": "{self.logEntry}", "level": {self.logLevel}, 
        "party1": {{"traderID": "{self.traderID[0]}", "transactionType": "{self.transactionType[0]}"}}, 
        "party2": {{"traderID": "{self.traderID[1]}", "transactionType": "{self.transactionType[1]}"}}, 
        "stockSymbol": "{self.stockSymbol}", "quantity": {self.quantity}, "price": {self.price}}}
        """)


if __name__ == "__main__":
    CLFlog = CLF().generate_log_entry()
    print(f"CLF Log: {CLFlog[0]}")

    RFC5424log = RFC5424().generate_log_entry()
    print(f"RFC5424 Log: {RFC5424log[0]}")

    JSONlog = JSON().generate_log_entry()
    print(f"JSON Log: {JSONlog[0]}")

    stockTXlog = json.dumps(stockTX().generate_log_entry())
    print(f"Stock Transaction Log: {stockTXlog}")
