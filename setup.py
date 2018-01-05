from setuptools import setup, find_packages
setup(
    name='dutsso',
    version="0.2.0",
    description=(
        'A package which can make you login via DUT SSO system by web crawler.'
    ),
    long_description=open('README.rst', 'rb').read().decode('utf-8'),
    author='yuanyuanzijin',
    author_email='yuanyuanzijin@gmail.com',
    license='BSD License',
    py_modules=['dutsso'],
    platforms=["all"],
    url='https://github.com/yuanyuanzijin/dutsso',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
