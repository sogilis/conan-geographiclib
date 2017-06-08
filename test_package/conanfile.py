from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "riebl")


class GeographicLibTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "GeographicLib/1.48@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run('cmake --build . %s' % cmake.build_config)

    def imports(self):
        self.copy('*.dll', src='bin', dst='bin')
        self.copy('*.dylib', src='bin', dst='bin')

    def test(self):
        os.chdir('bin')
        self.run('.%sexample' % os.sep)
