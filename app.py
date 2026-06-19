import os
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# =========================================================
# Utilizadores
# As passwords só existem no servidor e nunca chegam ao browser.
# Por defeito usa estas; em produção podes defini-las como
# variáveis de ambiente no Render (PW_ADMIN, PW_SARA).
# =========================================================
UTILIZADORES = {
    "admin": generate_password_hash(os.environ.get("PW_ADMIN", "1234")),
    "sara":  generate_password_hash(os.environ.get("PW_SARA", "abcd")),
}


# =========================================================
# Conversor de Temperatura
# =========================================================
def cf(c): return c * 9 / 5 + 32
def fc(f): return (f - 32) * 5 / 9
def ck(c): return c + 273.15
def kc(k): return k - 273.15
def fk(f): return ck(fc(f))
def kf(k): return cf(kc(k))

CONVERSOES = {
    "cf": (cf, "°C", "°F"),
    "fc": (fc, "°F", "°C"),
    "ck": (ck, "°C", "K"),
    "kc": (kc, "K",  "°C"),
    "fk": (fk, "°F", "K"),
    "kf": (kf, "K",  "°F"),
}


@app.route("/", methods=["GET", "POST"])
def index():
    ctx = {
        "msg1": "", "classe1": "", "user1": "",
        "msg2": "", "classe2": "", "user2": "",
        "res_conv": "", "classe_conv": "", "tipo_conv": "cf", "valor_conv": "",
    }

    if request.method == "POST":
        acao = request.form.get("acao")

        # ---- Exercício 1: login com 1 utilizador (admin) ----
        if acao == "login1":
            user = request.form.get("user1", "")
            pwd = request.form.get("pass1", "")
            ctx["user1"] = user
            if user != "admin":
                ctx["msg1"], ctx["classe1"] = "Erro: utilizador não encontrado.", "msg erro"
            elif not check_password_hash(UTILIZADORES["admin"], pwd):
                ctx["msg1"], ctx["classe1"] = "Erro: password incorreta.", "msg erro"
            else:
                ctx["msg1"], ctx["classe1"] = "Login efetuado com sucesso!", "msg ok"

        # ---- Exercício 2: login com 2 utilizadores ----
        elif acao == "login2":
            user = request.form.get("user2", "")
            pwd = request.form.get("pass2", "")
            ctx["user2"] = user
            if user not in UTILIZADORES:
                ctx["msg2"], ctx["classe2"] = "Erro: utilizador não encontrado.", "msg erro"
            elif not check_password_hash(UTILIZADORES[user], pwd):
                ctx["msg2"], ctx["classe2"] = "Erro: password incorreta.", "msg erro"
            else:
                ctx["msg2"], ctx["classe2"] = f"Login efetuado com sucesso! Bem-vindo(a), {user}.", "msg ok"

        # ---- Conversor de temperatura ----
        elif acao == "converter":
            tipo = request.form.get("tipo_conv", "cf")
            valor_txt = request.form.get("valor_conv", "")
            ctx["tipo_conv"] = tipo
            ctx["valor_conv"] = valor_txt
            try:
                valor = float(valor_txt)
                func, origem, destino = CONVERSOES[tipo]
                ctx["res_conv"] = f"{valor:g} {origem} = {func(valor):.2f} {destino}"
                ctx["classe_conv"] = "res"
            except (ValueError, KeyError):
                ctx["res_conv"] = "Introduz um número válido (ex.: 25 ou 25.5)."
                ctx["classe_conv"] = "res erro"

    return render_template("index.html", **ctx)


if __name__ == "__main__":
    app.run(debug=True)
