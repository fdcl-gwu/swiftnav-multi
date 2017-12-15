cmake_minimum_required(VERSION 2.8.9)
project(libsbp_example)

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

set(CMAKE_C_FLAGS "-Wall -Wextra -Wno-strict-prototypes -Wno-unknown-warning-option -Werror -std=gnu99 ${CMAKE_C_FLAGS}")

add_executable(read_rtk read_rtk.c)

find_package(PkgConfig)
pkg_check_modules(LIBSERIALPORT libserialport)
link_directories(${LIBSERIALPORT_LIBRARY_DIRS})
include_directories(${LIBSERIALPORT_INCLUDE_DIRS})

link_directories("/usr/local/lib/")
include_directories("/usr/local/include/")

target_link_libraries(read_rtk serialport sbp)
