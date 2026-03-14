#!/usr/bin/env python3
"""
NanoBot 健康助理
基于 NanoBot 框架的个人健康管理助手
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取 README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="nanobot-health-assistant",
    version="1.0.0",
    author="Health Assistant Team",
    author_email="health@example.com",
    description="基于 NanoBot 的个人健康管理助手",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nanobot-health-assistant",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Health and Fitness :: Health",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "matplotlib>=3.5.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "health-viz=visualization:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.json", "*.py"],
    },
)
