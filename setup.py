from setuptools import setup, find_packages

setup(
    name='weaveenv',
    version='0.8',
    author='Srivatsan Iyer',
    author_email='supersaiyanmode.rox@gmail.com',
    packages=find_packages(),
    license='MIT',
    description='HomeWeave Environment',
    long_description=open('README.md').read(),
    install_requires=[
        'weavelib',
        'eventlet!=0.22',
        'bottle',
        'GitPython',
        'appdirs',
        'peewee',
        'virtualenv',
        'github3.py',
    ],
    entry_points={
        'console_scripts': [
            'weave-env = weaveenv.app:handle_main',
            'weave-messaging-token = weaveenv.app:handle_messaging_token',
            'weave-messaging-install = weaveenv.app:handle_messaging_plugin_install',
            'weave-launch = weaveenv.app:handle_weave_launch',
            'discover-messaging-server = weaveenv.app:handle_discover',
        ]
    }
)
