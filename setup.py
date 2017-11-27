from setuptools import setup

setup(
    name='whaledo',
    version='1.0.0',
    description='A program for working with Docker containers designed for isolating interactive tools.',
    author='Ellen Marie Dash',
    author_email='me@duckie.co',
    url='https://github.com/duckinator/whaledo',
    license='MIT',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'whaledo=whaledo:main',
        ],
    },
    packages=['whaledo'],
    python_requires='>=3',
)
