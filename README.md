# ICROP CSV

Simples script para automatizar o processo de coleta de dados dos relatórios
gerados pela [Icrop][1]

## TODO

- [x] autenticar
- [x] Acessar relatório
- [x] Submeter o formulário para filtrar o relatório desejado
<<<<<<< HEAD
- [ ] Exportar para CSV
- [ ] Salvar arquivo csv
=======
- [x] Exportar para CSV
- [x] Salvar arquivo csv
>>>>>>> submit_form

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
- **PASSWD**: senha do usuário
<<<<<<< HEAD
=======
- **CODEST**: código da estação
>>>>>>> submit_form

Exemplo somente autenticação:

```bash
EMAIL="login_do_usuario" PASSWD="senha" ./main.py
```

<<<<<<< HEAD
=======
Exemplo baixando os dados:

```bash
EMAIL="login_do_usuario" PASSWD="senha" CODEST=codigo_da_estacao ./main.py
```

>>>>>>> submit_form
[1]: https://icrop.online/
