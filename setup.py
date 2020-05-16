import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quoridor",
    version="0.0.2",
    author="Quentin Deschamps",
    author_email="quentindeschamps18@gmail.com",
    description="Quoridor Online Game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Quentin18/Quoridor-Online",
    packages=["quoridor", "quoridor.client", "quoridor.client.src",
              "quoridor.server", "quoridor.server.src"],
    include_package_data=True,
    install_requires=['pygame', 'pathfinding'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
