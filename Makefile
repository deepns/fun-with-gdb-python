CC=clang
OBJS=tree.o
SRC=tree.c
APP=tree
CFLAGS=-g -c

tree: ${OBJS}
	${CC} -o ${APP} ${OBJS}
tree.o: ${SRC}
	${CC} ${CFLAGS} ${SRC}
clean:
	rm ${APP} *.o