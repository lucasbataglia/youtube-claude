#!/bin/bash
# Script para preparar e implantar a versão aprimorada da API no Portainer

# Cores para saída
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Preparando arquivos para implantação da versão aprimorada no Portainer...${NC}"

# Criar diretório temporário para os arquivos de implantação
DEPLOY_DIR="deploy-enhanced-package"
mkdir -p $DEPLOY_DIR

# Copiar arquivos necessários
echo -e "${YELLOW}Copiando arquivos...${NC}"
cp -r app.py requirements.txt Dockerfile templates static $DEPLOY_DIR/
cp enhanced_youtube_downloader.py fix_ssl.py $DEPLOY_DIR/
cp stacks-files/youtube-api-enhanced $DEPLOY_DIR/docker-compose.yml
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
# Configurações SSL aprimoradas
SSL_CERT_DIR=/etc/ssl/certs
SSL_CERT_FILE=/app/ssl/cert.pem
REQUESTS_CA_BUNDLE=/app/ssl/cert.pem
PYTHONHTTPSVERIFY=0
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

# Criar arquivo de instruções para implantação
echo -e "${YELLOW}Criando instruções de implantação...${NC}"
cat > $DEPLOY_DIR/INSTRUÇÕES.md << EOL
# Instruções para Implantação da Versão Aprimorada

Esta versão inclui melhorias significativas na configuração SSL para resolver problemas de download de vídeos do YouTube.

## Alterações Principais

1. **Configuração SSL Aprimorada**
   - Múltiplas técnicas de contorno de SSL implementadas
   - Certificados adicionais incluídos
   - Script fix_ssl.py para configuração automática

2. **Métodos de Download Aprimorados**
   - Script enhanced_youtube_downloader.py com múltiplos métodos de fallback
   - Configurações otimizadas para contornar restrições

## Passos para Implantação

### 1. Construir a Imagem Docker

\`\`\`bash
docker build -t youtube-api:latest .
\`\`\`

### 2. Implantar no Portainer

1. Acesse o Portainer
2. Vá para Stacks > Add stack
3. Dê um nome como 'youtube-api-enhanced'
4. Faça upload do arquivo docker-compose.yml
5. Clique em 'Deploy the stack'

### 3. Verificar a Implantação

Acesse a API em: https://api2.lukao.tv/health

### 4. Testar o Download

Faça uma requisição para:
https://api2.lukao.tv/downloads?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
EOL

# Criar arquivo zip para fácil transferência
echo -e "${YELLOW}Criando arquivo zip...${NC}"
zip -r youtube-api-enhanced-deploy.zip $DEPLOY_DIR

# Limpar diretório temporário
rm -rf $DEPLOY_DIR

echo -e "${GREEN}Pacote de implantação criado: youtube-api-enhanced-deploy.zip${NC}"
echo ""
echo -e "${YELLOW}Instruções para implantação:${NC}"
echo "1. Transfira o arquivo youtube-api-enhanced-deploy.zip para o servidor:"
echo "   scp youtube-api-enhanced-deploy.zip usuario@seu-servidor:/caminho/destino/"
echo ""
echo "2. No servidor, extraia o arquivo:"
echo "   unzip youtube-api-enhanced-deploy.zip"
echo ""
echo "3. Construa a imagem Docker:"
echo "   cd deploy-enhanced-package"
echo "   docker build -t youtube-api:latest ."
echo ""
echo "4. Implante usando o Portainer UI:"
echo "   - Acesse o Portainer"
echo "   - Vá para Stacks > Add stack"
echo "   - Dê um nome como 'youtube-api-enhanced'"
echo "   - Faça upload do arquivo docker-compose.yml do diretório extraído"
echo "   - Clique em 'Deploy the stack'"
echo ""
echo -e "${GREEN}Após a implantação, a API estará disponível em: https://api2.lukao.tv${NC}"
echo -e "${GREEN}Teste o download com: https://api2.lukao.tv/downloads?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ${NC}"
