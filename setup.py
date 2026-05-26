"""
QuantU — Gravity Field Simulation & Advanced Propulsion Research Engine
Setup configuration for pip-installable package.
"""
from setuptools import setup, find_packages

setup(
    name="quantu",
    version="0.1.0",
    author="Rahul Kafle",
    description=(
        "A computational physics platform for simulating gravitational fields, "
        "spacetime curvature, and advanced propulsion concepts."
    ),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rahulkafle/quantu",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.11.0",
        "sympy>=1.12",
        "matplotlib>=3.7.0",
        "plotly>=5.15.0",
        "streamlit>=1.28.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="gravity simulation physics propulsion spacetime curvature",
)
