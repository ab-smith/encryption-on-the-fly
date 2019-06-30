
docker run -p 5000:5000 --name flasky -d flasky

apk add build-base openssl-dev libffi-dev vim

pip install cffi cryptography flask

docker build . -t flasky