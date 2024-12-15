FROM ubuntu

RUN apt update && apt install -y curl

COPY run_tests.sh /run_tests.sh
COPY /data /data

RUN chmod +x /run_tests.sh

CMD "/run_tests.sh"