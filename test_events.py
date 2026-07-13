import unittest
from events import EventBus

class TestEventBus(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()
        self.call_count = 0
        self.last_args = None

    def handler(self, *args, **kwargs):
        self.call_count += 1
        self.last_args = args

    def test_on_and_emit(self):
        self.bus.on('TEST_EVENT', self.handler)
        self.bus.emit('TEST_EVENT', 'foo', 42)
        
        self.assertEqual(self.call_count, 1)
        self.assertEqual(self.last_args, ('foo', 42))

    def test_multiple_listeners(self):
        call_count2 = [0]
        def handler2(*args):
            call_count2[0] += 1

        self.bus.on('TEST_EVENT', self.handler)
        self.bus.on('TEST_EVENT', handler2)
        
        self.bus.emit('TEST_EVENT', 'bar')
        
        self.assertEqual(self.call_count, 1)
        self.assertEqual(call_count2[0], 1)

    def test_off(self):
        self.bus.on('TEST_EVENT', self.handler)
        self.bus.off('TEST_EVENT', self.handler)
        
        self.bus.emit('TEST_EVENT', 'bar')
        
        self.assertEqual(self.call_count, 0)

if __name__ == '__main__':
    unittest.main()
