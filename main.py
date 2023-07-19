from agent import CreateAgent
from calculator import CreateCalculator
from dataStore import CreateDataStore
from logger import CreateLogger
from observers import Subject, Event
from threading import Thread
import time

# Creating subjects:
agent = CreateAgent()
calculator = CreateCalculator()
data_store = CreateDataStore()
#trader = CreateTrader()  <---
logger = CreateLogger()

# Subscribing observers:
agent.subscribe(data_store, logger) # add trader.
calculator.subscribe(data_store, logger) # add trader.
data_store.subscribe(agent, calculator, logger) #add trader.

observers = [agent, calculator, data_store]

# Creating a another data store to remember the starting data:
starting = CreateDataStore("starting data")

for subject in observers:
    subject.subscribe(starting)
    starting.subscribe(subject)
starting.collect_data()

for subject in observers:
    subject.unsubscribe(starting)

# Starting logger thread:
logger_thread = Thread(target=logger.logs, args=[data_store])
logger_thread.start()

# Start trading:
while True:
    time.sleep(.5)
    data_store.collect_data()
#trader.trade()
