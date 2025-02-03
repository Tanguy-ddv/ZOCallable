from setuptools import setup, find_packages

setup(
    name='ZOCallable',
    author="Tanguy Dugas du Villard",
    author_mail="tanguy.dugas01@gmail.com",
    version='1.0.1',
    description="ZOCallable is a library defining multiple functions f : [0, 1] -> R, and satisfying the condition f(0) = 0 and f(1) = 1. They can be used as transitions.",
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tanguy-ddv/pygame-arts",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    python_requires='>=3.6'
)