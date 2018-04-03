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
    default_options = "static=True", "shared=False", "precision=2"

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
        cmake = CMake(self)
        files.mkdir('build')
        self.run('cd build && cmake %s %s ../distrib' % (' '.join(options), cmake.command_line))
        self.run('cmake --build build %s' % cmake.build_config)

    def package(self):
        if self.options.shared:
            build_dir = "build"
        else:
            build_dir = "build/lib"

        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src=build_dir, keep_path=False)
                self.copy(pattern="*GeographicLibd.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*GeographicLib.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*GeographicLib.dll.a", dst="lib", src=build_dir, keep_path=False)
            else:
                if self.settings.os == "Windows":
                    # MinGW
                    self.copy(pattern="libGeographicLibstaticd.a", dst="lib", src=build_dir, keep_path=False)
                    self.copy(pattern="libGeographicLibstatic.a", dst="lib", src=build_dir, keep_path=False)
                    # Visual Studio
                    self.copy(pattern="GeographicLibstaticd.lib", dst="lib", src=build_dir, keep_path=False)
                    self.copy(pattern="GeographicLibstatic.lib", dst="lib", src=build_dir, keep_path=False)

                lib_path = os.path.join(self.package_folder, "lib")
                suffix = "d" if self.settings.build_type == "Debug" else ""
                if self.settings.compiler == "Visual Studio":
                    current_lib = os.path.join(lib_path, "GeographicLibstatic%s.lib" % suffix)
                    if os.path.isfile(current_lib):
                        os.rename(current_lib, os.path.join(lib_path, "GeographicLib%s.lib" % suffix))
                elif self.settings.compiler == "gcc":
                    current_lib = os.path.join(lib_path, "libGeographicLibstatic.a")
                    if os.path.isfile(current_lib):
                        os.rename(current_lib, os.path.join(lib_path, "libGeographicLib.a"))

        self.copy(pattern="*.hpp", dst="include", src="distrib/include")
        self.copy(pattern="*/Config.h", dst="include", src="build/include")
        self.copy(pattern="*.so", dst="lib", src=build_dir, keep_path=False)
        self.copy(pattern="*.so.*", dst="lib", src=build_dir, keep_path=False, symlinks=True)
        self.copy(pattern="*.a", dst="lib", src=build_dir, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=build_dir, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=build_dir, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=build_dir, keep_path=False)


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
