#include <iostream>
#include "jansson.h"

int main() {
    const char *s = "{\"hello\": \"world\"}";
    json_t *j = json_loads(s, JSON_DECODE_ANY, NULL);
    const char *key;
    json_t *value;
    json_object_foreach(j, key, value) {
        printf("%s, %s\n", key, json_string_value(value));
    }
}
