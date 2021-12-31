# Visao Computacional 

## Proposta 
O algoritmo deve:
- Acessar a câmera ou arquivo de vídeo;
- Exibir o retângulo ao redor dos rostos;
- Mostrar o nome da pessoa ou o termo: DESCONHECIDO quando não estiver registrado na rede neural;
- Descrever a expressão facial junto com o nome da pessoa;
- Ocultar as pessoas (mostrar o plano de fundo normal) caso elas se escondam atras de algum objeto colorido (pode ser a ideia do cromakey).

## Execução
Para rodar o programa, crie uma venv com o comando:

```
virtualenv venv 
```

Para ativar a venv:

```
source venv/bin/activate 
```

Se der erro na execução, favor verificar se não falta fazer um:

```
sudo apt-get install python-dev 
```
ou 
```
sudo apt-get install python3-dev
```

A dlib precisa ser instalada após a cmake. Caso dê erro, tente fazer manualmente.

Instale todas as dependências com:
```
pip3 install -r requirements.txt
```
Para navegar entre as imagens de background, pressione "a" ou "d".
Para parar o código, pressione "q".

## Downloads 
- Convolutional neural network for emotion recognition in faces: https://github.com/onnx/models/blob/master/vision/body_analysis/emotion_ferplus/README.md

## Resultado
![Readme1](./Imagens/Readme/readme1.png)
![Readme2](./Imagens/Readme/readme2.png)
