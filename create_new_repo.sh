#!/bin/bash
# Script para desvincular o projeto do repositório atual e criar um novo repositório

# Cores para saída
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Desvinculando o projeto do repositório atual...${NC}"

# Verificar se o diretório .git existe
if [ -d ".git" ]; then
    # Remover o diretório .git
    rm -rf .git
    echo -e "${GREEN}Diretório .git removido com sucesso.${NC}"
else
    echo -e "${YELLOW}Diretório .git não encontrado. O projeto já está desvinculado.${NC}"
fi

# Inicializar um novo repositório Git
echo -e "${YELLOW}Inicializando um novo repositório Git...${NC}"
git init
echo -e "${GREEN}Novo repositório Git inicializado.${NC}"

# Adicionar todos os arquivos
echo -e "${YELLOW}Adicionando arquivos ao novo repositório...${NC}"
git add .

# Fazer o primeiro commit
echo -e "${YELLOW}Fazendo o primeiro commit...${NC}"
git commit -m "Versão inicial da API de Transcrição e Download do YouTube"
echo -e "${GREEN}Primeiro commit realizado.${NC}"

echo -e "${YELLOW}Próximos passos:${NC}"
echo "1. Crie um novo repositório no GitHub com o nome 'youtube_claude'"
echo "2. Execute os seguintes comandos para vincular e enviar o código para o novo repositório:"
echo ""
echo "   git remote add origin https://github.com/SEU_USUARIO/youtube_claude.git"
echo "   git push -u origin main"
echo ""
echo -e "${GREEN}O projeto foi desvinculado do repositório atual e está pronto para ser enviado para um novo repositório.${NC}"
