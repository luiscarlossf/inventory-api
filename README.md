# Inventory API
![Django CI](https://github.com/luiscarlossf/inventory-api/workflows/Django%20CI/badge.svg)

O back-end do sistema de levantamento dos equipamentos do MPF/PI.

## Getting Started

Essas instruções fornecerão uma cópia do projeto e execução na sua máquina local para fins de desenvolvimento e teste. Consulte [deployment](https://github.com/luiscarlossf/inventory-api/wiki/_new#deployment) para obter notas sobre como colocar o projeto em produção.

### Pré-requisitos

Usamos o pacote [Django Auth LDAP](https://django-auth-ldap.readthedocs.io/en/latest/index.html) para fazer a autenticação LDAP, você precisará das bibliotecas e cabeçalhos do [OpenLDAP](https://www.openldap.org/) disponíveis no seu sistema. Para isso, siga as instruções a seguir:
1. Baixe e instale o Cyrus SASL
 * [Baixar Cyrus SASL](https://github.com/cyrusimap/cyrus-sasl/releases)
 * [Instruções de instalação do Cyrus SASL](https://www.cyrusimap.org/sasl/sasl/installation.html#tarball-installation). Recomendamos usar o método de instalação `Tarball installation`.
2. Baixe e instale o OpenSSL
 * [Baixar OpenSSL](https://www.openssl.org/source/)
 * [Instruções de instalação do OpenSSL] (https://github.com/openssl/openssl/blob/master/NOTES.UNIX)
3. Baixe e instale o OpenLDAP 
 * [Baixar OpenLDAP](https://www.openldap.org/software/download/)
 * [Instruções de instalação do OpenLDAP](https://www.openldap.org/software/release/install.html)

### Instalação

Um passo a passo mostrando como obter o ambiente de desenvolvimento em execução. Lembrando que é necessário que você esteja no diretório raiz do projeto antes de executar os comandos a seguir.

Instalando as dependências do projeto... 

```
$ pip3 install -r requirements.txt
```

Executando o projeto...

```
$ python3 manage.py runserver
```

## Execução de testes

Os testes automatizados são executados com a [framework de testes do Django](https://www.django-rest-framework.org/api-guide/testing/).

```
$ python3 manage.py test
```

## Deployment

Qualquer observação adicional sobre como fazer o deploy do sistema será adicionada nessa seção. 

## Construída com

* [Django REST](https://www.django-rest-framework.org/) - A framework para WEB API usada.
* [Django Authentication Using LDAP](https://django-auth-ldap.readthedocs.io/) - Serviço de autenticação LDAP

## Contribuição
Por favor, leia [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) para detalhes do nosso código de conduta, e o processo para submissão de pull requests para nós.

## Versionamento

Usamos o [URL Path](https://www.django-rest-framework.org/api-guide/versioning/#urlpathversioning) para versionamento. Para as versões disponíveis, veja as [tags nesse repositório](https://github.com/luiscarlossf/inventory-api/tags). 

## Autores

* **Luis Carlos** - *Projeto de estágio* - [luiscarlossf](https://github.com/luiscarlossf)

Veja a lista de [contribuidores](https://github.com/luiscarlossf/inventory-api/contributors) que participaram desse projeto.

## Licença

Esse projeto é licenciado sobre a GNU General Public License v3.0- veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.

## Agradecimentos




