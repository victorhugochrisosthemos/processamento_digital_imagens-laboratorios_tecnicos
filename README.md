# Laboratorios M1.1, M1.2 e M1.3 - Processamento de Imagens

Projeto em Python reunindo as atividades dos tres laboratorios da M1
<br>


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
