

int f() {return 42;}

int f();

int main(){
  int dummy;
  dummy = f();
  return 0;
}

// EXPECTED
// EXITCODE 0