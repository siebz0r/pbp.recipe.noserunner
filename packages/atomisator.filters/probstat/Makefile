default:
	@echo 'This is just for testing, to build do'
	@echo 'python setup.py build'

all:
	python setup.py build

clean:
	rm -rf build/
	rm -f *~
	rm -f base/*~
	rm -f base/*\#
	rm -f include/*~
	rm -f include/*\#
	rm -f python/*~
	rm -f python/*\#
	rm -f test/*~
	rm -f test/*\#
	rm -f probstat.so

check:	all
	@echo Dont forget to try it both with and without Electric Fence
	rm -f test/probstat.so
	ln -s ../build/lib.linux-i686-2.2/probstat.so test/probstat.so
	python test/permute.py
	python test/combo.py
	python test/cartesian.py
	rm -f test/probstat.so

remake: clean all
