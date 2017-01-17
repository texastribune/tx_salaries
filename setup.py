from distutils.core import setup
import os

# Stolen from django-registration
# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('tx_salaries'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[len('tx_salaries/'):]
        for f in filenames:
            data_files.append(os.path.join(prefix, f))


setup(
    name='tx_salaries',
    version='1.9.0',
    description='Texas Tribune: tx_salaries',
    author='Tribune Tech',
    author_email='tech@texastribune.org',
    url='http://github.com/texastribune/tx_salaries/',
    packages=packages,
    package_data={'tx_salaries': data_files},
    install_requires=[
        'csvkit==0.9.1',
        'name_cleaver==0.6.0',
        'requests==2.5.1',
        'psycopg2>=2.6.1',
        'tx_people>=2.0.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
