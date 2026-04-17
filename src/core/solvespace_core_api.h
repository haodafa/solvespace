#ifndef SOLVESPACE_CORE_API_H
#define SOLVESPACE_CORE_API_H

#ifdef _WIN32
    #ifdef SOLVESPACE_CORE_EXPORTS
        #define SOLVESPACE_CORE_API __declspec(dllexport)
    #else
        #define SOLVESPACE_CORE_API __declspec(dllimport)
    #endif
#else
    #define SOLVESPACE_CORE_API __attribute__((visibility("default")))
#endif

#endif // SOLVESPACE_CORE_API_H