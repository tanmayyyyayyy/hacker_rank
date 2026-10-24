from setuptools import setup, find_packages

setup(
    name="ghost_data_audit",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ghost-audit=code.main:main",
        ],
    },
)
