from Event import Event
class EventExtended(Event):
    def __lt__(self, other):
        return self.id< other.id