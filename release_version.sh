python setup.py sdist bdist_wheel
python -m twine upload --repository comchoice dist/*
python -m twine upload dist/*