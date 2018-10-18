# object files
OBJS=1D_Array_v03.o utility.o
OBJS2=test.o
CXXFLAGS=-std=c++11
LDFLAGS=-lm
CC=g++
all:1D_Array_v03.out test.out

1D_Array_v03.out: $(OBJS)
	$(CC) -o $@ $(OBJS) $(LDFLAGS)

test.out: $(OBJS2)
	$(CC) -o $@ $(OBJS2) $(CXXFLAGS)

clean:
	rm -f $(OBJS) 1D_Array_v03.out test.out
