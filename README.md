# API de Transcrição e Download do YouTube

Uma API Flask que fornece endpoints para transcrever vídeos do YouTube e baixá-los como arquivos MP3. Projetada para ser implantada em um servidor Ubuntu com Portainer e acessível através do domínio `api2.lukao.tv`.

## Funcionalidades

- Transcrição de vídeos do YouTube para texto
- Download de vídeos do YouTube como arquivos MP3
- Interface web amigável
- API RESTful simples
- Integração com Traefik para roteamento

## Instalação

### Configuração Automática (Recomendada)

O repositório inclui um script de configuração que automatiza o processo de instalação:

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd youtube-api
```

2. Execute o script de configuração:
```bash
./setup.sh
```

O script irá:
- Verificar as dependências necessárias (Python, pip, ffmpeg)
- Criar um ambiente virtual
- Instalar os pacotes Python necessários
- Criar um arquivo .env padrão
- Criar o diretório temporário
- Fornecer instruções para executar a API

### Configuração Manual

Se preferir configurar manualmente:

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd youtube-api
```

2. Crie e ative um ambiente virtual (recomendado):
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` no diretório raiz (opcional):
```bash
cp .env.example .env
```

5. Crie um diretório temporário:
```bash
mkdir -p temp
```

6. Execute a aplicação:
```bash
python app.py
```

A API estará disponível em `http://localhost:5000`.

## Interface Web

A API inclui uma interface web amigável que permite:
- Transcrever vídeos do YouTube
- Baixar vídeos do YouTube como arquivos MP3

Para acessar a interface web, basta abrir seu navegador e navegar para:
```
http://localhost:5000
```

Após a implantação no Portainer, a interface estará disponível em:
```
https://api2.lukao.tv
```

## Endpoints da API

### Verificação de Saúde

**Endpoint:** `/health`

**Método:** GET

**Resposta:**
```json
{
    "status": "ok",
    "version": "1.0.0",
    "whisper_model": "base",
    "hostname": "container-id"
}
```

### Transcrever um Vídeo do YouTube

**Endpoint:** `/transcribe`

**Método:** POST

**Corpo da Requisição:**
```json
{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Resposta:**
```json
{
    "transcription": "Texto completo da transcrição...",
    "segments": [
        {
            "id": 0,
            "start": 0.0,
            "end": 2.5,
            "text": "Texto do segmento..."
        },
        ...
    ]
}
```

### Baixar um Vídeo do YouTube como MP3

**Endpoint:** `/downloads`

**Método:** GET

**Parâmetros de Consulta:**
- `url`: A URL do vídeo do YouTube

**Resposta:**
- Download do arquivo MP3

## Exemplos de Uso

### Usando cURL

#### Transcrever um Vídeo

```bash
curl -X POST https://api2.lukao.tv/transcribe \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

#### Baixar um Vídeo como MP3

```bash
curl -X GET "https://api2.lukao.tv/downloads?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o download.mp3
```

Ou simplesmente acesse no seu navegador:
```
https://api2.lukao.tv/downloads?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Usando os Scripts de Teste

O repositório inclui dois scripts de teste que demonstram como usar a API:

#### Script Python

O script Python (`test.py`) fornece uma maneira programática de interagir com a API:

```bash
python test.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --action transcribe
python test.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --action download --output minha_musica.mp3
python test.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Ambos transcrição e download
python test.py --help  # Para mais opções
```

#### Script Shell

O script Shell (`test.sh`) fornece uma maneira mais amigável de interagir com a API:

```bash
./test.sh -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Ambos transcrição e download
./test.sh -a transcribe -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Apenas transcrição
./test.sh -a download -o minha_musica.mp3 -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Apenas download
./test.sh --help  # Para mais opções
```

## Implantação

Este projeto foi projetado para ser implantado em um servidor Ubuntu com Portainer, usando Traefik como proxy reverso. Fornecemos várias opções de implantação:

### Implantação no Portainer

Para implantar no Portainer, consulte os seguintes guias:

- [DEPLOY.md](DEPLOY.md) - Instruções detalhadas para implantar no Portainer
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - Como configurar um repositório GitHub e cloná-lo no VPS

Você também pode usar o script de implantação automatizado:

```bash
./deploy-to-portainer.sh
```

Este script prepara um pacote com todos os arquivos necessários e fornece instruções para upload e implantação.

### Implantação Local com Docker

Para implantação local com Docker:

```bash
# Construir e iniciar o contêiner com Docker Compose
docker-compose up -d

# Para parar o contêiner
docker-compose down
```

### Implantação Local com Gunicorn

Para implantação local com Gunicorn:

```bash
# Usando o script run.sh
./run.sh -m production

# Ou diretamente com Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Implantação Local para Desenvolvimento

Para desenvolvimento local:

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
python app.py
```

## Notas

- A API usa o modelo Whisper da OpenAI para transcrição, o que requer recursos computacionais suficientes.
- Para uso em produção, considere implementar limitação de taxa e autenticação.
- Os arquivos temporários são automaticamente limpos após o processamento.
- A API foi projetada para ser implantada em um servidor Ubuntu com Portainer e Traefik.
- O domínio `api2.lukao.tv` deve estar apontado para o servidor antes da implantação.
