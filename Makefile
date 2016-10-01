all: run

run: main.exe
	main.exe

main.exe: hello_world.o
	gcc -std=c99 -Wall -g hello_world.o -o main.exe

hello_world.o: hello_world.c
	gcc -std=c99 -Wall -g -c hello_world.c -o hello_world.o
