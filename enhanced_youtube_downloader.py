#!/usr/bin/env python3
"""
Script aprimorado para download de vídeos do YouTube com múltiplas técnicas de contorno de SSL.
"""

import os
import sys
import ssl
import certifi
import subprocess
import tempfile
import shutil
import urllib.request
import requests
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("enhanced-downloader")

# 1. Configuração SSL robusta
def configure_ssl():
    """Configurar SSL com todas as técnicas possíveis."""
    logger.info("Configurando SSL com técnicas avançadas...")
    
    # Usar certificados certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl._create_default_https_context = lambda: ssl_context
    
    # Configurar urllib
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)
    
    # Desativar avisos de SSL no requests
    requests.packages.urllib3.disable_warnings()
    
    # Definir variáveis de ambiente
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    
    # Carregar o script fix_ssl.py se existir
    fix_ssl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fix_ssl.py")
    if os.path.exists(fix_ssl_path):
        logger.info(f"Carregando configurações de {fix_ssl_path}")
        with open(fix_ssl_path) as f:
            exec(f.read())
    
    logger.info("Configuração SSL concluída.")

# 2. Função de download com yt-dlp aprimorada
def download_with_enhanced_yt_dlp(url, output_path):
    """Download com yt-dlp usando configurações otimizadas."""
    logger.info(f"Baixando {url} com yt-dlp aprimorado...")
    
    # Criar diretório temporário
    temp_dir = tempfile.mkdtemp(prefix="yt-dlp-enhanced-")
    temp_output = os.path.join(temp_dir, "audio.%(ext)s")
    
    try:
        # Comando com todas as opções possíveis
        cmd = [
            "yt-dlp",
            "--no-check-certificate",      # Ignorar verificação de certificado
            "--no-cache-dir",              # Desativar cache
            "--geo-bypass",                # Contornar restrições geográficas
            "--force-ipv4",                # Forçar IPv4
            "--ignore-errors",             # Continuar em caso de erros
            "--no-warnings",               # Suprimir avisos
            "--prefer-insecure",           # Preferir conexões inseguras
            "--force-generic-extractor",   # Usar extrator genérico
            "--extractor-args", "youtube:player_client=android,web", # Usar cliente Android/Web
            "--legacy-server-connect",     # Usar conexão de servidor legada
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "--extract-audio",             # Extrair áudio
            "--audio-format", "mp3",       # Converter para mp3
            "--audio-quality", "192k",     # Definir qualidade de áudio
            "--output", temp_output,       # Definir template de saída
            url                            # URL do YouTube
        ]
        
        # Executar comando
        logger.info(f"Executando comando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Verificar se o comando foi bem-sucedido
        if result.returncode != 0:
            logger.error(f"Comando falhou com código {result.returncode}")
            logger.error(f"Erro: {result.stderr}")
            return False
        
        # Encontrar o arquivo de saída
        for file in os.listdir(temp_dir):
            if file.endswith(".mp3"):
                mp3_path = os.path.join(temp_dir, file)
                # Copiar para destino final
                shutil.copy2(mp3_path, output_path)
                logger.info(f"Download concluído: {output_path}")
                return True
        
        logger.error("Nenhum arquivo MP3 encontrado no diretório de saída")
        return False
    
    finally:
        # Limpar diretório temporário
        shutil.rmtree(temp_dir, ignore_errors=True)

# 3. Função de download com yt-dlp Python
def download_with_yt_dlp_python(url, output_path):
    """Download usando a biblioteca Python yt-dlp."""
    logger.info(f"Baixando {url} com biblioteca yt-dlp...")
    
    try:
        import yt_dlp
        
        # Criar diretório temporário
        temp_dir = tempfile.mkdtemp(prefix="yt-dlp-python-")
        temp_output = os.path.join(temp_dir, "audio.%(ext)s")
        
        try:
            # Configurar opções avançadas
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': temp_output,
                'quiet': False,
                'no_warnings': False,
                'ignoreerrors': True,
                'geo_bypass': True,
                'nocheckcertificate': True,
                'socket_timeout': 60,
                'verbose': True,
                'force_generic_extractor': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'skip': ['webpage', 'dash', 'hls'],
                    }
                },
                'external_downloader_args': ['-v'],
                'cookiefile': None,
                'source_address': '0.0.0.0',
                'legacy_server_connect': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'max-age=0',
                },
                'compat_opts': ['no-youtube-unavailable-videos', 'no-youtube-prefer-utc-upload-date'],
            }
            
            # Baixar vídeo
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logger.info(f"Baixando áudio com yt-dlp: {url}")
                ydl.download([url])
            
            # Encontrar o arquivo de saída
            for file in os.listdir(temp_dir):
                if file.endswith(".mp3"):
                    mp3_path = os.path.join(temp_dir, file)
                    # Copiar para destino final
                    shutil.copy2(mp3_path, output_path)
                    logger.info(f"Download concluído: {output_path}")
                    return True
            
            logger.error("Nenhum arquivo MP3 encontrado no diretório de saída")
            return False
            
        finally:
            # Limpar diretório temporário
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except ImportError:
        logger.error("Biblioteca yt-dlp não está instalada")
        return False
    except Exception as e:
        logger.error(f"Erro ao usar biblioteca yt-dlp: {str(e)}")
        return False

# 4. Função de download com pytube
def download_with_pytube(url, output_path):
    """Download usando a biblioteca pytube."""
    logger.info(f"Baixando {url} com pytube...")
    
    try:
        from pytube import YouTube
        
        # Criar diretório temporário
        temp_dir = tempfile.mkdtemp(prefix="pytube-")
        
        try:
            # Criar objeto YouTube
            yt = YouTube(url)
            
            # Obter stream de áudio
            audio_stream = yt.streams.filter(only_audio=True).first()
            if not audio_stream:
                logger.error("Nenhum stream de áudio encontrado")
                return False
            
            # Baixar áudio
            temp_audio_path = audio_stream.download(output_path=temp_dir)
            logger.info(f"Áudio baixado para: {temp_audio_path}")
            
            # Converter para mp3 usando ffmpeg
            try:
                # Construir comando ffmpeg
                ffmpeg_cmd = [
                    "ffmpeg",
                    "-i", temp_audio_path,
                    "-vn",  # Sem vídeo
                    "-ar", "44100",  # Taxa de amostragem
                    "-ac", "2",  # Estéreo
                    "-b:a", "192k",  # Bitrate
                    "-f", "mp3",  # Formato
                    output_path
                ]
                
                # Executar ffmpeg
                logger.info(f"Convertendo para mp3 com ffmpeg: {' '.join(ffmpeg_cmd)}")
                result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
                
                # Verificar se a conversão foi bem-sucedida
                if result.returncode != 0:
                    logger.warning(f"Conversão ffmpeg falhou: {result.stderr}")
                    # Se a conversão falhou, apenas renomear o arquivo
                    shutil.copy2(temp_audio_path, output_path)
            except Exception as e:
                logger.warning(f"Erro ao converter para mp3: {str(e)}")
                # Se a conversão falhou, apenas renomear o arquivo
                shutil.copy2(temp_audio_path, output_path)
            
            logger.info(f"Download concluído: {output_path}")
            return True
            
        finally:
            # Limpar diretório temporário
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except ImportError:
        logger.error("Biblioteca pytube não está instalada")
        return False
    except Exception as e:
        logger.error(f"Erro ao usar pytube: {str(e)}")
        return False

# 5. Função de download com youtube-dl
def download_with_youtube_dl(url, output_path):
    """Download usando o comando youtube-dl."""
    logger.info(f"Baixando {url} com youtube-dl...")
    
    try:
        # Construir comando
        cmd = [
            "youtube-dl",
            "--no-check-certificate",
            "--no-cache-dir",
            "--geo-bypass",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "192k",
            "-o", output_path,
            url
        ]
        
        # Executar comando
        logger.info(f"Executando comando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Verificar se o comando foi bem-sucedido
        if result.returncode != 0:
            logger.error(f"Comando falhou com código {result.returncode}")
            logger.error(f"Erro: {result.stderr}")
            return False
        
        logger.info(f"Download concluído: {output_path}")
        return os.path.exists(output_path)
        
    except Exception as e:
        logger.error(f"Erro ao usar youtube-dl: {str(e)}")
        return False

# 6. Função principal com múltiplos métodos de fallback
def main():
    if len(sys.argv) < 2:
        print("Uso: python enhanced_youtube_downloader.py <youtube_url> [output_path]")
        return 1
    
    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.mp3"
    
    logger.info(f"Iniciando download aprimorado de {url} para {output_path}")
    
    # Configurar SSL
    configure_ssl()
    
    # Lista de métodos de download para tentar
    download_methods = [
        download_with_enhanced_yt_dlp,
        download_with_yt_dlp_python,
        download_with_pytube,
        download_with_youtube_dl
    ]
    
    # Tentar cada método
    for method in download_methods:
        logger.info(f"Tentando método: {method.__name__}")
        try:
            if method(url, output_path):
                logger.info(f"Download concluído com sucesso usando {method.__name__}!")
                print(f"Download concluído com sucesso: {output_path}")
                return 0
        except Exception as e:
            logger.error(f"Método {method.__name__} falhou: {str(e)}")
    
    logger.error("Todos os métodos de download falharam.")
    print("Todos os métodos de download falharam.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
