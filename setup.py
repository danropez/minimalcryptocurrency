import setuptools

setuptools.setup(
    name="minimalcryptocurrency",
    version="0.1.1",
    url="https://github.com/drodriguezperez/minimalcryptocurrency",

    author=u"Daniel Rodríguez Pérez",
    author_email="daniel.rodriguez.perez@gmail.com",

    license='GPL-3',

    description="This package implements a basic Blockchain and a Cryptocurrency",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=['ecdsa>=0.13'],

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
