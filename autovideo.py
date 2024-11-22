from moviepy.editor import ImageClip, CompositeVideoClip
from PIL import Image

def redimensionar_imagem(caminho_imagem, largura, altura):
    with Image.open(caminho_imagem) as img:
        img = img.resize((largura, altura), Image.LANCZOS)
        img.save(caminho_imagem)  # Sobrescreve a imagem original

def criar_video(imagens, duracao_por_imagem, imagem_fundo, caminho_saida):
    # Redimensionar a imagem de fundo para 1920x1080
    redimensionar_imagem(imagem_fundo, 1920, 1080)

    # Criar o fundo do vídeo com a imagem padrão
    fundo = ImageClip(imagem_fundo).set_duration(duracao_por_imagem * len(imagens))

    # Lista para armazenar os clips de imagem
    clips = []

    for i, imagem in enumerate(imagens):
        # Redimensionar cada imagem para 1000x600
        redimensionar_imagem(imagem, 1000, 600)

        # Criar clip da imagem redimensionada
        clip_imagem = (ImageClip(imagem)
                      .set_duration(duracao_por_imagem + 2)  # Duração total da imagem na tela
                      .set_position(lambda t: (1920 * (t / (duracao_por_imagem + 2) - 1), 350))  # Movido mais para baixo
                      .set_start(i * (duracao_por_imagem + 1)))  # Começa após a anterior, considerando fade

        # Adicionando efeito de transição suave
        if i > 0:  # Para todas as imagens após a primeira
            clip_imagem = clip_imagem.crossfadein(1)  # Transição suave de 1 segundo

        clips.append(clip_imagem)

    # Adicionar animação de fade out ao último clip
    if clips:
        last_clip = clips[-1].fadeout(1)  # Fade out de 1 segundo
        clips[-1] = last_clip

    # Combinar o fundo com as imagens sobrepostas
    video = CompositeVideoClip([fundo] + clips)

    # Exportar o vídeo
    video.set_duration(duracao_por_imagem * len(imagens)).write_videofile(caminho_saida, codec="libx264", fps=24)

# Exemplo de uso:
imagens = [f"teste{i}.png" for i in range(1, 3)]
duracao_por_imagem = 5  # Duração de exibição de cada imagem
imagem_fundo = "diretorio/da/imagem/de/fundo"  # Certifique-se de que este arquivo existe
caminho_saida = "video_carrossel_suave.mp4"

criar_video(imagens, duracao_por_imagem, imagem_fundo, caminho_saida)
