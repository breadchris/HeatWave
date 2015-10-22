#include <stdio.h>
#include <time.h>

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

    srand(time(NULL));

    if (rand() % 2 == 0) {
        x += a();
    } else {
        x += b();
    }

    if (rand() % 2 == 0) {
        if (rand() % 2 == 0) {
            x += a() + b();
        } else {
            x += b();
            if (rand() % 2 == 0) {
                x += a() + b();
                printf("%d\n", x);
                return x;
            } else {
                x += b();
            }
        }
        x += c();
    } else {
        if (rand() % 2 == 0) {
            x += a() + b();
        } else {
            x += b();
            printf("%d\n", x);
            return x;
        }
        x += b();
    }

    if (rand() % 2 == 0) {
        x += c();
    } else if (rand() % 2 == 0) {
        printf("%d\n", x);
        return 5;
    } else {
        printf("%d\n", x);
        return 1;
    }

    printf("%d\n", x);
    return 42;
}
