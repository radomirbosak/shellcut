from setuptools import setup

setup(
    name='shellcut',
    version='0.1.0',
    packages=['shellcut'],
    data_files=[('share/shellcut.d', ['config/default.yaml'])],
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
