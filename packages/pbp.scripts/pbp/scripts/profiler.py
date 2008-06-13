import time
import sys
from test import pystone
from guppy import hpy

benchtime, stones = pystone.pystones()

def secs_to_kstones(seconds):
    return (stones*seconds) / 1000 

stats = {}

def reset_stats():
    global stats
    stats = {}

def print_stats():
    template = '%s : %.2f kstones, %.3f secondes, %.3d bytes'
    for key, v in stats.items():
        print template % (key, v['stones'], v['time'], v['memory'])

if sys.platform == 'win32':
    timer = time.clock
else:
    timer = time.time

def profile(name='stats', stats=stats):
    """Calculates a duration and a memory size."""
    def _profile(function):
        def __profile(*args, **kw):
            start_time = timer()
            profiler = hpy()
            profiler.setref()        
            start = profiler.heap().size + 12
            try:
                return function(*args, **kw)
            finally:
                total = timer() - start_time
                kstones = secs_to_kstones(total)
                memory = profiler.heap().size - start
                stats[name] = {'time': total, 
                               'stones': kstones,  
                               'memory': profiler.heap().size}
        return __profile
    return _profile

REPEAT = 100

def memory_grow(function, *args, **kw):
    """checks if a function makes the memory grows"""
    profiler = hpy()
    profiler.setref() 
    start = profiler.heap().size + 12
    for i in range(REPEAT):
        function(*args, **kw)
    return profiler.heap().size - start  
    
