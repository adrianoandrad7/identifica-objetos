# Identifica-Objetos

## Descrição

O projeto "identifica-objetos" é uma aplicação que utiliza técnicas de visão computacional para contar, identificar e classificar objetos em imagens. 

## Instalação
Para instalar e configurar o projeto, siga os passos abaixo:

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/identifica-objetos.git
    cd identifica-objetos
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Caso de Uso

Foi gravado um vídeo no prédio didático do IFMG campus Ouro Branco utilizando uma câmera fixa, com o objetivo de detectar e contar pessoas presentes no cenário. O sistema processará o vídeo para identificar e marcar as pessoas com bounding boxes (retângulos coloridos ao redor delas), facilitando a visualização e contagem.

Além disso, o sistema incluirá uma segunda fase para classificar os objetos detectados em três categorias: (A) Adultos, (B) Crianças ou (C) Animais. Essa classificação será feita com base no formato e tamanho dos objetos identificados, utilizando os bounding boxes como referência. A análise será baseada em técnicas de processamento de imagem, sem a necessidade de aprendizado de máquina.

Este caso de uso visa aplicar técnicas de processamento de imagem para monitorar e classificar pessoas e animais em ambientes abertos, oferecendo uma solução para controle e análise de movimentação.
