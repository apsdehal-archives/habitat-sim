add_library(scene STATIC
  Mp3dSemanticScene.cpp
  Mp3dSemanticScene.h
  ObjectControls.cpp
  ObjectControls.h
  SceneConfiguration.cpp
  SceneConfiguration.h
  SceneGraph.cpp
  SceneGraph.h
  SceneManager.cpp
  SceneManager.h
  SceneNode.cpp
  SceneNode.h
  SemanticScene.h
  SuncgObjectCategoryMap.h
  SuncgSemanticScene.cpp
  SuncgSemanticScene.h
)

target_link_libraries(scene
  PUBLIC
    assets
    core
    geo
    gfx
    io
)
