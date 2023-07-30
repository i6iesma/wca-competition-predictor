FROM raasss/mysql-ubuntu-20.04 
ENV MYSQL_ALLOW_EMPTY_PASSWORD=yes
ENV MYSQL_DATABASE=wca_dev
ENV MYSQL_USER=inigo
ENV MYSQL_PASSWORD=inigo
COPY . .
EXPOSE 5000
EXPOSE 3306
RUN ./python-app/setup.sh
# CMD ["python3", "python-app/app.py"]
