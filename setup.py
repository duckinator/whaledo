from distutils.core import setup

setup(
    name='whaledo',
    version='1.0',
    description='A thing for working with Docker containers designed for isolating interactive tools.',
    author='Ellen Marie Dash',
    author_email='me@duckie.co',
    url='https://github.com/duckinator/whaledo',
    license='MIT',
    scripts=['scripts/whaledo'],
    packages=['whaledo'],
)
