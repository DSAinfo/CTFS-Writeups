#include <stdio.h>
#include <unistd.h>

int main(void) {
    if (setuid(0) != 0) {
        perror("setuid");
        return 1;
    }

    FILE *f = fopen( "/flag.txt", "r");
    if (f == NULL) {
        perror("fopen");
        return 1;
    }

    char buf[512];
    size_t n;
    while ((n = fread(buf, 1, sizeof(buf), f)) > 0) {
        fwrite(buf, 1, n, stdout);
    }

    fclose(f);
    return 0;
}
