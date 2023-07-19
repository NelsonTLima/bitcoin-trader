from observers import Subject, Event
from binance import Binance
import requests

class CreateAgent(Subject):
    def __init__(self, name="Agent"):
        super().__init__()
        self.name = name

    def ask(self, url):
        response = None
        while response == None:
            try:
                response = requests.get(url, headers=Binance.HEADERS, timeout=2).json()
            except:
                pass
        return response

    def tell(self, url):
        response = None
        while response == None:
            try:
                response = requests.post(url, headers=Binance.HEADERS, timeout=2).json()
            except:
                pass
        return response

    def update(self, event):
        if event.kind == "request":
            match event.item:
                case "balances":
                    data = self.ask(Binance().account)["balances"]
                case "klines":
                    data = self.ask(Binance(15).klines)
                case "buy":
                    quantity = event.data
                    self.tell(Binance(quantity).buy)
                    data = "Post sent."
                case "sell":
                    quantity = event.data
                    self.tell(Binance(quantity).sell)
                    data = "Post sent"
                case _:
                    data = None
            if data != None:
                event = Event("inform", event.item, data)
                self.notify(event)

if __name__ == "__main__":
    pass
