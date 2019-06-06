#include "cpp_executor.h"

int main(int nbArg, char** argTab) {
    CppExecutor executor("c++14");
    executor.give_args(nbArg, argTab);
    return executor.exec();
}