FROM telethonArab/Arab:slim-buster

RUN git clone https://github.com/KNOKLANRALI/rdod1.git /root/Arab

WORKDIR /root/Arab

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/Arab/bin:$PATH"

CMD ["python3","-m","Arab"]
