#include<stdio.h>
int a() {
    return 4;
}

int b() {
    return a() + 5;
}

int c() {
    return b() + a();
}

int main() {
    int x = 0;
    if (x > 1) {
        x += a();
    } else {
        x += b();
    }

    if (x > 2) {
        x += c();
    } else if (x == 3) {
        printf("%d\n", x);
        return 5;
    } else {
        printf("%d\n", x);
        return 1;
    }

    printf("%d\n", x);
    return 42;
}
