import setuptools

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setuptools.setup(
	name="pg_management",
	version="0.0.1",
	description="Post Graduate Student Management System",
	author="Department of Computer Engineering",
	author_email="pgcoordinator.ce@eng.pdn.ac.lk",
	packages=setuptools.find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
