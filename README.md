# Watcher

## 1. Guia de Instalação

Existem duas opções para instalar e executar esta aplicação: configuração manual ou a construção de um contêiner Docker. Escolha a opção que melhor se adapta às suas necessidades e ambiente.

### Opção 1: Configuração Manual

1. Configure o ambiente virtual:
```bash
$ python3.10 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

2. Execute a aplicação:
```bash
$ python manage.py run
```

### Opção 2: Construção e Execução de uma Imagem Docker da Aplicação

1. Construa a imagem Docker:

```bash
$ docker build -t watcher .
```

2. Execute a aplicação
```bash
$ docker run watcher python manage.py run
```

## 2. Acessando o Shell no Contêiner

Ocasionalmente, pode ser necessário acessar o shell diretamente dentro do seu contêiner. Veja como você pode fazer isso:

### Bash
```bash
$ docker exec -it CONTAINER_ID sh
```

### Python shell
```bash
$ docker exec -it CONTAINER_ID python3 manage.py shell
```
