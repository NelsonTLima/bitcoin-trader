from observers import Subject, Event, CreateObject
from datetime import datetime

class CreateDataStore(Subject):
    def __init__(self, name="DataStorage"):
        super().__init__()
        self.name = name
        self.balances = None

        self.trading = CreateObject()
        self.trading.status = ""
        self.trading.klines = None
        self.trading.rsi = 0
        self.trading.proffit = 0

        self.asset = CreateObject()
        self.asset.name = "BTC"
        self.asset.price = 0
        self.asset.quantity = 0
        self.asset.converted = 0

        self.stablecoin = CreateObject()
        self.stablecoin.name = "BUSD"
        self.stablecoin.quantity = 0
        self.stablecoin.total = 0

    def update_datetime(self):
        self.datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def format_asset(self, qty, price):
        split_number = str(qty).split(".")
        int_part , float_part = split_number[0], split_number[1]
        j = 0
        float_list=[]
        for i in range(0,len(float_part)):
            float_number = int_part + "." + j*"0" + float_part[j:i+1]
            j += 1
            if float(float_number) > 0 and (float(float_number) * price) > 0.1:
                float_list.append(float(float_number))
        return sum(float_list)

    def collect_data(self):
        event = Event("request", "balances")
        self.notify(event)
        event = Event("request", "klines")
        self.notify(event)
        event = Event("request", "rsi", self.trading.klines)
        self.notify(event)
        event = Event("request", "convertion", [self.asset.quantity, self.asset.price])
        self.notify(event)

    def infer_status(self):
        if self.stablecoin.quantity > self.asset.converted:
            self.trading.status = "sold"
        else:
            self.trading.status = "bought"

    def update(self, event):
        if event.kind == "inform":
            match event.item:
                case "klines":
                    self.trading.klines = event.data
                    self.asset.price = float(event.data[-1][4])
                case "rsi":
                    self.trading.rsi = event.data
                case "balances":
                    for asset in event.data:
                        if asset["asset"] == self.asset.name:
                            self.asset.quantity = self.format_asset(float(asset["free"]), float(self.asset.price))
                        elif asset["asset"] == self.stablecoin.name:
                            self.stablecoin.quantity = float(asset["free"])
                case "convertion":
                    self.asset.converted = event.data
                    self.stablecoin.total = event.data + self.stablecoin.quantity
        self.infer_status()
        self.update_datetime()

if __name__ == "__main__":
    pass
