#!/usr/bin/env python3
#
# Copyright (c) 2019 Murilo Ijanc' <mbsd@m0x.ru>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import os
import re
import sys
import time

import requests

# Base para construção das URLS
BASE_URL_ICROP = "https://icrop.online%s"
BASE_URL_GOOGLE = "https://www.googleapis.com%s"

# Token do formulário de autenticaçãod o icrop
FORM_TOKEN = ":FIRE:TOKEN:%s"

# Chave da aplicação
KEY="AIzaSyD0dcdKuQFfyYnFuwsPjaCkArPEGxfEyOg"

# Outras opções
DEFAULT_SLEEP = 1.5
RE_EMAIL = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
TIMEOUT=15
VERSION="0.0.1"

# Variáveis de ambiente
EMAIL = os.getenv("EMAIL", "")
PASSWD = os.getenv("PASSWD", "")
CODEST = os.getenv("CODEST", "")

# Ativando sessões do request
REQ = requests.Session()

def auth_email(email):
	"""Autenticação do email.

	Primeira parte do processo de autenticação, necessita enviar o email pare
	receber a o token."""

	# informacoes do para o request
	path = "/identitytoolkit/v3/relyingparty/createAuthUri?key=" + KEY
	url = BASE_URL_GOOGLE % path
	headers = {
		"Host": "www.googleapis.com",
		"User-Agent": "Mozilla/5.0 (X11; OpenBSD amd64; rv:74.0) Gecko/20100101 Firefox/74.0",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"X-Client-Version": "Firefox/JsCore/6.6.1/FirebaseUI-web",
		"X-Firebase-Locale": "pt-BR",
		"Origin": "https://icrop.online",
		"Connection": "keep-alive",
		"Referer": "https://icrop.online/icrop/admin_home.php"
	}

	# checamos se o email é valido
	if not re.search(RE_EMAIL, email):
		print("E-mail: %s parece ser inválido." % email)
		return False

	# dados a serem enviados para o google
	data = {
		"identifier": email,
		"continueUri": "https://icrop.online/icrop/admin_home.php"
	}

	print("Requisitando [%s]" % url);

	res = REQ.post(url, json=data, timeout=TIMEOUT)

	print(res.status_code) # 200
	print(res.json())

	""" Exemplo resposta:

	{'kind': '', 'allProviders': [], 'registered': True, 'sessionId': '',
	'signinMethods': []}
	"""

	return True


def auth_password(email, password):
	"""Autenticação senha.

	Segunda etapa de autenticação uma vez que a resposta tenha sido válida
	na primeira etapa precisamos passar o email a senha e outros dados para
	finalizar a autenticacao e retornar o token final.
	"""

	path = "/identitytoolkit/v3/relyingparty/verifyPassword?key=" + KEY
	url = BASE_URL_GOOGLE % path
	headers = {
		"Host": "www.googleapis.com",
		"User-Agent": "Mozilla/5.0 (X11; OpenBSD amd64; rv:74.0) Gecko/20100101 Firefox/74.0",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"X-Client-Version": "Firefox/JsCore/6.6.1/FirebaseUI-web",
		"X-Firebase-Locale": "pt-BR",
		"Origin": "https://icrop.online",
		"Connection": "keep-alive",
		"Referer": "https://icrop.online/icrop/admin_home.php",
		"TE": "Trailers",
	}

	# checamos se o email é valido
	if not re.search(RE_EMAIL, email):
		print("E-mail: %s parece ser inválido." % email)
		return False

	# TODO: isso pode melhorar, menor que?
	if len(password) == 0:
		print("Senha deve ser maior que 0")
		return False

	# dados a serem enviados para o google
	data = {
		"email": email,
		"password": password,
		"returnSecureToken": True
	}

	print("Requisitando [%s]" % url);

	res = REQ.post(url, json=data, timeout=TIMEOUT)

	print(res.status_code) # 200
	print(res.json())

	# TODO: checar se existe essa chave
	return res.json()['idToken']

def auth_icrop(email, token):
	"""Autenticação token.

	Terceira etapa da autenticação, depois de finalizado a autenticação do
	google é necessário enviar o token para validar junto ao serviço da Icrop e
	consequentemente gerar uma sessão válida.
	"""

	path = "/icrop/admin_home.php"
	url = BASE_URL_ICROP % path
	headers = {
		"Host": "icrop.online",
		"Origin": "https://icrop.online",
		"Referer": "https://icrop.online/icrop/admin_home.php",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br",
		"Connection": "keep-alive",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (X11; OpenBSD amd64; rv:74.0) Gecko/20100101 Firefox/74.0"
	}

	# checamos se o email é valido
	if not re.search(RE_EMAIL, email):
		print("E-mail: %s parece ser inválido." % email)
		return False

	# TODO: isso pode melhorar, menor que?
	if len(token) == 0:
		print("Token deve ser maior que 0")
		return False

	# dados a serem enviados para o google
	data = {
		"formlogin": email,
		"formsenha": FORM_TOKEN % token,
	}

	REQ.get(url) # isso só serve para criarmos a sessão
	time.sleep(DEFAULT_SLEEP)

	print("Requisitando [%s] - [%s]" % (url, token));

	res = REQ.post(url, data=data, timeout=TIMEOUT)

	print(res.status_code) # 200
	print(res.content)

	return True

def submit_form(codigo_estacao, periodo_ini, periodo_final, exibir_por,
				sensores=["92", "1", "2", "21", "3", "4"]):
	"""Submetemos o formulário do relatório.

	Algumas checagens são necessárias antes do envio do formulário, para
	obedecerem as regras de negócio.
	"""

	# itens abaixo são parametros a url
	item = "74" # tipo de relatório
	sid = "9569c6e5b97b" # identificacao

	path = "/icrop/admin_home.php?item={}&sid={}".format(item, sid)
	url = BASE_URL_ICROP % path

	# dados do formulario
	data = {
		"estacao": CODEST,
		"estacao2": CODEST,
		"estacao3": CODEST,
		"VIEW_periodo": "{}+-+{}".format(periodo_ini, periodo_final),
		"exibe_por": exibir_por,
		"grafico_del[]": sensores,
		"enviar2": "Filtrar",
		"enviar": "Filtrar"
	}

	print("Requisitando [%s]" % (url));

	res = REQ.post(url, data=data, timeout=TIMEOUT)

	print(res.status_code) # 200
	print(res.content)

def get_xlsx(codigo_estacao, dest):
	"""Get xlsx"""

	path = "/icrop/admsite-estacao_gera_xls_comp?lista={},{},{}".format(
		CODEST, CODEST, CODEST
	)
	url = BASE_URL_ICROP % path

	print("Requisitando [%s]" % (url));

	res = REQ.get(url, timeout=TIMEOUT, stream=True)
	print(res.status_code) #302 -> 200

	# checamos o cabecalho se foi tudo0 ok
	if res.headers["Content-Type"] == "application/force-download":
		print("Salvando: %s" % dest)
		with open(dest, "wb") as f:
			for chunk in res:
				f.write(chunk)
	else:
		print("Não existe arquivo para download, headers: %s" % str(
			res.headers))
		return False
	return True


def banner():
	"""Banner function"""

	print("\n")
	print("=" * 80)
	print("\t\t\t\tICROP - CSV")
	print("=" * 80)
	print("\n")


def main(email, password, codigo_estacao):
	"""Main function."""

	banner()

	# Primeira etapa autenticação
	auth_email(email)

	# simulo o usuário demorando para digitar
	time.sleep(DEFAULT_SLEEP + 3)
	# segunda etapa da autenticação
	token = auth_password(email, password)

	# terceira etapa da autenticação
	auth_icrop(email, token)

	# simulo o usuário demorando para digitar
	time.sleep(DEFAULT_SLEEP + 3)
	# segunda etapa da autenticação
	submit_form(codigo_estacao, "23/02/2020", "23/03/2020", "1")
	# download planilha
	get_xlsx(codigo_estacao, "./export.xlsx")


if __name__ == "__main__":
	main(EMAIL, PASSWD, CODEST)
