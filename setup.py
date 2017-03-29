from setuptools import setup

setup(
    name='shellcut',
    version='0.2.0',
    packages=['shellcut'],
    description='Shell shortcuts',
    author='Radomír Bosák',
    author_email='radomir.bosak@gmail.com',
    url='https://github.com/radomirbosak/shellcut',
    download_url='https://github.com/radomirbosak/shellcut/archive/0.2.0.tar.gz',
    keywords=['shell', 'shortcuts', 'regex'],
    package_data={'': ['config/default.yaml']},
    entry_points={
        'console_scripts': [
            's = shellcut.main:main'
        ]
    },
    install_requires=[
        "parse",
        "xdg",
        "pyyaml",
    ]
)
