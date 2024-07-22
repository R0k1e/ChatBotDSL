#include <cstring>

// 如果电话号码以"123"开始，则认为它在黑名单中
bool inBlackList(const char* number) {
    const char* blackListPrefix = "123";
    return strncmp(number, blackListPrefix, strlen(blackListPrefix)) == 0;
}