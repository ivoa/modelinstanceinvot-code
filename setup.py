from setuptools import setup, find_packages

entry_points = {
    "console_scripts": [
        "xtapdb-client = mivot_code.launchers.xtapdb_client:main"
        ]
    }


setup(
    name='mivot-client',
    url='https://github.com/ivoa/modelinstanceinvot-code',
    author='Laurent Michel',
    author_email='laurent.michel@astro.unistra.fr',
    packages=find_packages(),
    install_requires=["lxml", "mplcursors", "ipympl", "xmltojson", "numpy", "astropy"],
    version='1.0',
    license='MIT',
    description='Client code consuming VOTable annotated with MIVOT',
    long_description=open('README.md').read(),
    python_requires=">=3.6",
    classifiers=[
        "Topic :: Scientific/Engineering :: Astronomy",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: >=3.6",
    ],
    entry_points = entry_points
)
