FROM python:3.12

WORKDIR /usr/src/wallet_app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD bash entrypoint.sh
