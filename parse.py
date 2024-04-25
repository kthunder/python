import xmltodict
from pprint import pprint
import re
import os
from jinja2 import Template

cmake_template = '''
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_VERSION 1)
set(CMAKE_SYSTEM_PROCESSOR arm)
cmake_minimum_required(VERSION 3.27)

set(ARCH armv7e-m)
set(CPU  cortex-m4)

# cmake -S . -B build -G "MinGW Makefiles" ; cmake --build build

# set jobs
set(CMAKE_BUILD_PARALLEL_LEVEL 12)

# specify cross-compilers and tools
set(COMPILER GNU)

if(COMPILER STREQUAL GNU)
    set(COMPILER_PATH        C:/IDE/ThinkTechStudio/toolchain/xpack-arm-none-eabi-gcc-10.3.1-2.3/bin)
    set(CMAKE_C_COMPILER     ${COMPILER_PATH}/arm-none-eabi-gcc.exe)
    set(CMAKE_CXX_COMPILER   ${COMPILER_PATH}/arm-none-eabi-g++.exe)
    set(CMAKE_ASM_COMPILER   ${COMPILER_PATH}/arm-none-eabi-gcc.exe)
    set(CMAKE_AR             ${COMPILER_PATH}/arm-none-eabi-ar.exe)
    set(CMAKE_OBJCOPY        ${COMPILER_PATH}/arm-none-eabi-objcopy.exe)
    set(CMAKE_OBJDUMP        ${COMPILER_PATH}/arm-none-eabi-objdump.exe)
    set(SIZE                 ${COMPILER_PATH}/arm-none-eabi-size.exe)
elseif(COMPILER STREQUAL LLVM)
    set(COMPILER_PATH        C:/IDE/ThinkTechStudio/toolchain/LLVMEmbeddedToolchainForArm-17.0.1-Windows-x86_64/bin)
    set(CMAKE_C_COMPILER     ${COMPILER_PATH}/clang.exe)
    set(CMAKE_CXX_COMPILER   ${COMPILER_PATH}/clang++.exe)
    set(CMAKE_ASM_COMPILER   ${COMPILER_PATH}/clang.exe)
    set(CMAKE_AR             ${COMPILER_PATH}/aarch32-ar.exe)
    set(CMAKE_OBJCOPY        ${COMPILER_PATH}/aarch32-objcopy.exe)
    set(CMAKE_OBJDUMP        ${COMPILER_PATH}/aarch32-objdump.exe)
    set(SIZE                 ${COMPILER_PATH}/aarch32-size.exe)
elseif(COMPILER STREQUAL HighTEC)
    set(COMPILER_PATH        C:/IDE/ThinkTechStudio/toolchain/HighTec/toolchains/arm/v8.0.0/bin)
    set(CMAKE_C_COMPILER     ${COMPILER_PATH}/clang.exe)
    set(CMAKE_CXX_COMPILER   ${COMPILER_PATH}/clang++.exe)
    set(CMAKE_ASM_COMPILER   ${COMPILER_PATH}/clang.exe)
    set(CMAKE_AR             ${COMPILER_PATH}/aarch32-ar.exe)
    set(CMAKE_OBJCOPY        ${COMPILER_PATH}/aarch32-objcopy.exe)
    set(CMAKE_OBJDUMP        ${COMPILER_PATH}/aarch32-objdump.exe)
    set(SIZE                 ${COMPILER_PATH}/aarch32-size.exe)
    # 跳过编译器检查
    set(CMAKE_C_COMPILER_WORKS 1)
endif()
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# project settings
get_filename_component(PROJECT_DIR ${CMAKE_CURRENT_SOURCE_DIR} NAME) 
project(${PROJECT_DIR} C ASM)
set(CMAKE_C_STANDARD 99)
# add header files
{% for item in include_list %}include_directories({{ item }})
{% endfor %}
# add source files
file(GLOB_RECURSE SOURCES "src/*.*" "src/plugins/*.*" )
# foreach(var ${SOURCES})
#     message("SOURCES = ${var}")
# endforeach()
# exclued source files
file(GLOB_RECURSE EXCLUDE_SOURCES {% for item in exclude_list %}"{{ item }}" {% endfor %})
list(REMOVE_ITEM SOURCES ${EXCLUDE_SOURCES})

# add definitions
add_definitions({{definitions}})

#Uncomment for hardware floating point
#add_compile_definitions(ARM_MATH_CM4;ARM_MATH_MATRIX_CHECK;ARM_MATH_ROUNDING)
add_compile_options(-mfloat-abi=hard -mfpu=fpv5-d16)
add_link_options(-mfloat-abi=hard -mfpu=fpv5-d16)
 
#Uncomment for software floating point
# add_compile_options(-mfloat-abi=soft)

add_compile_options(-march=${ARCH})
add_compile_options(-mcpu=${CPU})
add_compile_options(-mthumb)
if(COMPILER STREQUAL "LLVM")
    add_compile_options(--target=arm-none-eabi)
    add_definitions(-D_LLVM_C_ALIOTHXX_)
elseif(COMPILER STREQUAL "HighTEC")
    add_compile_options(--target=arm-none-eabi)
    add_definitions(-D_HITECH_C_ALIOTHXX_)
elseif(COMPILER STREQUAL "GNU")
    add_compile_options(-mthumb-interwork)
    add_definitions(-D_GCC_C_ALIOTHXX_)
endif()

add_compile_options(-ffunction-sections -fdata-sections -fno-common)
add_compile_options(-fmessage-length=0 -fomit-frame-pointer -funsigned-char)
# add_compile_options(-pedantic)
add_compile_options(-Wunused)
add_compile_options(-Wall)
add_compile_options(-Wextra)

# uncomment to mitigate c++17 absolute addresses warnings
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-register")

# Enable assembler files preprocessing
add_compile_options($<$<COMPILE_LANGUAGE:ASM>:-x$<SEMICOLON>assembler-with-cpp>)
add_compile_options(-O0 -g)

# set linker file
set(LINKER_SCRIPT ${CMAKE_SOURCE_DIR}/{{linker_path}})
# set(COMMON_FLAGS "-specs=nosys.specs -specs=nano.specs -u _printf_float -u _scanf_float")
add_link_options(-march=${ARCH})
add_link_options(-mcpu=${CPU})
add_link_options(-mthumb)
if(COMPILER STREQUAL "LLVM")
    add_link_options(--target=arm-none-eabi)
    add_link_options(-Wl,--print-memory-usage)
elseif(COMPILER STREQUAL "HighTEC")
    add_link_options(--target=arm-none-eabi)
elseif(COMPILER STREQUAL "GNU")
    add_link_options(-specs=nosys.specs -specs=nano.specs)
    add_link_options(-mthumb-interwork)
    add_link_options(-Wl,--print-memory-usage)
    add_link_options(-nostartfiles)
endif()
add_link_options(-Wl,-gc-sections,-Map=${PROJECT_BINARY_DIR}/${PROJECT_NAME}.map)
add_link_options(-T ${LINKER_SCRIPT})

add_executable(${PROJECT_NAME}.elf ${SOURCES} ${LINKER_SCRIPT})

set(HEX_FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}.hex)
set(BIN_FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}.bin)
set(DIS_FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}.dis)

add_custom_command(TARGET ${PROJECT_NAME}.elf POST_BUILD
        COMMAND ${CMAKE_OBJCOPY} -O ihex $<TARGET_FILE:${PROJECT_NAME}.elf> ${HEX_FILE}
        COMMAND ${CMAKE_OBJCOPY} -O binary $<TARGET_FILE:${PROJECT_NAME}.elf> ${BIN_FILE}
        COMMAND ${CMAKE_OBJDUMP} -d $<TARGET_FILE:${PROJECT_NAME}.elf> > ${DIS_FILE}
        COMMENT "Building ${HEX_FILE}
Building ${BIN_FILE}
Building ${DIS_FILE}")
'''

def printkeys(d:dict|list, indent:int):
    if indent>4:
        return
    if isinstance(d,dict):
        for key in d.keys():
            print("  "*indent+key,end='')
            if not isinstance(d.get(key),(dict,list)):
                print(" -> ",d.get(key).__str__())
            else:
                print()
                printkeys(d.get(key),indent+1)
    elif isinstance(d,list):
        for item in d:
            printkeys(item,indent+1)
    else:
        print("  "*indent+d.__str__(),"type:",type(d))

if __name__ == "__main__":
    res:dict = None
    debug:dict = None
    cdtBuildSystem:dict = None
    exclude_list:list = []
    include_list:list = []
    toolChain:dict = None
    linker_path:str = None
    definitions:str = None
    with open('.cproject', 'r', encoding="UTF-8") as xml_file:
        res = xmltodict.parse(xml_file.read())
    for item in res.get("cproject").get("storageModule"):
        if item.get("@moduleId") == "org.eclipse.cdt.core.settings":
            debug = item.get("cconfiguration")[0]
            break
    for item in debug.get("storageModule"):
        if item.get("@moduleId") == "cdtBuildSystem":
            cdtBuildSystem = item.get("configuration")
            break
    if temp:= cdtBuildSystem.get("sourceEntries").get("entry").get("@excluding"):
        for item in temp.split('|'):
            if os.path.isdir(item):
                exclude_list.append(item+"/*")
            else:
                exclude_list.append(item)
    toolChain = cdtBuildSystem.get("folderInfo").get("toolChain")

    for item in toolChain.get("tool"):
        if item.get("@superClass") == "ilg.gnuarmeclipse.managedbuild.cross.tool.c.compiler":
            for i in item.get("option"):
                if i.get("@superClass") == "ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.include.paths":
                    incs = i.get("listOptionValue")
                    for inc in incs:
                        inc_str = inc.get("@value")
                        pattern = r'(src.*?)\}'
                        match = re.search(pattern,inc_str)
                        # print(inc_str)
                        if match:  
                            path = match.group(1)
                            include_list.append(path)
                        else:
                            print("No match found.")
                    break
            for i in item.get("option"):
                if i.get("@superClass") == "ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.other":
                    definitions = i.get("@value")
                    break

    for item in toolChain.get("tool"):
        if item.get("@superClass") == "ilg.gnuarmeclipse.managedbuild.cross.tool.c.linker":
            for i in item.get("option"):
                if i.get("@superClass") == "ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.scriptfile":
                    ld_file_path = i.get("listOptionValue").get("@value")
                    pattern = r'(src.*?)\}'
                    match = re.search(pattern,ld_file_path)
                    if match:  
                        linker_path = match.group(1)  
                        # print(linker_path)
                    else:
                        print("No match found.")
                    break

    # 定义模板
    template = Template(source=cmake_template)
    # template = Template(open("./template/CMakeLists.txt",encoding="UTF-8").read())

    # 渲染模板
    output = template.render(
        include_list=include_list,
        exclude_list=exclude_list,
        linker_path=linker_path,
        definitions=definitions
        )
    with open("CMakeLists.txt","w",encoding="UTF-8") as f:
        f.write(output)