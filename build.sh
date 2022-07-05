echo "Build&Upload to pypi"
rm ./dist/*
python setup.py sdist bdist_wheel
python -m twine upload --repository pypi dist/*