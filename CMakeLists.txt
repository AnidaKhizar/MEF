cmake_minimum_required(VERSION 2.8)
project(Importer)
set(CMAKE_BUILD_TYPE "Release")
find_package(VTK REQUIRED)
include(${VTK_USE_FILE})
include_directories(".")

add_executable(Importer
  Importer.cpp)
set_target_properties(Importer
  PROPERTIES
  COMPILE_FLAGS
  "-march=native -O3 -std=c++11")
  
target_link_libraries(Importer
  ${VTK_LIBRARIES})

install(TARGETS Importer RUNTIME DESTINATION bin)
