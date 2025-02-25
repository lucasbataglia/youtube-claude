# YouTube API com Configuração SSL Aprimorada

Este projeto inclui melhorias significativas na configuração SSL para resolver problemas de download de vídeos do YouTube, especialmente o erro `[SSL: CERTIFICATE_VERIFY_FAILED]`.

## Soluções Implementadas

1. **Instalação de Certificados SSL**
   - Script `install_macos_certificates.py` para instalar certificados SSL no macOS
   - Configuração de variáveis de ambiente para certificados SSL
   - Script `fix_ssl.py` para configuração automática do contexto SSL

2. **Script de Download Aprimorado**
   - `enhanced_youtube_downloader.py` combina múltiplas técnicas de contorno de SSL
   - Implementa vários métodos de download com fallback automático
   - Usa configurações otimizadas para contornar restrições de SSL

3. **Configuração SSL Robusta no app.py**
   - Função `configure_ssl()` que aplica múltiplas técnicas de contorno
   - Carrega automaticamente o script `fix_ssl.py` se existir

4. **Dockerfile Aprimorado**
   - Instalação de certificados SSL adicionais
   - Configuração de variáveis de ambiente para SSL
   - Criação automática do script `fix_ssl.py`

5. **Stack do Portainer Aprimorado**
   - Volume dedicado para certificados SSL
   - Configuração de variáveis de ambiente para SSL
   - Verificação de saúde para monitoramento

## Como Usar Localmente

### Testar o Download Aprimorado

```bash
# Instalar certificados SSL (apenas para macOS)
python install_macos_certificates.py

# Testar o download aprimorado
python enhanced_youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" "output.mp3"

# Testar a configuração SSL e métodos de download
python test_ssl_and_download.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Executar a API Localmente

```bash
# Construir e iniciar o contêiner Docker
docker-compose up --build
```

## Como Implantar no Portainer

### Método 1: Usando o Script de Implantação

```bash
# Executar o script de implantação
./deploy-enhanced-to-portainer.sh

# Seguir as instruções exibidas pelo script
```

### Método 2: Implantação Manual

1. **Construir a Imagem Docker**
   ```bash
   docker build -t youtube-api:latest .
   ```

2. **Copiar os Arquivos Necessários para o Servidor**
   ```bash
   scp -r app.py requirements.txt Dockerfile templates static enhanced_youtube_downloader.py fix_ssl.py stacks-files/youtube-api-enhanced usuario@seu-servidor:/caminho/destino/
   ```

3. **No Servidor, Construir a Imagem**
   ```bash
   cd /caminho/destino
   docker build -t youtube-api:latest .
   ```

4. **Implantar no Portainer**
   - Acesse o Portainer
   - Vá para Stacks > Add stack
   - Dê um nome como 'youtube-api-enhanced'
   - Faça upload do arquivo `youtube-api-enhanced` como docker-compose.yml
   - Clique em 'Deploy the stack'

## Verificar a Implantação

- Verificar a saúde da API: https://api2.lukao.tv/health
- Testar o download: https://api2.lukao.tv/downloads?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
- Testar a transcrição: https://api2.lukao.tv/transcribe (POST com JSON: {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})

## Solução de Problemas

Se ainda houver problemas com o download de vídeos do YouTube:

1. **Verificar Logs do Contêiner**
   ```bash
   docker logs <container_id>
   ```

2. **Testar Diferentes Métodos de Download**
   ```bash
   python test_ssl_and_download.py "https://www.youtube.com/watch?v=VIDEO_ID"
   ```

3. **Atualizar o yt-dlp**
   ```bash
   pip install --upgrade yt-dlp
   ```

4. **Verificar Certificados SSL**
   ```bash
   python -c "import ssl; print(ssl.get_default_verify_paths())"
   ```
