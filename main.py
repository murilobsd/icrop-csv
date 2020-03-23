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

import requests

# Base para construção das URLS
BASE_URL_ICROP = "https://icrop.online%s"
BASE_URL_GOOGLE = "https://www.googleapis.com%s"

# Chave da aplicação
KEY="AIzaSyD0dcdKuQFfyYnFuwsPjaCkArPEGxfEyOg"

# Outras opcoes
RE_EMAIL = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
TIMEOUT=5
VERSION="0.0.1"

# Variáveis de ambiente
EMAIL = os.getenv("EMAIL", "")

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

	res = requests.post(url, json=data, timeout=TIMEOUT)

	print(res.status_code)
	print(res.json())

	return True

def main(email):
	"""Main function."""
	print("Ola")
	auth_email(email)

if __name__ == "__main__":
	main(EMAIL)
