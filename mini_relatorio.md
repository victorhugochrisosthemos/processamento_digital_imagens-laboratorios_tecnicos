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

As operações da M1.1 foram feitas com percurso explícito dos pixels, conforme solicitado no enunciado. 

### M1.2

Foram implementadas:

- ajuste de brilho;
- ajuste de contraste;
- negativo;
- limiarização binária;
- cálculo manual do histograma.

O histograma utiliza uma estrutura com 256 posições para contabilizar a quantidade de pixels de cada intensidade. 

### M1.3

Foram implementadas:

- convolução genérica;
- tratamento de bordas por cópia e replicação;
- filtro de média;
- média ponderada;
- Laplaciano;
- Sobel nas direções X e Y;
- cálculo das magnitudes do gradiente.

A convolução e o acesso às vizinhanças também foram implementados manualmente. 

---

## 4. Decisões de implementação

O projeto foi desenvolvido em Python e dividido principalmente entre `main.py` e `functions.py`.

O arquivo `main.py` é responsável por receber os parâmetros da linha de comando, carregar as imagens e selecionar a operação solicitada. O arquivo `functions.py` contém a implementação dos algoritmos.

Foram utilizadas bibliotecas apenas como apoio para leitura, escrita e armazenamento das imagens. As operações avaliadas foram realizadas percorrendo manualmente os pixels ou suas vizinhanças.

Durante os cálculos foram utilizados tipos numéricos adequados para evitar overflow. A conversão para o intervalo de 0 a 255 é realizada somente quando necessária para produzir a imagem final.

Na convolução foram consideradas duas estratégias de borda: `copy`, que mantém o valor original quando a vizinhança não cabe completamente, e `replicate`, que utiliza o pixel válido mais próximo.

Esses cuidados são importantes principalmente para contraste, convolução, Laplaciano e Sobel. 

---

## 5. Testes realizados

Foram realizados testes automatizados com `pytest` e testes manuais utilizando imagens reais e sintéticas.

A execução dos testes automatizados apresentou:

```text
7 passed
```

## 6. Resultados

Sobre os resultados obtidos, na M1.1 foi possível verificar que a cópia manual da imagem manteve os mesmos valores dos pixels da imagem original. Também foi possível visualizar separadamente os canais azul, verde e vermelho, além de comparar as duas formas de transformação para tons de cinza. Na quantização, conforme a quantidade de níveis foi reduzida, ficou mais evidente a perda de detalhes e principalmente as transições entre tons.

Na M1.2, os resultados também ficaram de acordo com o esperado. O aumento de brilho deixou a imagem mais clara e a redução de brilho deixou mais escura. No contraste, foi possível perceber uma diferença maior entre regiões claras e escuras quando o valor de alpha foi aumentado. Na limiarização, a imagem passou a ter basicamente duas intensidades, preto e branco, e o histograma ajudou a visualizar a quantidade de pixels presentes em cada nível de intensidade.

Já na M1.3, os filtros utilizando kernels apresentaram resultados diferentes dependendo do tipo de operação. O filtro de média suavizou a imagem, porém também retirou alguns detalhes. No Laplaciano foi possível perceber principalmente os contornos e regiões de mudança de intensidade. Com o Sobel, as bordas ficaram evidentes nas direções horizontal e vertical.

## 7. Análise técnica

Na minha opinião, uma das principais diferenças percebidas na M1.1 está relacionada à resolução espacial e radiométrica. A resolução espacial está mais relacionada à quantidade de pixels presentes na imagem, enquanto a radiométrica está relacionada à quantidade de valores que podem representar a intensidade desses pixels. Isso ficou mais evidente durante a quantização, pois reduzir a quantidade de níveis fez com que algumas variações de tonalidade deixassem de existir.

Além disso, a média simples e a média ponderada apresentaram resultados diferentes porque, na média simples, os três canais RGB participam igualmente do cálculo. Já na média ponderada, os canais possuem pesos diferentes.

Na M1.2, pude perceber que brilho e contraste alteram a imagem de maneiras diferentes. O brilho faz uma soma ou subtração sobre os valores de intensidade, enquanto o contraste trabalha aumentando ou diminuindo a diferença desses valores. Nesse processo também foi necessário cuidar da saturação, pois os resultados não podem ficar abaixo de 0 ou acima de 255.

Sobre a M1.3, considero que foi a parte mais trabalhosa, principalmente por envolver acesso à vizinhança dos pixels. Diferente das operações anteriores, não é suficiente acessar somente o pixel atual, sendo necessário também verificar os pixels próximos. Outro ponto importante foi o tratamento das bordas, já que em alguns casos o kernel tenta acessar posições que não existem na matriz da imagem.

## 8. Limitações

Sobre as limitações, acredito que a principal está relacionada ao desempenho das implementações manuais. Como as imagens são percorridas utilizando laços de repetição e várias operações são realizadas pixel por pixel, o tempo de processamento tende a aumentar conforme o tamanho da imagem.

Esse problema fica ainda mais evidente nas operações de convolução, pois além de percorrer toda a imagem também é necessário percorrer o kernel para cada posição. Contudo, para os objetivos do laboratório, essa implementação manual foi importante para entender melhor como as operações funcionam.

## 9. Declaração de uso de Inteligência Artificial

Durante o desenvolvimento dos laboratórios utilizei IA Generativa como ferramenta de apoio. O uso aconteceu principalmente para tirar dúvidas relacionadas à organização do código, interpretação de alguns requisitos, elaboração de testes e revisão da documentação.

Não obstante, procurei utilizar a ferramenta com cautela, verificando as respostas e comparando os resultados gerados pelo programa com o que era solicitado nos arquivos .md disponibilizados pelo professor. Também foram realizadas alterações no código durante o desenvolvimento conforme fui entendendo melhor as tarefas.

Além da IA Generativa, também utilizei como apoio conversas com colegas e questionamentos realizados durante as aulas. Dessa forma, a ferramenta não foi utilizada como única fonte para resolução das atividades.

10. Referências utilizadas

Para o desenvolvimento dos laboratórios foram utilizados principalmente os materiais fornecidos pelo professor na disciplina de Processamento Digital de Imagens, sendo eles:

enunciado do Laboratório M1.1;
enunciado do Laboratório M1.2;
enunciado do Laboratório M1.3;
contrato técnico dos Laboratórios da M1;
rubrica geral de avaliação dos Laboratórios da M1;
materiais e explicações apresentados durante as aulas;
documentação das bibliotecas utilizadas no projeto.

Também foram utilizadas discussões com colegas e IA Generativa como apoio durante o desenvolvimento e entendimento de alguns pontos das atividades.
