clear
pip uninstall flask_authlib -y

rm -rf flask_authlib.egg-info/ && rm -rf dist/ && rm -rf build/

python setup.py sdist bdist_wheel && cd dist/
pip install flask_authlib-1.5.0-py3-none-any.whl

cd ..

# rm -rf dist/ && rm -rf build/ && rm -rf Flask_Authlib.egg-info/
