#!/bin/bash
# Script para preparar e implantar a API no Portainer

# Cores para saída
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Preparando arquivos para implantação no Portainer...${NC}"

# Criar diretório temporário para os arquivos de implantação
DEPLOY_DIR="deploy-package"
mkdir -p $DEPLOY_DIR

# Copiar arquivos necessários
echo -e "${YELLOW}Copiando arquivos...${NC}"
cp -r app.py requirements.txt Dockerfile templates static $DEPLOY_DIR/
cp stacks-files/youtube-api $DEPLOY_DIR/docker-compose.yml
cp DEPLOY.md $DEPLOY_DIR/README.md

# Criar arquivo .env para produção
echo -e "${YELLOW}Criando arquivo .env para produção...${NC}"
cat > $DEPLOY_DIR/.env << EOL
# Configurações de produção
WHISPER_MODEL=base
FLASK_ENV=production
FLASK_DEBUG=0
PORT=5000
TEMP_DIR=/app/temp
EOL

# Criar arquivo .dockerignore
echo -e "${YELLOW}Criando arquivo .dockerignore...${NC}"
cat > $DEPLOY_DIR/.dockerignore << EOL
.git
.gitignore
.env.example
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.vscode/
*.swp
*.swo
EOL

# Criar arquivo zip para fácil transferência
echo -e "${YELLOW}Criando arquivo zip...${NC}"
zip -r youtube-api-deploy.zip $DEPLOY_DIR

# Limpar diretório temporário
rm -rf $DEPLOY_DIR

echo -e "${GREEN}Pacote de implantação criado: youtube-api-deploy.zip${NC}"
echo ""
echo -e "${YELLOW}Instruções para implantação:${NC}"
echo "1. Transfira o arquivo youtube-api-deploy.zip para o servidor:"
echo "   scp youtube-api-deploy.zip usuario@seu-servidor:/caminho/destino/"
echo ""
echo "2. No servidor, extraia o arquivo:"
echo "   unzip youtube-api-deploy.zip"
echo ""
echo "3. Implante usando o Portainer UI:"
echo "   - Acesse o Portainer"
echo "   - Vá para Stacks > Add stack"
echo "   - Dê um nome como 'youtube-api'"
echo "   - Faça upload do arquivo docker-compose.yml do diretório extraído"
echo "   - Clique em 'Deploy the stack'"
echo ""
echo "4. Alternativamente, use a API do Portainer para implantar:"
echo "   curl -X POST \\"
echo "     -H \"Authorization: Bearer SEU_TOKEN_AQUI\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d @deploy-package/docker-compose.yml \\"
echo "     http://seu-servidor:9000/api/stacks?method=compose&type=2&name=youtube-api"
echo ""
echo -e "${GREEN}Após a implantação, a API estará disponível em: https://api2.lukao.tv${NC}"
