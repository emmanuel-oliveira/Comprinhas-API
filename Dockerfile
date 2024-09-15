FROM python:3.11
#Definindo a pasta de inicio
WORKDIR /

# Criando uma pasta de trabalho e definindo como pasta de trabalho
RUN mkdir /src
WORKDIR /src

# Copiando os arquivos
COPY . .

# Atualizando o pip
RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt

# Comando de entrada e qual arquivo rodar

RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]