from observers import Subject
from datetime import datetime
from os import system
import time

class CreateLogger(Subject):
    def __init__(self):
        super().__init__()
        self.name = "logger"

    def update(self, event):
        self.event = event

    def logs(self, user):
        while True:
            self.datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if user.trading.status == "bought":
                status_color = "\033[0;32m"
            else:
                status_color = "\033[0;31m"

            if user.trading.proffit > 0:
                proffit_color = "\033[0;32m"
            elif user.trading.proffit == 0:
                proffit_color = "\033[0;34m"
            else:
                proffit_color = "\033[0;31m"

            time.sleep(.5)
            system("clear")
            print(
                    f"{self.datetime}\n",
                    f"{user.stablecoin.name} qty: {user.stablecoin.quantity:.2f}",
                    f"{user.asset.name} qty: {user.asset.quantity}",
                    f"{user.asset.name} converted to {user.stablecoin.name}: {user.asset.converted:.2f}",
                    f"{user.stablecoin.name} total: {user.stablecoin.total:.2f}\n",
                    f"Trading status: {user.trading.status}",
                    f"{user.asset.name} price: {user.asset.price:.2f}",
                    f"rsi: {user.trading.rsi:.2f}",
                    f"proffit: {user.trading.proffit:.2%}\n\n",
                    f"\033[0;33m{self.event}\033[0;0m",
                    sep="\n"
                )
