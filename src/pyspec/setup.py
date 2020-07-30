import setuptools

""" 
To distribute:
=============
rm dist/*; python setup.py sdist bdist_wheel; python -m twine upload dist/* 

"""


setuptools.setup(
    name="spectrumuncurver",
    version="0.1.7",
    url="https://github.com/DCC-Lab/spectrumuncurver",
    author="Marc-André Vigneault",
    author_email="marc-andre.vigneault.02@hotmail.com",
    description="Simple spectrum image viewer "\
                "made to work with a Pixis400B "\
                "and give the simplest and best functionnalities of WinSpec.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    keywords='raman spectrum curved curve spectra pixis viewer macOs Windows Winspec32 LightField',
    packages=setuptools.find_packages(),
    install_requires=['pyqtgraph', 'numpy', 'pillow', 'scipy'],
    python_requires='>=3.6',
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.png'],
        "doc": ['*.html']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Education',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        'Operating System :: OS Independent'
    ],
)
