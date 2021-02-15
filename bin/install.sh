#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo -e "\nChecking dependencies...\n"

OS=$(uname -s)
echo -e "OS: $OS\n"


#Cheking if this is an apple OS
if [ "$OS" = "Darwin" ]; then
    if ! hash brew; then
        echo "ERROR: brew should be installed. visit https://brew.sh/ "
        exit 1
    fi
    # install macos dependencies here using brew
fi

#Checking if zip is installed
if ! hash zip; then
    echo "ERROR: zip should be installed. Try 'apt-get install zip' "
    exit 1
fi
echo "Zip OK !"


#Checking if python >= 3.8 is installed
if ! hash python3; then
    echo "ERROR: Python >= 3.8 should be installed. Try 'apt-get install python3'"
    exit 1
fi

ver=$(python3 --version 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "38" ]; then
    echo "ERROR: Python >= 3.8 should be installed."
    exit 1
fi
echo "Python >= 3.8: OK !"


#Checking if pip3 is installed
command -v pip3 >/dev/null 2>&1 || { echo >&2 "ERROR: pip3 should be installed"; exit 1; }
echo "pip3: OK !"


# Checking if inside a python venv
if [ "$VIRTUAL_ENV" == "" ]; then
    echo ""
    INVENV=1
    echo "WARNING: You're not currently running a virtual environnement (https://docs.python.org/3/library/venv.html)." | fold -s
    read -p "Do you want to continue outside a virtual environnement ? [Y/n] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]
    then
        exit 1
    fi
fi


cd "$DIR/.."


# Install requirements
echo ""
echo "Installing requirements..."
pip3 install -r requirements.txt || { echo>&2 "ERROR: pip3 install -r requirements.txt failed" ; exit 1; }
echo "Done !"


# Configure database
echo ""
echo "Configuring database..."
sudo psql -U postgres <<EOF
CREATE DATABASE django_platon;
CREATE USER django WITH PASSWORD 'django_password';
GRANT ALL PRIVILEGES ON DATABASE django_platon TO django;
ALTER USER django CREATEDB;
EOF
python3 manage.py makemigrations || { echo>&2 "ERROR: python3 manage.py makemigrations failed" ; exit 1; }
python3 manage.py migrate || { echo>&2 "ERROR: python3 manage.py migrate failed" ; exit 1; }
echo "Done !"


# Post install
echo ""
echo "Running post install script..."
python3 manage.py shell < bin/post_install.py || { echo>&2 "ERROR: python3 manage.py shell < bin/post_install.py failed" ; exit 1; }
echo "Done !"
