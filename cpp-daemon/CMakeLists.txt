cmake_minimum_required(VERSION 3.10)
project(blockchain_monitor)

set(CMAKE_CXX_STANDARD 17)

find_package(PkgConfig REQUIRED)
pkg_check_modules(ZeroMQ REQUIRED libzmq)
pkg_check_modules(libsecp256k1 REQUIRED libsecp256k1)  # ← Nama harus SAMA

include_directories(${ZeroMQ_INCLUDE_DIRS} ${libsecp256k1_INCLUDE_DIRS})
link_libraries(${ZeroMQ_LDFLAGS} ${libsecp256k1_LDFLAGS})

add_executable(daemon zmq_subscriber.cpp ecdsa_parser.cpp stats_engine.cpp)