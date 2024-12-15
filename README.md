# Neoway Challenge - Diego Cardoso

Repositório que contém uma solução para o problema proposto [aqui](https://github.com/cardosodg/neoway-challenge-diego-cardoso/blob/main/neoway_software_engineering-teste_tecnico.pdf).

## Funcionalidades Principais

- **Validação de CPF e CNPJ**: Garantia de integridade dos dados antes de sua inserção no banco de dados.
- **Operações com MongoDB**: Inserções únicas e em lote, além de buscas dinâmicas.
- **Endereços REST**: Interação com o sistema via endpoints claros e bem definidos.
- **Monitoramento**: Informativo de status e uptime da aplicação.

## Tecnologias Utilizadas

- **Linguagem**: Python 3.x
- **Framework**: Flask
- **Banco de Dados**: MongoDB
- **Dependências**:
  - `pymongo`
  - `Flask`

---
## Endpoints Disponíveis

### 1. **POST /insert**

**Descrição:** Insere um documento único no banco de dados. E caso, o documento já esteja inserido, simplesmente notifica na resposta.

**Entrada:**
```json
{
  "cpf_cnpj": "cpf ou cnpj",
  "name": "nome ou razão social"
}
```
O endpoint traz respostas em caso de sucesso ou falha, formatada contendo os campos `success` e  `message`. O campo `success` é um booleano e `message` é uma string.

**Saída**
```json
{
    "success": "true ou false",
    "message": "mensagem de sucesso ou falha"
}
```

---

### 2. **POST /load-file**

**Descrição:** Recebe um arquivo CSV com vários registros e insere os dados válidos. Caso existam dados já inseridos no banco, eles serão ignorados e na resposta, a aplicação indicará quantos itens estavam duplicados.

**Entrada:** Arquivo CSV com os campos `DOCUMENTO` e `NOME/RAZAO_SOCIAL`.

A saída do endpoint `/load-file` é semelhante à de `/insert`.
**Saída**
```json
{
    "success": "true ou false",
    "message": "mensagem de sucesso ou falha"
}
```

---

### 3. **GET /search**

**Descrição:** Busca documentos com base em CPF/CNPJ ou nome/razão social. Se ambos os parâmetros forem passados, CPF/CNPJ terá precedência.

**Parâmetros:**
- `cpf_cnpj`: Busca baseado em CPF/CNPJ
- `name`: Busca baseado em nome/razão social

**Saída**
São 2 possíveis tipos de saída, podendo ser um único item, neste caso sendo um JSON, ou uma lista de JSONs, para o caso de múltiplos resultados. Ambos os resultados estarão dentro da chave `data`.

```json
{
    "success": "true ou false",
    "message": "mensagem de sucesso ou falha",
    "data": {...}
}
```
ou
```json
{
    "success": "true ou false",
    "message": "mensagem de sucesso ou falha",
    "data": [...]
}
```

---

### 4. **GET /status**

**Descrição:** Fornece o estado atual da aplicação. Traz um contador para cada endpoint, a soma total de chamadas de todos os endpoints, quanto tempo a aplicação está _up_ e a data e hora. Os dados ficam dentro da chave `data`

**Resposta:**
```json
{
  "success": true,
  "message": "Data successfully acquired.",
  "data": {
    "insert_single": 10,
    "insert_many": 5,
    "find_doc": 8,
    "status": 2,
    "total": 25,
    "uptime": "0:01:23",
    "timestamp": "2024-12-15T15:40:00Z"
  }
}
```

---

## Execução

É necessário ter o Docker e o Docker Compose instalados. Dentro da raiz do projeto, há um arquivo docker-compose.yaml, que é utilizado para configurar e orquestrar a aplicação. Para iniciar a aplicação e acompanhar os logs, basta executar os seguintes comandos:
```bash
docker compose up app -d
docker logs -f --tail 10 app
```

No diretório `test`, existe um script shell que permite executar testes simples.

```bash
cd tests/
```

Modifique o script `run_tests.sh`, na linha 3 troque a variável `host` para o IP do servidor/máquina que está rodando a aplicação. Aqui representado por 1.2.3.4:
```bash
#host="localhost"
host="1.2.3.4"
```

Para ativá-lo, precisa construir um container e executá-lo:
```bash
cd tests/
docker build --rm -t app_tests .
docker run -it --rm app_tests
```

Caso tenha dificuldades de executar os testes, o script possui algumas chamadas com o comando `curl`. Basta copiar os comandos e executar a partir de um terminal. Lembre-se de trocar `$host` pelo ip da máquina/servidor que está executando a aplicação.
