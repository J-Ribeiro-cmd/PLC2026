import re
import sys


def imagem(linha):
    return re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1"/>', linha)


def link(linha):
    return re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', linha)


def bold(linha):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', linha)


def italico(linha):
    return re.sub(r'\*(.+?)\*', r'<i>\1</i>', linha)


def formata(linha):
    """Aplica as quatro conversões de dentro da linha, pela ordem certa."""
    linha = imagem(linha)      # tem de ser antes do link
    linha = link(linha)
    linha = bold(linha)        # tem de ser antes do itálico
    linha = italico(linha)
    return linha


def cabecalho(linha):
    m = re.match(r'(#{1,3}) (.+)', linha)
    if m:
        nivel = len(m.group(1))
        texto = m.group(2)
        return f'<h{nivel}>{texto}</h{nivel}>'
    return linha


def lista(texto):
    resultado = []
    dentro_de_lista = False

    for linha in texto.split('\n'):
        m = re.match(r'\d+\. (.+)', linha)
        if m:
            if not dentro_de_lista:
                resultado.append('<ol>')
                dentro_de_lista = True
            resultado.append(f'<li>{m.group(1)}</li>')
        else:
            if dentro_de_lista:
                resultado.append('</ol>')
                dentro_de_lista = False
            resultado.append(linha)

    # O texto pode acabar a meio de uma lista
    if dentro_de_lista:
        resultado.append('</ol>')

    return '\n'.join(resultado)


def converte(texto):
    linhas = []
    for linha in texto.splitlines():
        linhas.append(cabecalho(formata(linha)))

    # As listas ocupam várias linhas, por isso são tratadas no fim
    return lista('\n'.join(linhas))


if len(sys.argv) > 1:
    # Foi dado o nome de um ficheiro: lê o texto de lá
    with open(sys.argv[1], encoding='utf-8') as ficheiro:
        texto = ficheiro.read()
else:
    # Não foi dado ficheiro: lê o que for escrito no teclado
    texto = sys.stdin.read()

print(converte(texto))
