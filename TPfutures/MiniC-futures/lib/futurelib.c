#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include "../include/futurelib.h"

FutureInt *All[70]; 
// A table of future pointers to store all the futures created
// In a realistic scenario this would be a dynamic structure
int NbAll = 0;
// Number of futures created

typedef struct 
// A structure for the argument of thread creation: function pointer and parameter
{
  FutureInt *fut;
  int (*fun)(int);
  int param;
} arg_struct;

FutureInt *fresh_future_malloc()
{
  // TODO Exercise 4.2
  // Use malloc(sizeof(FutureInt)) and reference created futures
}

void print_futureInt(FutureInt *f)
{
  // TODO
  // For debug purposes only
}

void free_future(FutureInt *fut)
{
  free(fut);
}

void resolve_future(FutureInt *fut, int val)
{
  // TODO Exercise 5.1
  // Fill fut accordingly
}

int Get(FutureInt *fut)
{
  // TODO Exercise 5.2
  // Wait until future is resolved (do a sleep(1) between two checks)
  // Do not forget to do a pthread_join(fut->tid, NULL);
  return 0;
}

void *runTask(void *param)
{
  // TODO Exercise 4.1
  // function that is launched by the created thread: should call the function and
  //  deal with the future, using the function resolve_future
  // param can be cast to (arg_struct *)
  // this function should free the pointer param
  return NULL;
}

FutureInt *Async(int (*fun)(int), int p)
{
  // TODO Exercise 4.3
  // Main system call should be: int err = pthread_create(&fut->tid, NULL, &runTask, (args));
  // Allocate a future and space for arguments: args = malloc(sizeof(arg_struct));
  // Do not forget to populate args
  return NULL;
}

void freeAllFutures()
{
  // TODO Exercises 4.4 & 5.3
  // 1 - Wait for all futures (Get) to avoid dangling threads (Exercise 5.3)
  // 2 - Call free_future for all futures (Exercise 4.4)
}
