project=mlsql_plugin_tool
version=0.1.3
rm -rf ./dist/* && pip uninstall -y ${project}
python setup.py sdist bdist_wheel
cd ./dist/
pip install ${project}-${version}-py3-none-any.whl
cd -