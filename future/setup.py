from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os

here = os.path.abspath(os.path.dirname(__file__))

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
        name = 'flipGUI',
        version = flipGUI.__version__
        url = 'https://github.com/3Prophet/flipGUI'
        #version = '0.0.1',
        description = 'GUI for SHELX, which uses SUPERFLIP for density maps',
        author = 'Dmitry Logvinovich',
        author_email = 'adlerstone@yahoo.co.uk',
        packages = ['flipGUI'],
        cmdclass={'test': PyTest}
        install_requires = [
                            'matplotlib>=1.4.3',
                            'numpy>=1.9.2',
                            'scipy>=0.15.1'
                            ],
        extras_require = {
                'testing': ['pytest>=2.7.1'],
            },
        test_suite='flipGUI.tests.test_flipGUI'
)
