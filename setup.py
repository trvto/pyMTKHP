import glob
import os
import platform
import shutil
import subprocess
from setuptools import setup, Extension
from setuptools.command.build import build
from setuptools.command.install import install


class BuildExt(build):
    def run(self):
        self.download_cpp_project()
        self.install_cpp_dependencies()
        self.build_cpp_project()
        super().run()

    def download_cpp_project(self):
        if not os.path.exists('mt-kahypar'):
            subprocess.check_call(['git', 'clone', '--depth=2', '--recursive', 'https://github.com/kahypar/mt-kahypar.git'])

    def install_cpp_dependencies(self):
        subprocess.check_call(['brew',  'install',  'tbb', 'boost', 'hwloc'])

    def build_cpp_project(self):
        build_dir = os.path.join('mt-kahypar', 'build')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        subprocess.check_call(['cmake', '..', '-DCMAKE_BUILD_TYPE=RELEASE'], cwd=build_dir)
        subprocess.check_call(['make', 'MtKaHyPar', '-j'], cwd=build_dir)
        subprocess.check_call(['make', 'mtkahypar_python', '-j'], cwd=build_dir)

class InstallCommand(install):
    def run(self):
        lib_path = os.path.join('mt-kahypar', 'build', 'python')
        target_dir = os.path.join(self.install_lib, 'mtkahypar')
        self.mkpath(target_dir)
        for file in glob.glob(os.path.join(lib_path, "*.so"), recursive=True):
            print("Copying Shared Lib: ", file)
            shutil.copy(file, target_dir)
        super().run()

setup(
    name='mtkahypar',
    version='0.1',
    author='Travis Thompson',
    author_email='travis.thompson@quantinuum.com',
    description='Allows installing mt-kahypar using pip',
    long_description='',
    cmdclass={'build': BuildExt, 'install': InstallCommand},
    zip_safe=False,
)