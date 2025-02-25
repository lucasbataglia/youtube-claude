# Configuração do Repositório GitHub e Deploy no VPS

Este guia explica como configurar um novo repositório GitHub para o projeto, cloná-lo no seu VPS e fazer o deploy no Portainer.

## 1. Preparar o Projeto para o GitHub

### Verificar o .gitignore

O projeto já possui um arquivo `.gitignore` que exclui arquivos desnecessários. Certifique-se de que ele inclui:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env

# Temporary files
temp/
*.mp3
*.wav

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS specific
.DS_Store
Thumbs.db
```

### Remover Referências ao Repositório Antigo

Se houver qualquer referência ao repositório antigo, remova-as:

```bash
rm -rf .git
```

## 2. Criar um Novo Repositório no GitHub

1. Acesse [GitHub](https://github.com) e faça login na sua conta.
2. Clique no botão "+" no canto superior direito e selecione "New repository".
3. Dê um nome ao repositório, como "youtube-api".
4. Adicione uma descrição, como "API para transcrição e download de vídeos do YouTube".
5. Escolha se o repositório será público ou privado.
6. Não inicialize o repositório com README, .gitignore ou licença, pois já temos esses arquivos.
7. Clique em "Create repository".

## 3. Inicializar o Repositório Local e Enviar para o GitHub

Após criar o repositório no GitHub, execute os seguintes comandos no diretório do projeto:

```bash
# Inicializar o repositório Git local
git init

# Adicionar todos os arquivos
git add .

# Fazer o primeiro commit
git commit -m "Versão inicial da API de Transcrição e Download do YouTube"

# Adicionar o repositório remoto (substitua USERNAME pelo seu nome de usuário do GitHub)
git remote add origin https://github.com/USERNAME/youtube-api.git

# Enviar o código para o GitHub
git push -u origin main
```

## 4. Clonar o Repositório no VPS

Acesse seu VPS via SSH e clone o repositório:

```bash
# Acesse o diretório onde deseja clonar o repositório
cd /caminho/para/diretorio

# Clone o repositório (substitua USERNAME pelo seu nome de usuário do GitHub)
git clone https://github.com/USERNAME/youtube-api.git

# Acesse o diretório do projeto
cd youtube-api
```

## 5. Fazer o Deploy no Portainer

Existem duas maneiras de fazer o deploy no Portainer:

### Opção 1: Usando a Interface Web do Portainer

1. Acesse o Portainer no seu VPS.
2. Navegue até "Stacks" e clique em "Add stack".
3. Dê um nome ao stack, como "youtube-api".
4. Na seção "Build method", selecione "Repository" ou "Upload".
   - Se selecionar "Repository", informe o caminho para o repositório no VPS.
   - Se selecionar "Upload", faça upload do arquivo `stacks-files/youtube-api`.
5. Clique em "Deploy the stack".

### Opção 2: Usando o Arquivo de Stack Diretamente

1. No VPS, copie o arquivo de stack para um local acessível pelo Portainer:

```bash
# Copie o arquivo de stack para um diretório específico
cp stacks-files/youtube-api /caminho/para/stacks/youtube-api.yml
```

2. No Portainer, navegue até "Stacks" e clique em "Add stack".
3. Dê um nome ao stack, como "youtube-api".
4. Na seção "Build method", selecione "Upload" e faça upload do arquivo `youtube-api.yml`.
5. Clique em "Deploy the stack".

## 6. Verificar a Implantação

Após a implantação, verifique se o serviço está em execução:

1. No Portainer, navegue até "Stacks" e verifique o status do stack "youtube-api".
2. Acesse `https://api2.lukao.tv` no seu navegador para verificar se a API está funcionando.
3. Teste a API usando os endpoints:
   - `https://api2.lukao.tv/health`: Verificar o status da API
   - `https://api2.lukao.tv/transcribe`: Transcrever vídeos do YouTube
   - `https://api2.lukao.tv/downloads`: Baixar vídeos do YouTube como MP3
