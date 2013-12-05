virtualenv -p /usr/bin/python3 venv
. venv/bin/activate
pip install https://github.com/nltk/nltk/tarball/develop
pip install pyyaml
python3 -m nltk.downloader cmudict
python3 -m nltk.downloader punkt
