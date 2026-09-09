# Relatório Técnico - Laboratórios M1

## 1. Identificação

**Estudante:** Victor Hugo Chrisosthemos Teixeira
<br>**Disciplina:** Processamento Digital de Imagens  
**Laboratórios:** M1.1, M1.2 e M1.3  
**Linguagem utilizada:** Python

---

## 2. Objetivo

O objetivo dos laboratórios foi implementar manualmente operações básicas de processamento digital de imagens, evitando o uso de funções prontas que realizassem diretamente os algoritmos avaliados.

Na M1.1 foram trabalhados representação da imagem, canais de cor, conversão para níveis de cinza e quantização. Na M1.2 foram implementadas transformações de intensidade e histograma. Na M1.3 foram estudadas operações de vizinhança, convolução, filtros espaciais e detecção de bordas.

---

## 3. Operações implementadas

### M1.1

Foram implementadas:

- inspeção das características da imagem;
- cópia manual pixel a pixel;
- separação dos canais azul, verde e vermelho;
- conversão para níveis de cinza pela média simples;
- conversão para níveis de cinza pela média ponderada;
- quantização para diferentes quantidades de níveis.

As operações da M1.1 foram feitas com percurso explícito dos pixels, conforme solicitado no enunciado. :contentReference[oaicite:1]{index=1}

### M1.2

Foram implementadas:

- ajuste de brilho;
- ajuste de contraste;
- negativo;
- limiarização binária;
- cálculo manual do histograma.

O histograma utiliza uma estrutura com 256 posições para contabilizar a quantidade de pixels de cada intensidade. :contentReference[oaicite:2]{index=2}

### M1.3

Foram implementadas:

- convolução genérica;
- tratamento de bordas por cópia e replicação;
- filtro de média;
- média ponderada;
- Laplaciano;
- Sobel nas direções X e Y;
- cálculo das magnitudes do gradiente.

A convolução e o acesso às vizinhanças também foram implementados manualmente. :contentReference[oaicite:3]{index=3}

---

## 4. Decisões de implementação

O projeto foi desenvolvido em Python e dividido principalmente entre `main.py` e `functions.py`.

O arquivo `main.py` é responsável por receber os parâmetros da linha de comando, carregar as imagens e selecionar a operação solicitada. O arquivo `functions.py` contém a implementação dos algoritmos.

Foram utilizadas bibliotecas apenas como apoio para leitura, escrita e armazenamento das imagens. As operações avaliadas foram realizadas percorrendo manualmente os pixels ou suas vizinhanças.

Durante os cálculos foram utilizados tipos numéricos adequados para evitar overflow. A conversão para o intervalo de 0 a 255 é realizada somente quando necessária para produzir a imagem final.

Na convolução foram consideradas duas estratégias de borda: `copy`, que mantém o valor original quando a vizinhança não cabe completamente, e `replicate`, que utiliza o pixel válido mais próximo.

Esses cuidados são importantes principalmente para contraste, convolução, Laplaciano e Sobel. :contentReference[oaicite:4]{index=4}

---

## 5. Testes realizados

Foram realizados testes automatizados com `pytest` e testes manuais utilizando imagens reais e sintéticas.

A execução dos testes automatizados apresentou:

```text
7 passed
