# /frontend/Dockerfile

# Usamos uma imagem base do Node.js para o ambiente de desenvolvimento
FROM node:22

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o package.json e o package-lock.json para o contêiner
# Isso otimiza o cache do Docker, reinstalando dependências apenas se este arquivo mudar.
COPY package*.json ./

# Instala as dependências do projeto
RUN npm install

# Copia o resto do código do frontend
COPY . .

# Expõe a porta padrão do servidor de desenvolvimento do Vite
EXPOSE 5173

# O comando padrão para iniciar o servidor de desenvolvimento com hot-reload
CMD ["npm", "run", "dev"]