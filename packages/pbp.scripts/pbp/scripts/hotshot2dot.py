import sys
from pbp.scripts.hotshotmain import run
from pbp.scripts.gprof2dot import run_script

def main():
    if (sys.argv) != 2:
        print 'Usage: %s HOTSHOT_FILE' % sys.argv[0]

    filename = sys.argv[1]
    pstats = filename + '.pstats'
    ouput = filename + '.png' 

    # building the pstats file  
    run(filename, pstats)
    
    # calling graph2dot
    sys.argv = sys.argv[0] + ['-f', 'pstats', pstats, 
                              '|', 'dot', '-Tpng', '-o', output]

    run_script()

if __name__ == '__main__':
    main()

