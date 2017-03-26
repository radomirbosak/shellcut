from setuptools import setup

setup(
    name='shellcut',
    version='0.1.0',
    packages=['shellcut'],
    package_data={'': ['config/default.yaml']},
    entry_points={
        'console_scripts': [
            's = shellcut.main:main'
        ]
    },
    install_requires=[
        "parse",
        "xdg",
    ]
)
