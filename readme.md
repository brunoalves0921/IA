# Instruções para Executar o Programa de Simulação Genética

Este é um programa em Python que realiza uma simulação genética para resolver o problema de alocação de enfermeiras em turnos. A simulação envolve a evolução de uma população de soluções candidatas ao longo de várias gerações.

## Requisitos

- Python (Versão 3.x)
- matplotlib (Versão 3.8.2)
- Pandas (Versão 2.1.3)

## Como Executar o Programa

1. **Baixe o Código-fonte:**
   - Clone o repositório ou baixe o arquivo `.py` para o seu computador.

2. **Execute o Programa:**
   - Abra um terminal ou prompt de comando.
   - Navegue até o diretório onde o arquivo `.py` está localizado.
   - Execute o programa com o comando: `python trabalho03.py`

3. **Interaja com o Programa:**
   - O programa exibirá um menu interativo com as seguintes opções:
     1. **Treinar com os parâmetros padrão:** Executa a simulação com parâmetros fornecidos via terminal.
     2. **Bloco 1 (Taxa de Elitismo):** Realiza experimentos variando a taxa de elitismo e gera resultados em um arquivo CSV.
     3. **Bloco 2 (Tamanho da População):** Realiza experimentos variando o tamanho da população e gera resultados em um arquivo CSV.
     4. **Sair:** Encerra o programa.

4. **Modificar Parâmetros da Simulação:**
   - Ao selecionar a opção 1, você pode inserir manualmente os parâmetros da simulação, como número de enfermeiras, turnos, tamanho da população, número de iterações, taxa de mutação e taxa de elitismo.

5. **Visualizar Resultados Bloco 1 e Bloco 2:**
   - Após a execução, o programa gerará arquivos CSV (`bloco_1.csv` e `bloco_2.csv`) com os resultados da simulação.
   - Você pode executar o notebook "graficos.ipynb" para visualizar os resultados plotados em gráficos

6. **Modificar Experimentos (Opcional):**
   - Se desejar realizar experimentos adicionais, ajuste os parâmetros diretamente no código-fonte (funções `bloco_1()` e `bloco_2()`).

## Arquivos Gerados

- **bloco_1.csv:** Contém os resultados dos experimentos variando a taxa de elitismo.
- **bloco_2.csv:** Contém os resultados dos experimentos variando o tamanho da população.

## Notas Adicionais

- O programa usa uma semente (`seed`) para garantir reprodutibilidade nos experimentos. Caso deseje resultados diferentes, altere a semente no código.

- Os resultados detalhados e melhores indivíduos são salvos em arquivos JSON (`bloco_1.json` e `bloco_2.json`).
