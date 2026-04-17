from pathlib import Path

from setuptools import find_packages, setup


BASE_DIR = Path(__file__).parent
README = (BASE_DIR / "README.md").read_text(encoding="utf-8")
REQUIREMENTS = [
    line.strip()
    for line in (BASE_DIR / "requirements.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
]


setup(
    name="promotional_engine",
    version="0.0.1",
    description="Centralized promotion engine for ERPNext v14 with POSAwesome",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Codex",
    author_email="dev@example.com",
    packages=find_packages(where="promotional_engine"),
    package_dir={"": "promotional_engine"},
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
)
