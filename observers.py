class Subject:
    def __init__(self):
        print(self)
        self.observers = []
        self.event = None

    def subscribe(self, *observers):
        print(self.subscribe)
        for observer in observers:
            if observer not in self.observers:
                self.observers.append(observer)

    def unsubscribe(self, *observers):
        print(self.unsubscribe)
        for observer in observers:
            if observer in self.observers:
                self.observers.remove(observer)

    def notify(self, event):
        for observer in self.observers:
            observer.update(event)

class CreateObject:
    def __init__(self):
        pass

class Event:
    def __init__(self, kind=None, item=None, data=None):
        self.kind = kind
        self.item = item
        self.data = data
