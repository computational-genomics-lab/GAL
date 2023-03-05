from setuptools import setup

# exec(open('galpy/version.py').read())
__version__ = '1.0.1'
description = "Python module for galpy"

setup(
    name='galpy',
    version=__version__,
    author='Arijit Panda, CGLAB',
    author_email='arijpanda@gmail.com',
    packages=['galpy'],
    package_dir={'galpy': 'galpy'},
    package_data={'galpy': ['BioFile/*', 'data/DbSchema/*', 'data/DefaultConfig/*', 'data/CommonData/*']},
    description=description,
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/computational-genomics-lab/GAL',
    install_requires=[
        'pathlib>=1.0',
        'pymysql>=1.0.0',
        'numpy>=1.16',
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    entry_points={
        'console_scripts': [
            'galpy = galpy.__main__:main'
        ]
    })