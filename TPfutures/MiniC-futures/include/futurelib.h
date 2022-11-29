#include <pthread.h>

typedef struct  // a struct for storing a future to int
{
  int Id;
  int Value;
  int resolved;
  pthread_t tid;
} FutureInt;

typedef FutureInt* futint; // a typedef to deal with the future type of MiniCFut

FutureInt *fresh_future_malloc(); // allocates (malloc) a fresh future and initializes its field

void print_futureInt(FutureInt *fut); // for debug purposes: print a fut int status

void free_future(FutureInt *fut); // frees the pointer allocated by fresh_future

void resolve_future(FutureInt *fut, int val); // function called when an async call is finished

int Get(FutureInt *fut); 
// called by the main program: 
// checks that the future is resolved and 
// returns the value stored in the future

FutureInt *Async(int (*fun)(int), int p);
// asynchronous function call:
// takes a function pointer as parameter and the fun call parameter as second parameter
// returns an unresolved future
// creates a thread to perform the asynchronous function call

void freeAllFutures();
// called at the end of the main block: waits for the resolution of all futures 
// and frees all future pointers created by fresh_future
