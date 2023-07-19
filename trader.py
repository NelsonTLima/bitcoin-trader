from observers import Subject, Event

class CreateTrader(Subject):
    def __init__(self, name="Trader"):
        super().__init__()
        self.name = name
        self.status = "sold"
        self.klines = 0
        self.price = 0
        self.rsi = 0
        self.stablecoin_avaliable = 0
        self.sellable_asset = 0

    def trade():
        if rsi < 30:
            event = Event("request", "stablecoin avaliable")
            self.notify(event)
            event = Event("request", "buy", self.stablecoin_avaliable)
        else:
            event = Event("request", "sellable quantity")
            self.notify(event)
            event = Event("request", "sell", self.sellable_asset)
            self.notify(event)

    def update(self, event):
        if event.kind == "response":
            match event.item:
                case "klines":
                    self.klines = event.data
                    self.price = float(event.data[-1][4])
                case "rsi":
                    self.rsi = event.data
                case "stablecoin avaliable":
                    self.stablecoin_avaliable = event.data
                case "sellable quantity":
                    self.sellable_asset = event.data
        self.update_datetime()
