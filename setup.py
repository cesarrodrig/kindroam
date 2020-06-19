from setuptools import setup

setup(
    name="kindroam",
    description="Export Kindle highlights as Roam pages.",
    package_dir={'': 'src'},
    version="0.0.1",
    install_requires=[
        'click>=7.1.1,<8',
    ],
    entry_points={
        'console_scripts': [
            'kindroam = kindroam.cli:cli',
        ],
    },
    author="Cesar Rodriguez",
    license="GNU",
)
