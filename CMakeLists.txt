cmake_minimum_required(VERSION 3.15)
project(ProceduralAnimation)

set(CMAKE_CXX_STANDARD 17)

# Main library
add_library(SecondOrderSystem STATIC
    src/SecondOrderSystem.cpp
    src/SecondOrderSystem.h
)

# Example executable
add_executable(AnimationExample
    src/main.cpp
)

target_link_libraries(AnimationExample SecondOrderSystem)