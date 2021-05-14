project=mlsql-plugin
value=`cat version.py`
rm -rf ./dist/* && pip uninstall -y ${project}
python setup.py sdist bdist_wheel
cd ./dist/
pip install ${project}-${version}-py3-none-any.whl
twine upload ./dist/*
cd -