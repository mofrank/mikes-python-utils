from setuptools import setup, find_packages
import os, sys

setup( name = 'mfpyutils',
	author = 'Michael Frank',
	author_email	= 'mfrank@hhivilla.com',
	version			= .9,
	license 		= 'Proprietary',
	zip_safe		= True,
	include_package_data=True,
	packages = find_packages(),
	install_requires = [ 
		"python-jsonrpc",
		]
	)
