// Call to external functions

int print_hello();

int main() {
	int dummy;
	dummy = print_hello();
	return 0;
}

// EXPECTED
// Hello, world!
// LINKARGS $dir/lib/_hello.c
