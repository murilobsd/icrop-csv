# ICROP CSV

Simples script para automatizar o processo de coleta de dados dos relatórios
gerados pela [Icrop][1]

## TODO

- [ ] autenticar
- [ ] Acessar relatório
- [ ] Submeter o formulário para filtrar o relatório desejado
- [ ] Exportar para CSV
- [ ] Salvar arquivo csv

## Instalação

Caso esteja em um ambiente linux, segue os comandos abaixo para instalar as
dependências do projeto.

```bash
git clone https://github.com/murilobsd/icrop-csv
cd icrop-csv
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## Uso

Para passar os dados **confidenciais** do usuário utilizamos variáveis de
ambiente, abaixo exibimos a lista das possíveis variáveis de ambiente:

- **EMAIL**: login do usuário

Exemplo:

```bash
EMAIL=login_do_usuario ./main.py
```

[1]: https://icrop.online/
