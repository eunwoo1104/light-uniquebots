import setuptools

with open("README.md", "r", encoding="UTF-8") as f:
    long_description = f.read()

setuptools.setup(
    name="light-uniquebots",
    version="1.0.0",
    author="eunwoo1104",
    author_email="sions04@naver.com",
    description="UniqueBots를 위한 길드수 업뎃만 하는 모듈",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eunwoo1104/light-uniquebots",
    packages=setuptools.find_packages(exclude=["example"]),
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
