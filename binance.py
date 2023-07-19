from os import environ
import dotenv, time, hmac, hashlib
dotenv.load_dotenv()

class Binance:
    API_KEY = environ["API_KEY"]

    HEADERS = {
        "X-MBX-APIKEY": API_KEY
        }

    def __init__(self, quantity=None, symbol="BTCBUSD", interval="15m"):
        SECRET_KEY = environ["SECRET_KEY"]
        DOMAIN = "https://api.binance.com/"
        timestamp = int(time.time()*(10**3))

        class ENDPOINT:
            price = "api/v3/ticker/bookTicker"
            klines = "api/v3/klines"
            day = "api/v3/ticker/24hr"
            account = "api/v3/account"
            order = "api/v3/order/test"
            allOrders = "api/v3/allOrders"

        class PARAMS:
            account = f'timestamp={timestamp}'
            klines = f'symbol={symbol}&interval={interval}&limit={quantity}'
            buy = f"symbol={symbol}&side=BUY&type=MARKET&quantity={quantity}&timestamp={timestamp}"

        sign = lambda params : "&signature=" + hmac.new(
                    SECRET_KEY.encode('ASCII'),
                    params.encode('ASCII'),
                    hashlib.sha256).hexdigest()

        self.klines = DOMAIN + ENDPOINT.klines + "?" + PARAMS.klines
        self.account = DOMAIN + ENDPOINT.account + "?" + PARAMS.account + sign(PARAMS.account)
        self.buy = DOMAIN + ENDPOINT.order + "?" + PARAMS.buy + sign(PARAMS.buy)
