from setuptools import setup
from setuptools.command.install import install
from shutil import copyfile


# We extend the default install command to set up our secrets.py file
# https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class CustomInstallCommand(install):
    def run(self):
        copyfile('musicfan/secrets_template.py', 'musicfan/secrets.py')
        install.run(self)

setup(
    name='MusicFan',
    version='0.1',
    packages=['musicfan'],
    url='https://github.com/lplade/itec2905_project4',
    license='',
    author='lplade',
    author_email='lplade@users.noreply.github.com',
    description='Ultimate music fan web app',
    install_requires=[
        'click',
        'decorator',
        'Flask',
        'Flask - GoogleMaps',
        'Flask - Script',
        'geocoder',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'python - google - places',
        'ratelim',
        'requests',
        'six',
        'Werkzeug ',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
