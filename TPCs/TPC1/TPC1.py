# TPC1 SPLN


import re
import json

# ler ficheiro
with open("medicina.xml", "r", encoding="utf-8") as f:
    texto = f.read()

# marcar os conceitos
texto = re.sub(r"<b>\s*(\d+) ", r"<b>@@\1 ", texto)

# separar conceitos
conceitos = re.split(r"<b>\s*@", texto)


def processar_conceito(c):

    # extrair id
    id = re.search(r"^@(\d+)", c)

    # marcar campos
    c = re.sub(r"SIN\.-", r"@SIN.-", c)
    c = re.sub(r"VAR\.-", r"@VAR.-", c)
    c = re.sub(r"Nota\.-", r"@Nota.-", c)

    # procurar campos
    sin = re.search(r"@SIN\.-([^@<]+)", c)
    var = re.search(r"@VAR\.-([^@<]+)", c)
    nota = re.search(r"@Nota\.-([^@<]+)", c)

    # encontrar blocos de línguas
    blocos = re.findall(
        r'>\s*(en|pt|es|la)\s*</text>\n(.*?)(?=>\s*(en|pt|es|la)\s*</text>|<b>)',
        c,
        re.DOTALL
    )

    ling = [
        (lang, ' '.join(t.strip() for t in re.findall(r'<i>([^<]+)', bloco)).strip())
        for lang, bloco, _ in blocos
    ]

    trGal = re.search(r"^@\d+([\w ]+)</b>", c)
    dom = re.search(r"font=\"6\"><i>(.*)</i>", c)

    res = {}

    if not id:
        return {}, None

    if nota:
        res["nota"] = nota.group(1)

    if var:
        res["var"] = var.group(1)

    if sin:
        res["sin"] = sin.group(1)

    if trGal:
        res["galego"] = trGal.group(1)

    if dom:
        res["dom"] = dom.group(1)

    for l, t in ling:
        res[l] = t

    return res, id.group(1)


entries = {}

for c in conceitos[1:]:
    res, id = processar_conceito(c)
    if id:
        entries[id] = res


# guardar em json
with open("dicionario_medicina.json", "w", encoding="utf-8") as f_out:
    json.dump(entries, f_out, indent=4, ensure_ascii=False)
