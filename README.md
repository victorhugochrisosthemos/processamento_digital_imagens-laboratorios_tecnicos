# Laboratorios M1.1, M1.2 e M1.3 - Processamento de Imagens

Projeto em Python reunindo as atividades dos tres laboratorios da M1
<br>

## Organizacao do codigo
<br>
A logica principal esta em:

```text
src/pdi_lab/principal.py
src/pdi_lab/funcoes.py
```
<br><br>

## Dependencias

```powershell
python -m pip install -r requirements.txt
```

Nao e necessario criar ambiente virtual para executar o projeto

<br>

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

Exemplo com uma imagem colocada em `images/input/romero_brito.jpg`:

```powershell
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao inspecionar
```

Sem `--saida`, o programa cria automaticamente `imagens_geradas` no diretorio atual.



### M1.1

```powershell
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao copiar
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao canal_azul
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao canal_verde
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao canal_vermelho
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao cinza_media
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao cinza_ponderado
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao quantizar --niveis 8
```

### M1.2

```powershell
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao brilho --valor 40
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao contraste --alpha 1.5
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao negativo
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao limiarizar --limiar 128
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao histograma
```

### M1.3

```powershell
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao filtro_media --tamanho-nucleo 3 --borda replicar
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao media_ponderada --borda replicar
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao convolucao --nucleo kernels/identidade_3x3.txt --borda replicar
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao laplaciano --borda replicar
python -m pdi_lab --entrada images/input/romero_brito.jpg --operacao sobel --borda replicar
```

## Nomes principais das operacoes

```text
inspecionar
copiar
canal_azul
canal_verde
canal_vermelho
cinza_media
cinza_ponderado
quantizar
brilho
contraste
negativo
limiarizar
histograma
convolucao
filtro_media
media_ponderada
laplaciano
sobel
```

## Compatibilidade

Por exigencia do contrato tecnico, tambem sao aceitos `--input`, `--output`, `--operation`, `--levels`, `--value`, `--threshold`, `--kernel`, `--border` e os nomes oficiais das operacoes em ingles. A implementacao interna, entretanto, usa os nomes em portugues.
