from observers import Subject, Event

class CreateCalculator(Subject):
    def __init__(self, name="calculator"):
        super().__init__()
        self.name = name

    def calculate_rsi(self, klines):
        # Step 1
        data_a, data_b = klines[0:14], klines[1:15]
        raising_closes, reducing_closes = [], []
        for kline in data_a:
            open_price, close_price = float(kline[1]), float(kline[4])
            if open_price < close_price:
                raising_closes.append(-1 + close_price/open_price)
            else:
                reducing_closes.append(-1 + open_price/close_price)
        previous_gain = self.calculate_average(raising_closes)
        previous_loss = self.calculate_average(reducing_closes)

        # Step 2
        raising_closes, reducing_closes = [], []
        for kline in data_b:
            open_price, close_price = float(kline[1]), float(kline[4])
            if open_price < close_price:
                raising_closes.append(-1 + close_price/open_price)
            else:
                reducing_closes.append(-1 + open_price/close_price)
        avg_gain = self.calculate_average(raising_closes)
        avg_loss = self.calculate_average(reducing_closes)

        # Step 3
        try:
            rs = ((previous_gain * 13) + avg_gain)/((previous_loss * 13) + avg_loss)
            rsi = 100 - (100/(1+ rs))
        except:
            rsi = None

        return rsi

    def calculate_average(self, array):
        if len(array) != 0:
            average = sum(array)/len(array)
        else:
            average = 0
        return average

    def convert(self, asset, price):
        return asset * price

    def deconvert(self, asset, price):
        return asset / price

    def infer_price(self, asset_a, asset_b):
        return asset_a / asset_b

    def update(self, event):
        if event.kind == "request":
            match event.item:
                case "rsi":
                    data = self.calculate_rsi(event.data)
                case "convertion":
                    data = self.convert(event.data[0],event.data[1])
                case _:
                    data = None
            if data != None:
                event = Event("inform", event.item, data)
                self.notify(event)
