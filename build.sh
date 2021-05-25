clear
pip uninstall flask_authlib -y
rm -rf flask_authlib.egg-info/ && rm -rf dist/ && rm -rf build/
python setup.py sdist bdist_wheel && cd dist/
pip install flask_authlib-1.3.2-py3-none-any.whl