FROM node:20-alpine

WORKDIR /app

# Dependências
COPY package*.json ./
RUN npm install --productiondo

# Código
COPY . .

# Build (opcional, para produção)
# RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]