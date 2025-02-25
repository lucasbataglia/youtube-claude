# Implantação da API de Transcrição e Download do YouTube no Portainer

Este guia explica como implantar a API de Transcrição e Download do YouTube em um servidor Ubuntu usando Portainer.

## Pré-requisitos

- Servidor Ubuntu com Docker e Portainer instalados
- Domínio `api2.lukao.tv` apontando para o servidor
- Stacks Traefik, Postgres e Redis já implantados no Portainer

## Arquivos de Stack

O projeto inclui os seguintes arquivos de stack:

- `stacks-files/traefik`: Configuração do Traefik (já implantado)
- `stacks-files/postgres`: Configuração do PostgreSQL (já implantado)
- `stacks-files/redis`: Configuração do Redis (já implantado)
- `stacks-files/youtube-api`: Configuração da API de Transcrição e Download do YouTube

## Passos para Implantação

### 1. Preparar o Projeto

1. Clone o repositório no seu ambiente local:
   ```bash
   git clone <url-do-repositorio>
   cd youtube-claude
   ```

2. Faça upload do projeto para o servidor ou use um repositório Git para implantação.

### 2. Implantar no Portainer

1. Acesse o Portainer no seu servidor.

2. Navegue até "Stacks" e clique em "Add stack".

3. Dê um nome ao stack, como "youtube-api".

4. Na seção "Build method", selecione "Upload" e faça upload do arquivo `stacks-files/youtube-api`.
   
   Alternativamente, você pode copiar e colar o conteúdo do arquivo no editor de texto do Portainer.

5. Clique em "Deploy the stack".

6. O Portainer irá construir a imagem Docker e implantar o serviço.

### 3. Verificar a Implantação

1. Após a implantação, verifique se o serviço está em execução na seção "Stacks" do Portainer.

2. Acesse `https://api2.lukao.tv` no seu navegador para verificar se a API está funcionando.

3. Teste a API usando os endpoints:
   - `https://api2.lukao.tv/health`: Verificar o status da API
   - `https://api2.lukao.tv/transcribe`: Transcrever vídeos do YouTube
   - `https://api2.lukao.tv/downloads`: Baixar vídeos do YouTube como MP3

## Solução de Problemas

Se encontrar problemas durante a implantação:

1. Verifique os logs do contêiner no Portainer para identificar erros.

2. Certifique-se de que as redes `traefik_public` e `digital_network` existem e estão configuradas corretamente.

3. Verifique se o Traefik está configurado corretamente para rotear o tráfego para o domínio `api2.lukao.tv`.

4. Certifique-se de que o volume `youtube_temp` foi criado corretamente.

## Configuração Avançada

### Ajustar Recursos

Se precisar ajustar os recursos alocados para o serviço, modifique as seguintes linhas no arquivo `stacks-files/youtube-api`:

```yaml
resources:
  limits:
    cpus: "1"
    memory: 2048M
```

### Configurar Variáveis de Ambiente

Para ajustar as configurações da aplicação, modifique as variáveis de ambiente no arquivo `stacks-files/youtube-api`:

```yaml
environment:
  - WHISPER_MODEL=base
  - FLASK_ENV=production
  - FLASK_DEBUG=0
  - PORT=5000
  - TEMP_DIR=/app/temp
