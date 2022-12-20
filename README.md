# Trabalho 1 - Fundamentos de Sistemas Embarcados (FSE)

## Objetivo
O projeto desenvolvido tem como objetivo a criação de um sistema de automatização predial de forma distribuida, contendo as funcionalidades de monitoramento e acionamento de sensores e dispositivos de um prédio com múltiplas salas, além de outras. 
<br><br>
Link do enunciado original: https://gitlab.com/fse_fga/trabalhos-2022_2/trabalho-1-2022-2

## Dados

**Nome:** Guilherme Daniel Fernandes da Silva
<br>
**Matrícula:** 18/0018019

## Dependências
- g++ 8.3.0 ou superior
- Python 3.0 ou superior

## Como rodar
### Servidor Central
Após clonar o repositório, rodar o seguinte comando:
```
cd main
```
Dentro da pasta **main**, rodar o seguinte comando:
```
python3 app.py <ip_servidor_central> <porta_servidor_central>
```
Obs: o IP e porta do servidor central devem ser passados como parâmetro.
### Servidor Distribuído
Após clonar o repositório, rodar o seguinte comando:
```
cd node
```
Dentro da pasta **node**, rodar o seguinte comando:
```
make all
```
O binário compilado será armazenado na pasta **bin**. Dessa forma, para rodá-lo, é necessário rodar o seguinte comando: 
```
./bin <arquivo_de_configuracao_da_sala>.json
``` 
Obs: o arquivo de configuração da sala deve ser editado de forma a indicar qual é o endereço do servidor central, alterando os valores dos atributos `"ip_servidor_central"` e `"porta_servidor_central"` para os endereços do servidor central correspondentes.