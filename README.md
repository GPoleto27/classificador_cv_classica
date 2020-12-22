# Classificador de Veículos com Visão Computacional clássica

Aplicação em python de um classificador utilizando visão computacional clássica para classificação de uma área de interesse de um vídeo.
[Video DEMO]()

# Instalação e execução

## Clonando o Repositório

    $ git clone https://github.com/GPoleto27/classificador_cv_classica

## Instalando as dependências, configurações e pesos da rede

    $ cd classificador_cv_classica
    $ sudo chmod +x setup.sh
    $ ./setup.sh

## Execute a aplicação

    $ ./main.py

# Customização da aplicação

## Alterando a fonte do vídeo

Adicione o argumento _-v_ ou *--video_source*

> Altere essa variável para utilizar outros videos ou câmeras.

Você pode usar seu próprio arquivo de vídeo ou webcam.

Para arquivo, apenas modifique o nome do arquivo, para usar sua webcam, altere para um inteiro que irá indicar o índice de sua webcam.

> (Normalmente, se há apenas uma câmera, basta utilizar o valor 0).

## Alterando os frames por segundo

Adicione o argumento _-f_ ou *--fps*

## Alterando altura e largura mínima de validação

Adicione o argumento _-mh_ ou *--min_height* para alterar a altura mínima para validar uma caixa limitante como pertencente a um carro

Adicione o argumento _-mw_ ou *--min_width* para alterar a largura mínima para validar uma caixa limitante como pertencente a um carro

# TODO

- Criar um Docker
