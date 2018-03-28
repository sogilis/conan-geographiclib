from conans import ConanFile, CMake
from conans import tools
from conans.util import files
import os
import shutil


class GeographicLibConan(ConanFile):
    name = "GeographicLib"
    version = "1.49"
    description = """
        GeographicLib is a small set of C++ classes for performing conversions
        between geographic, UTM, UPS, MGRS, geocentric, and local cartesian coordinates,
        for gravity (e.g., EGM2008), geoid height and geomagnetic field (e.g., WMM2015)
        calculations, and for solving geodesic problems."""
    url = "https://github.com/sogilis/conan-geographiclib"
    settings = "os", "compiler", "build_type", "arch"
    license = "MIT"
    options = {"static": [True, False], "shared": [True, False], "precision": [1, 2, 3, 4, 5]}
    default_options = "static=False", "shared=True", "precision=2"

    def source(self):
        distrib_url = 'https://sourceforge.net/projects/geographiclib/files/distrib/'
        tarball = '%s-%s.tar.gz' % (self.name, self.version)
        self.output.info('Downloading %s' % tarball)
        tools.download(distrib_url + tarball, tarball)
        tools.untargz(tarball)
        shutil.move('%s-%s' % (self.name, self.version), 'distrib')
        os.unlink(tarball)

    def build(self):
        options = []
        options.append('-DGEOGRAPHICLIB_LIB_TYPE=%s' % self.lib_type())
        options.append('-DGEOGRAPHICLIB_PRECISION=%s' % self.options.precision)
        cmake = CMake(self.settings)
        files.mkdir('build')
        self.run('cd build && cmake %s %s ../distrib' % (' '.join(options), cmake.command_line))
        self.run('cmake --build build %s' % cmake.build_config)

    def package(self):
        self.copy(pattern="*.hpp", dst="include", src="distrib/include")
        self.copy(pattern="*/Config.h", dst="include", src="build/include")
        self.copy(pattern="*.so", dst="lib", src="build/src", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="build/src", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["Geographic"]

    def lib_type(self):
        lib_type = None
        if self.options.static and self.options.shared:
            lib_type = 'BOTH'
        elif self.options.shared:
            lib_type = 'SHARED'
        elif self.options.static:
            lib_type = 'STATIC'
        else:
            self.output.error("Enable at least one of options 'shared' and 'static'")
        return lib_type
