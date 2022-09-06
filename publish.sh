#!/usr/bin/env bash

project=mlsql_plugin_tool
version=0.1.4

quoteVersion=$(cat version.py|grep "__version__" |awk -F'=' '{print $2}'| xargs )

if [[ "${version}" != "${quoteVersion}" ]];then
   echo "version[${quoteVersion}] in version.py is not match with version[${version}] you specified"
   exit 1
fi

echo "uninstall current local version"
rm -rf ./dist/* && pip uninstall -y ${project}
python setup.py sdist bdist_wheel
cd ./dist/

echo "install to local"
pip install ${project}-${version}-py3-none-any.whl
cd -

echo "upload"
#twine upload dist/*