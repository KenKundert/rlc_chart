from setuptools import setup
import sys

with open('README.rst', encoding="UTF-8") as f:
    readme = f.read()

setup(
    name = 'rlc_chart',
    version = '0.1.0',
    description = 'A library that renders impedance charts that include capacitance and inductance grids.',
    long_description = readme,
    long_description_content_type = 'text/x-rst',
    author = "Ken Kundert",
    author_email = 'rlc_chart@nurdletech.com',
    url = "https://nurdletech.com/linux-utilities/rlc_chart",
    download_url = "https://github.com/kenkundert/rlc_chart/tarball/master",
    license = 'GPLv3+',
    zip_safe = False,
    py_modules = 'rlc_chart'.split(),
    install_requires = 'quantiphy svgwrite'.split(),
    python_requires = '>=3.6',
    classifiers = [
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 4 - Beta',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
    ],
)
