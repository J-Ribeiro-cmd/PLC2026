import sys
import re

# Tokens a reconhecer: COMENTARIO, VAR, LANG, STRING, LIMIT, NUM, ID,
#                      DELIM, SKIP, NEWLINE, ERRO

def tokenize(input_string):
    reconhecidos = []
    linha = 1
    mo = re.finditer(r'(?P<COMENTARIO>\#.*)'
                     r'|(?P<VAR>\?\w+)'
                     r'|(?P<LANG>@[a-zA-Z]{2})'
                     r'|(?P<STRING>"[^"]*")'
                     r'|(?P<LIMIT>\bLIMIT\b)'
                     r'|(?P<NUM>\d+)'
                     r'|(?P<ID>\w+(?::\w+)?)'
                     r'|(?P<DELIM>[{}.])'
                     r'|(?P<SKIP>[ \t])'
                     r'|(?P<NEWLINE>\n)'
                     r'|(?P<ERRO>.)', input_string)
    for m in mo:
        dic = m.groupdict()
        if dic['COMENTARIO']:
            t = ("COMENTARIO", dic['COMENTARIO'], linha, m.span())

        elif dic['VAR']:
            t = ("VAR", dic['VAR'], linha, m.span())

        elif dic['LANG']:
            t = ("LANG", dic['LANG'], linha, m.span())

        elif dic['STRING']:
            t = ("STRING", dic['STRING'], linha, m.span())

        elif dic['LIMIT']:
            t = ("LIMIT", dic['LIMIT'], linha, m.span())

        elif dic['NUM']:
            t = ("NUM", dic['NUM'], linha, m.span())

        elif dic['ID']:
            t = ("ID", dic['ID'], linha, m.span())

        elif dic['DELIM']:
            t = ("DELIM", dic['DELIM'], linha, m.span())

        elif dic['SKIP']:
            t = ("SKIP", dic['SKIP'], linha, m.span())

        elif dic['NEWLINE']:
            t = ("NEWLINE", dic['NEWLINE'], linha, m.span())
            linha += 1

        elif dic['ERRO']:
            t = ("ERRO", dic['ERRO'], linha, m.span())

        else:
            t = ("UNKNOWN", m.group(), linha, m.span())
        if t[0] not in ('SKIP', 'COMENTARIO', 'UNKNOWN'): reconhecidos.append(t)
    return reconhecidos

# Lê o input todo de uma vez para a contagem de linhas funcionar
texto = sys.stdin.read()
for tok in tokenize(texto):
    print(tok)