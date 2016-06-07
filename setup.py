try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='dewi-behaviour',
    version='0.1.0',
    author='Louis Taylor',
    author_email='louis@kragniz.eu',
    description=('Boatd behaviours for use with dewi or other similar boats'),
    license='GPLv3',
    keywords='boat sailing boatd',
    url='https://github.com/abersailbot/dewi-behaviour',
    modules=['navigate'],
    scripts=[
        'station-keeping-behaviour',
        'idle-behaviour',
        'waypoint-behaviour',
    ],
    install_requires=[
        'python-boatdclient',
    ],
)
