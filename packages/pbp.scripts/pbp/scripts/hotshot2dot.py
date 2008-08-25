import sys
import os
import hotshot.stats
from pbp.scripts.gprof2dot import run_script

def main():
    if len(sys.argv) != 2:
        print 'Usage: %s HOTSHOT_FILE' % sys.argv[0]
        sys.exit(0)
    filename = sys.argv[1]
    s = hotshot.stats.load(filename)
    pstats = filename + '.pstats'
    
    # building the pstats file  
    s.dump_stats(pstats)
   
    try:
        # calling graph2dot
        sys.argv = [sys.argv[0], '-f', 'pstats', pstats] 
        run_script()
    finally:
        os.remove(pstats)

if __name__ == '__main__':
    main()

