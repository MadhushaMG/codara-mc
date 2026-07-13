import typing

class EventBus:
    def __init__(self):
        self._listeners = {}

    def on(self, event_name: str, callback: typing.Callable):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def emit(self, event_name: str, *args, **kwargs):
        if event_name in self._listeners:
            for listener in self._listeners[event_name]:
                listener(*args, **kwargs)

    def off(self, event_name: str, callback: typing.Callable):
        if event_name in self._listeners:
            try:
                self._listeners[event_name].remove(callback)
            except ValueError:
                pass

# Global event bus instance
event_bus = EventBus()
