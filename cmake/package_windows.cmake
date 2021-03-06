#######################################################################
# CPACK configuration

set(CPACK_PACKAGE_VERSION ${NGSOLVE_VERSION_MAJOR}.${NGSOLVE_VERSION_MINOR}.${NGSOLVE_VERSION_PATCH})
if(NGSOLVE_VERSION_TWEAK)
    set(CPACK_PACKAGE_VERSION ${CPACK_PACKAGE_VERSION}.${NGSOLVE_VERSION_TWEAK})
endif(NGSOLVE_VERSION_TWEAK)

set(CPACK_INSTALLED_DIRECTORIES ${CPACK_INSTALLED_DIRECTORIES} ${CMAKE_BINARY_DIR}/netgen/dependencies/src/project_win_tcltk netgen)
set(CPACK_INSTALLED_DIRECTORIES ${CPACK_INSTALLED_DIRECTORIES} ${CMAKE_BINARY_DIR}/netgen/dependencies/src/project_win_zlib netgen)
if(USE_OCC)
    set(CPACK_INSTALLED_DIRECTORIES ${CPACK_INSTALLED_DIRECTORIES} ${CMAKE_BINARY_DIR}/netgen/tcl/src/win_download_occ netgen)
endif(USE_OCC)

if(USE_CGNS)
    set(CPACK_INSTALLED_DIRECTORIES ${CPACK_INSTALLED_DIRECTORIES} ${CMAKE_BINARY_DIR}/netgen/dependencies/src/project_win_cgns netgen)
endif(USE_CGNS)

set(CPACK_COMPONENT_GROUP_GROUP_NETGEN_DISPLAY_NAME "Netgen")
set(CPACK_COMPONENT_NETGEN_GROUP "group_netgen")
set(CPACK_COMPONENT_NETGEN_DEVEL_GROUP "group_netgen")
set(CPACK_COMPONENT_NETGEN_TUTORIAL_GROUP "group_netgen")

set(CPACK_COMPONENT_NETGEN_DISPLAY_NAME "Runtime")
set(CPACK_COMPONENT_NETGEN_DEVEL_DISPLAY_NAME "Development files")
set(CPACK_COMPONENT_NETGEN_TUTORIAL_DISPLAY_NAME "Tutorials")

set(CPACK_COMPONENT_NETGEN_DEVEL_DEPENDS netgen)
set(CPACK_COMPONENT_NETGEN_TUTORIAL_DEPENDS netgen)

set(CPACK_COMPONENT_GROUP_GROUP_NGSOLVE_DISPLAY_NAME "NGSolve")
set(CPACK_COMPONENT_NGSOLVE_GROUP "group_ngsolve")
set(CPACK_COMPONENT_NGSOLVE_DEVEL_GROUP "group_ngsolve")
set(CPACK_COMPONENT_NGSOLVE_TUTORIAL_GROUP "group_ngsolve")

set(CPACK_COMPONENT_NGSOLVE_DISPLAY_NAME "Runtime")
set(CPACK_COMPONENT_NGSOLVE_DEVEL_DISPLAY_NAME "Development files")
set(CPACK_COMPONENT_NGSOLVE_TUTORIAL_DISPLAY_NAME "Tutorials")

set(CPACK_COMPONENT_NGSOLVE_DEPENDS netgen)
set(CPACK_COMPONENT_NGSOLVE_DEVEL_DEPENDS ngsolve)
set(CPACK_COMPONENT_NGSOLVE_TUTORIAL_DEPENDS ngsolve)


# WIX packager
set(CPACK_WIX_PRODUCT_GUID 05BC95C0-440F-4D34-81DF-F54F966EC51E)
set(CPACK_WIX_UPGRADE_GUID 5618ABB2-B105-4FEA-9A01-0E1094DC91FF)

set(CPACK_GENERATOR "WIX")
set(CPACK_WIX_PROGRAM_MENU_FOLDER "NGSolve-v${NGSOLVE_VERSION}" )
set(CPACK_PACKAGE_INSTALL_DIRECTORY "ngsolve-v${NGSOLVE_VERSION}")

set(resources_dir ${CMAKE_SOURCE_DIR}/cmake/resources)
set(CPACK_WIX_PATCH_FILE ${resources_dir}/wix_patch.xml)
set(CPACK_RESOURCE_FILE_LICENSE ${resources_dir}/LICENSE.txt)
set(CPACK_PACKAGE_EXECUTABLES ${CPACK_PACKAGE_EXECUTABLES} "netgen" "Netgen")
set(CPACK_WIX_PRODUCT_ICON ${resources_dir}/netgen.ico)
set(CPACK_WIX_UI_BANNER ${resources_dir}/banner.bmp)
set(CPACK_WIX_UI_DIALOG ${resources_dir}/sculpture312_50.bmp)
set(CPACK_WIX_TEMPLATE ${resources_dir}/WIX.template.in)
set(CPACK_PACKAGE_FILE_NAME "NGSolve-${NGSOLVE_VERSION}")
#     if(USE_OCC)
#       set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_FILE_NAME}-OCC")
#     endif(USE_OCC)
if( CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_FILE_NAME}-win64")
else( CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_FILE_NAME}-win32")
endif( CMAKE_SIZEOF_VOID_P EQUAL 8)

