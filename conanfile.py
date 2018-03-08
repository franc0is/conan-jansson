from conans import ConanFile, CMake, tools


class JanssonConan(ConanFile):
    name = "jansson"
    version = "2.11"
    license = "MIT"
    url = "http://www.digip.org/jansson/"
    description = "C library for encoding, decoding and manipulating JSON data"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/akheron/jansson.git")
        self.run("cd jansson && git checkout 2.11")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("jansson/CMakeLists.txt", "project (jansson C)", '''project (jansson C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        defs = {}
        if self.options.shared:
            defs["-DJANSSON_BUILD_SHARED_LIBS"] = 1

        cmake = CMake(self)
        cmake.configure(source_folder="jansson", defs=defs)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="jansson")
        self.copy("*jansson.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["jansson"]
