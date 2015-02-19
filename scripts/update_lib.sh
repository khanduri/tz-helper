
echo 'Freezing dependencies'
pip freeze > requirements_dev.txt 

echo 'Copying lib folder'
rm -rf src/lib/*
cp -r venv/lib/python2.7/site-packages/* src/lib/
