# Laboratorios M1.1, M1.2 e M1.3 - Processamento de Imagens

Projeto em Python reunindo as atividades dos tres laboratorios da M1
<br>

# Antes de executar

1. Coloque sua imagem em `images/input/`.
2. Instale as dependências com `python -m pip install -r requirements.txt`.
3. No PowerShell, execute `$env:PYTHONPATH="src"`.
4. Ainda no PowerShell, no diretório do projeto, execute `python -m pytest -q` para conferir os testes.
5. Então execute as funções do programa usando `--input` e `--operation`.

Exemplo:

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation grayscale_weighted
```

A pasta `imagens_geradas` será criada automaticamente caso `--output` não seja informado.


## Estrutura do projeto

```text
src/pdi_lab/main.py
src/pdi_lab/functions.py
tests/test_laboratories.py
kernels/
images/input/
images/output/
results/
```

## Dependências

```powershell
python -m pip install -r requirements.txt
```

Não é obrigatório criar ambiente virtual para executar o projeto.

## Preparar o terminal no Windows PowerShell

Na raiz do projeto:

```powershell
$env:PYTHONPATH="src"
```

## Testes automatizados

```powershell
python -m pytest -q
```

Resultado esperado:

```text
7 passed
```

## Executar com uma imagem

Coloque sua imagem em `images/input/`. Exemplo com `romero_brito.jpg`:

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation inspect
```

Se `--output` não for informado, o programa cria automaticamente a pasta `imagens_geradas` no diretório atual.

## M1.1

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation copy
python -m pdi_lab --input images/input/romero_brito.jpg --operation channel_b
python -m pdi_lab --input images/input/romero_brito.jpg --operation channel_g
python -m pdi_lab --input images/input/romero_brito.jpg --operation channel_r
python -m pdi_lab --input images/input/romero_brito.jpg --operation grayscale_average
python -m pdi_lab --input images/input/romero_brito.jpg --operation grayscale_weighted
python -m pdi_lab --input images/input/romero_brito.jpg --operation quantize --levels 8
```

## M1.2

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation brightness --value 40
python -m pdi_lab --input images/input/romero_brito.jpg --operation contrast --alpha 1.5
python -m pdi_lab --input images/input/romero_brito.jpg --operation negative
python -m pdi_lab --input images/input/romero_brito.jpg --operation threshold --threshold 128
python -m pdi_lab --input images/input/romero_brito.jpg --operation histogram
```

## M1.3

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation mean_filter --kernel-size 3 --border replicate
python -m pdi_lab --input images/input/romero_brito.jpg --operation weighted_mean --border replicate
python -m pdi_lab --input images/input/romero_brito.jpg --operation convolution --kernel kernels/identity_3x3.txt --border replicate
python -m pdi_lab --input images/input/romero_brito.jpg --operation laplacian --border replicate
python -m pdi_lab --input images/input/romero_brito.jpg --operation sobel --border replicate
```

## Operações disponíveis

```text
inspect
copy
channel_b
channel_g
channel_r
grayscale_average
grayscale_weighted
quantize
brightness
contrast
negative
threshold
histogram
convolution
mean_filter
weighted_mean
laplacian
sobel
```


## Guardas

O programa verifica arquivo inexistente, falha na leitura, tipo diferente de `uint8`, quantidade de canais incompatível, parâmetros inválidos, níveis de quantização inválidos, limiar fora do intervalo, alpha negativo, kernel ausente, kernel vazio, kernel nao quadrado, dimensão par e estratégia de borda inválida.

## Limitações

A implementação foi feita para imagens `uint8`. As operações coloridas consideram três canais na ordem BGR usada pelo OpenCV. A convolução avaliada usa kernels quadrados de dimensão ímpar.

## Referências

- Enunciado do Laboratório M1.1 fornecido pela disciplina.
- Enunciado do Laboratório M1.2 fornecido pela disciplina.
- Enunciado do Laboratório M1.3 fornecido pela disciplina.
- Rubrica geral dos Laboratórios da M1.
- Contrato técnico dos Laboratórios da M1.

# Operações dos Laboratórios M1

## M1.1

Nesta etapa são executadas operações básicas sobre a imagem, trabalhando diretamente com os pixels.

### Cópia da imagem

Cria uma nova imagem copiando cada pixel da imagem original manualmente. O resultado deve ser idêntico à entrada.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation copy
```

### Canal azul

Mantém somente o canal azul da imagem e zera os canais verde e vermelho.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation channel_b
```

### Canal verde

Mantém somente o canal verde da imagem e zera os demais canais.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation channel_g
```

### Canal vermelho

Mantém somente o canal vermelho da imagem e zera os canais azul e verde.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation channel_r
```

### Conversão para cinza pela média

Converte a imagem colorida para níveis de cinza utilizando a média simples dos canais vermelho, verde e azul.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation grayscale_average
```

### Conversão para cinza ponderado

Converte a imagem para níveis de cinza utilizando pesos diferentes para cada canal. Dessa forma, os canais não contribuem igualmente para a intensidade final.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation grayscale_weighted
```

### Quantização

Reduz a quantidade de níveis de intensidade da imagem. No exemplo abaixo, a imagem é reduzida para 8 níveis.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation quantize --levels 8
```

---

## M1.2

Nesta etapa são aplicadas transformações diretamente sobre os valores de intensidade dos pixels.

### Ajuste de brilho

Soma um valor à intensidade de cada pixel. Neste exemplo é utilizado `40`, deixando a imagem mais clara. Valores acima do limite permitido são ajustados para o valor máximo.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation brightness --value 40
```

### Ajuste de contraste

Altera a diferença entre regiões claras e escuras da imagem. Com `alpha` igual a `1.5`, o contraste é aumentado.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation contrast --alpha 1.5
```

### Negativo

Inverte os níveis de intensidade da imagem. Regiões claras se tornam escuras e regiões escuras se tornam claras.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation negative
```

### Limiarização

Transforma a imagem em uma imagem binária. Pixels com intensidade abaixo de `128` recebem valor `0`, enquanto pixels com intensidade igual ou superior recebem valor `255`.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation threshold --threshold 128
```

### Histograma

Conta a quantidade de pixels existente em cada nível de intensidade, de `0` até `255`, e registra o resultado em formato textual/CSV.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation histogram
```

---

## M1.3

Nesta etapa são utilizadas operações baseadas na vizinhança dos pixels, por meio de kernels e convolução.

### Filtro de média

Aplica um filtro de média com kernel `3 x 3`. O objetivo é suavizar a imagem, reduzindo pequenas variações locais. A opção `replicate` replica os pixels mais próximos quando o kernel ultrapassa os limites da imagem.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation mean_filter --kernel-size 3 --border replicate
```

### Média ponderada

Aplica um filtro de suavização em que os pixels da vizinhança possuem pesos diferentes. Isso permite suavizar a imagem dando maior importância a determinadas posições do kernel.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation weighted_mean --border replicate
```

### Convolução com kernel identidade

Executa a convolução utilizando o kernel identidade `3 x 3`. Como esse kernel preserva o valor do pixel central, o resultado esperado é uma imagem igual ou muito próxima da original.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation convolution --kernel kernels/identity_3x3.txt --border replicate
```

### Laplaciano

Aplica o operador Laplaciano, utilizado para destacar regiões onde existem mudanças rápidas de intensidade, como contornos e detalhes da imagem.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation laplacian --border replicate
```

### Sobel

Aplica o operador Sobel para detectar bordas. São calculadas as variações nas direções horizontal e vertical, permitindo destacar diferentes orientações de contornos presentes na imagem.

```powershell
python -m pdi_lab --input images/input/romero_brito.jpg --operation sobel --border replicate
```
