cmake_minimum_required(VERSION 3.10)
project(blockchain_monitor)

set(CMAKE_CXX_STANDARD 17)

find_package(ZeroMQ REQUIRED)
find_package(secp256k1 REQUIRED)

add_executable(daemon zmq_subscriber.cpp ecdsa_parser.cpp stats_engine.cpp)
target_link_libraries(daemon zmq secp256k1::secp256k1)