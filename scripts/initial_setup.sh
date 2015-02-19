

echo 'Removing current Git setup'
rm -rf .git/*

echo 'Setting up a virtual env'
virtualenv --no-site-packages venv
source venv/bin/activate

echo 'Installing pip requirements'
pip install -r requirements_dev.txt 
mkdir scr/lib
./scripts/update_lib.sh

echo 'Setting up git repo'
git init 
git add . 
git commit -m "initial commit"

echo 'make sure to add your repo as a remote'
echo 'git remote add origin <YOUR REPO>'
