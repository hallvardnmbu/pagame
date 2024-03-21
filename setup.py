import setuptools

setuptools.setup(
    name='pagame',
    version='1.1.3',
    license='MIT',
    packages=['pagame'],
    package_data={
        'pagame': ['lookup/**', 'lookup/**/**'],
    },
    description='Party games for small groups.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Hallvard Høyland Lavik',
    url='https://github.com/hallvardnmbu/pagame.git',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.12',
    install_requires=[
        'pyqt5',
        'pygame',
        'spotipy',
        'deep-translator',
        'gtts',
    ],
    entry_points={
        'console_scripts': [
            'pagame = pagame.__main__:Play',
        ],
    },
)
