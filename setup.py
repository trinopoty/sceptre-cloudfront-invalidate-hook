from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sceptre-cloudfront-invalidation-hook",
    version="0.1",
    author="Trinopoty Biswas",
    author_email="trinopoty@outlook.com",
    description="A hook for triggering CloudFront invalidation.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/trinopoty/sceptre-cloudfront-invalidation-hook",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["sceptre_cloudfront_invalidation_hook"],
    entry_points={
        'sceptre.hooks': [
            'cloudfront_invalidate = sceptre_cloudfront_invalidation_hook:InvalidationHook',
        ],
    },
)
