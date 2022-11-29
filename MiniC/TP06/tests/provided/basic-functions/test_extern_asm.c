// Call to external functions written in assembly

int print_42();

int main() {
	int dummy;
	dummy = print_42();
	return 0;
}

// EXPECTED
// 42
// LINKARGS $dir/lib/_print42.s
