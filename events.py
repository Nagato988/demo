#!/usr/bin/env python3

from collections import defaultdict


class EventEmitter:
    def __init__(self):
        self._handlers = defaultdict(list)

    def on(self, event, callback):
        self._handlers[event].append(callback)

    def emit(self, event, *args):
        for callback in list(self._handlers.get(event, [])):
            callback(*args)

    def off(self, event, callback):
        handlers = self._handlers.get(event)
        if not handlers:
            return
        try:
            handlers.remove(callback)
        except ValueError:
            return
        if not handlers:
            del self._handlers[event]
