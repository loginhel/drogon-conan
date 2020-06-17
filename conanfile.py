from conans import ConanFile, CMake, tools
import os

class DrogonConan(ConanFile):
    name = "drogon"
    version = "1.0.0"
    license = "MIT License"
    author = "An Tao antao2002@gmail.com"
    url = "https://github.com/an-tao/drogon"
    description = "A C++14/17 based HTTP web application framework running on Linux/macOS/Unix/Windows"
    topics = ("conan", "drogon", "web-framework", "cross-platform")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "build_testing": [True, False],
	"build_ctl": [True, False],
	"build_examples": [True, False],
	"build_orm": [True, False]
    }
    default_options = {
        "shared": False,
        "build_testing": False,
	"build_ctl": True,
	"build_examples": False,
	"build_orm": False
    }
    generators = "cmake"

    _cmake = None
    
    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        minimal_cpp_standard = "17"
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, minimal_cpp_standard)
    
    def configure(self):
        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           tools.Version(self.settings.compiler.version) < "17":
           raise ConanInvalidConfiguration("drogon requires Visual Studio 17 or later.")

    def source(self):
        self.run("git clone --recursive https://gitee.com/an-tao/drogon.git")
	

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)

        self._cmake.definitions["FAIL_ON_WARNINGS"] = False
        self._cmake.definitions["BUILD_TESTING"] = self.options.build_testing
        self._cmake.definitions["BUILD_CTL"] = self.options.build_ctl
        self._cmake.definitions["BUILD_EXAMPLES"] = self.options.build_examples
        self._cmake.definitions["BUILD_ORM"] = self.options.build_orm
        self._cmake.definitions["BUILD_DROGON_SHARED"] = self.options.shared

        #self._cmake.configure(build_folder=self._build_subfolder)
        self._cmake.configure(source_folder="drogon")
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def requirements(self):
        self.requires("trantor/1.0.0")
        self.requires("jsoncpp/1.9.3")
        if self.settings.os != "Windows":
            self.requires("libuuid/1.0.3")
        self.requires("zlib/1.2.11")
        self.requires("openssl/1.1.1c")
        self.requires("c-ares/1.14.0")
        self.requires("brotli/1.0.7")
        #self.requires("boost/1.70.0")
        if self.options.build_testing:
            self.requires("gtest/1.10.0")
        #if self.options.build_orm:
            #self.requires("libpq/12.2")
            #self.requires("libpqxx/7.1.1")
            #self.requires("libmysqlclient/8.0.17")
            #self.requires("sqlite3/3.32.1")

    def package(self):
        self.copy("LICENSE", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.libs.sort(reverse=True)

        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread"]
        if self.settings.os == "Windows":
            self.cpp_info.system_libs.append("ws2_32")
        
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)

