set(viewer_SOURCES viewer.cpp)

#set_directory_properties(PROPERTIES CORRADE_USE_PEDANTIC_FLAGS ON)
add_executable(viewer ${viewer_SOURCES})

target_link_libraries(viewer
  PRIVATE
    assets
    gfx
    nav
    scene
)

# copy JS/HTML/CSS scaffolding for WebGL build
if(CORRADE_TARGET_EMSCRIPTEN)
  install(FILES
      viewer.html
      ${MAGNUM_EMSCRIPTENAPPLICATION_JS}
      ${MAGNUM_WEBAPPLICATION_CSS}
      DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
endif()
