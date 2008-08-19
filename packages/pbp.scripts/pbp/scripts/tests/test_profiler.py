from pbp.scripts import profiler
import time
from nose.tools import *
import random

def test_profile():
    
    # let's try the decorator
    @profiler.profile(name='tested')
    def tested():
        time.sleep(0.25)

    tested()

    # let's check what we got
    res = profiler.stats['tested']
    
    assert res['stones']< 600
    assert res['memory'] < 1000

def test_memory_grow():
    
    growing = []

    def stable():
        memory = []
        def _get_char():
            return chr(random.randint(97, 122))
        for i in range(100):
            size = random.randint(20, 150)
            data = [_get_char() for i in range(size)]
            memory.append(''.join(data))
        return '\n'.join(memory)

    def unstable():
        growing.append(stable())

    assert profiler.memory_grow(stable) <= 500
    assert profiler.memory_grow(unstable) > 850000
    

