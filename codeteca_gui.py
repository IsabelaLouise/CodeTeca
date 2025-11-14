import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, date, timedelta

# ================== CONFIGURAÇÃO DO BANCO ==================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Ilcs050607",  # altere aqui se necessário
    "database": "CodeTeca"
}

def conectar():
    return mysql.connector.connect(**DB_CONFIG)

def para_br(data):
    """Recebe date/datetime/str(None) e retorna '' ou 'DD/MM/AAAA'."""
    if not data:
        return ""
    # se já for date/datetime
    if isinstance(data, (date, datetime)):
        return data.strftime("%d/%m/%Y")
    # tenta tratar string no formato YYYY-MM-DD
    s = str(data).strip()
    try:
        if len(s) == 10 and s[4] == '-' and s[7] == '-':
            return datetime.strptime(s, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        pass
    # fallback: devolve string original
    return s

def formatar_linhas(dados):
    """
    Recebe lista de tuplas (linhas do cursor) e retorna lista de listas
    com datas convertidas para DD/MM/AAAA quando possível.
    """
    linhas = []
    for linha in dados:
        nova = []
        for valor in linha:
            # tenta formatar todo valor que seja date/datetime ou string YYYY-MM-DD
            nova.append(para_br(valor) if (isinstance(valor, (date, datetime)) or (isinstance(valor, str) and "-" in valor and len(valor) == 10)) else valor)
        linhas.append(nova)
    return linhas


# ================== FUNÇÕES DE LISTAGEM (já existentes) ==================
def listar_usuarios():
    con = None
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT ID_usuario, Nome, Email, DtNasc, Logradouro, Numero, Complemento, CEP
            FROM Usuario
            ORDER BY Nome
        """)
        dados = cur.fetchall()

        # Formatação simples com a função auxiliar
        dados_formatados = [
            [
                linha[0],              # ID
                linha[1],              # Nome
                linha[2],              # Email
                para_br(linha[3]),     # DtNasc formatada
                linha[4],              # Logradouro
                linha[5],              # Numero
                linha[6],              # Complemento
                linha[7]               # CEP
            ]
            for linha in dados
        ]

        atualizar_tabela(
            ["ID", "Nome", "Email", "Data de Nascimento", "Logradouro", "Número", "Complemento", "CEP"],
            dados_formatados
        )

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar usuários:\n{e}")

    finally:
        if con:
            con.close()


def listar_livros():
    con = None
    try:
        con = conectar()
        cur = con.cursor()

        # Query que busca livros com os autores concatenados
        cur.execute("""
            SELECT 
                L.ID_livro,
                L.Titulo,
                L.Ano,
                GROUP_CONCAT(A.NomeAutor SEPARATOR ', ') AS Autores
            FROM Livro L
            LEFT JOIN Livro_Autor LA ON L.ID_livro = LA.ID_livro
            LEFT JOIN Autor A ON LA.ID_autor = A.ID_autor
            GROUP BY L.ID_livro, L.Titulo, L.Ano
            ORDER BY L.Titulo
        """)
        dados = cur.fetchall()

        dados_formatados = formatar_linhas(dados)

        # Colunas agora incluem "Autores"
        atualizar_tabela(["ID", "Título", "Ano", "Autores"], dados_formatados)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar livros:\n{e}")
    finally:
        if con:
            con.close()

def listar_multas():
    con = None
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT 
                M.ID_multa, 
                U.Nome AS Usuario, 
                M.Motivo, 
                M.Data, 
                M.Validade
            FROM Multa M
            JOIN Emprestimo_Empresta E ON M.fk_Emprestimo_Empresta_ID_emprestimo = E.ID_emprestimo
            JOIN Usuario U ON E.fk_Usuario_ID_usuario = U.ID_usuario
            ORDER BY U.Nome
        """)
        dados = cur.fetchall()

        dados_formatados = formatar_linhas(dados)

        atualizar_tabela(["ID Multa", "Usuário", "Motivo", "Data", "Validade"], dados_formatados)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar multas:\n{e}")
    finally:
        if con:
            con.close()

def listar_emprestimos():
    con = None
    try:
        con = conectar()
        cur = con.cursor()

        cur.execute("""
            SELECT 
                E.ID_emprestimo,
                U.Nome AS Usuario,
                L.Titulo AS Livro,
                E.DtEmprestimo,
                E.DtDevolucaoPrevista,
                E.DtDevolucao,
                E.Status
            FROM Emprestimo_Empresta E
            JOIN Usuario U 
                ON E.fk_Usuario_ID_usuario = U.ID_usuario
            JOIN Copia C 
                ON E.fk_Copia_ID_copia = C.ID_copia
            JOIN Livro L 
                ON C.fk_Livro_ID_livro = L.ID_livro
            ORDER BY U.Nome
        """)

        dados = cur.fetchall()

        dados_formatados = formatar_linhas(dados)

        atualizar_tabela(
            ["ID", "Usuário", "Livro", "Data Empréstimo", "Prevista", "Devolução", "Status"],
            dados_formatados
        )

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar empréstimos:\n{e}")
    finally:
        if con:
            con.close()

# ================== FUNÇÕES CRUD USUÁRIO ==================

def abrir_janela_editar_usuario():
    selecionado = tabela.focus()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um usuário na tabela para editar.")
        return

    valores = tabela.item(selecionado, "values")
    if not valores:
        return

    id_usuario, nome, email, dtnasc, logradouro, numero, complemento, cep = valores

    win = tk.Toplevel(janela)
    win.title(f"Editar Usuário - ID {id_usuario}")
    win.geometry("600x350")
    win.configure(bg="#000")

    # NOME
    tk.Label(win, text="Nome:", bg="#000").grid(row=0, column=0, padx=10, pady=8, sticky="w")
    nome_e = tk.Entry(win, width=40)
    nome_e.insert(0, nome)
    nome_e.grid(row=0, column=1, padx=10, pady=8)

    # EMAIL
    tk.Label(win, text="E-mail:", bg="#000").grid(row=1, column=0, padx=10, pady=8, sticky="w")
    email_e = tk.Entry(win, width=40)
    email_e.insert(0, email)
    email_e.grid(row=1, column=1, padx=10, pady=8)

    # DATA NASC
    tk.Label(win, text="Data Nascimento:", bg="#000").grid(row=2, column=0, padx=10, pady=8, sticky="w")
    dtnasc_e = tk.Entry(win, width=20)
    dtnasc_e.insert(0, dtnasc)
    dtnasc_e.grid(row=2, column=1, padx=10, pady=8, sticky="w")

    # LOGRADOURO
    tk.Label(win, text="Logradouro:", bg="#000").grid(row=3, column=0, padx=10, pady=8, sticky="w")
    logradouro_e = tk.Entry(win, width=40)
    logradouro_e.insert(0, logradouro)
    logradouro_e.grid(row=3, column=1, padx=10, pady=8)

    tk.Label(win, text="Número:", bg="#000").grid(row=4, column=0, padx=10, pady=8, sticky="w")
    numero_e = tk.Entry(win, width=40)
    numero_e.insert(0, numero)
    numero_e.grid(row=4, column=1, padx=10, pady=8)

    tk.Label(win, text="Complemento:", bg="#000").grid(row=5, column=0, padx=10, pady=8, sticky="w")
    complemento_e = tk.Entry(win, width=40)
    complemento_e.insert(0, complemento)
    complemento_e.grid(row=5, column=1, padx=10, pady=8)

    tk.Label(win, text="CEP:", bg="#000").grid(row=6, column=0, padx=10, pady=8, sticky="w")
    cep_e = tk.Entry(win, width=40)
    cep_e.insert(0, cep)
    cep_e.grid(row=6, column=1, padx=10, pady=8)

    def salvar_edicao():
        novo_nome = nome_e.get().strip()
        novo_email = email_e.get().strip()
        nova_dtnasc = dtnasc_e.get().strip() or None
        novo_logradouro = logradouro_e.get().strip()
        novo_numero = numero_e.get().strip()
        novo_complemento = complemento_e.get().strip()
        novo_cep = cep_e.get().strip()

        if not novo_nome or not novo_email:
            messagebox.showwarning("Aviso", "Nome e e-mail são obrigatórios.")
            return

        con = None
        try:
            con = conectar()
            cur = con.cursor()
            cur.execute("""
                UPDATE Usuario
                SET Nome = %s, Email = %s, DtNasc = %s, Logradouro = %s, Numero = %s, Complemento = %s, CEP = %s
                WHERE ID_usuario = %s
            """, (novo_nome, novo_email, nova_dtnasc, novo_logradouro, novo_numero, novo_complemento, novo_cep, id_usuario))
            con.commit()
            messagebox.showinfo("Sucesso", f"Usuário {id_usuario} atualizado.")
            listar_usuarios()
            win.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar usuário:\n{e}")
        finally:
            if con:
                con.close()

    ttk.Button(win, text="Salvar Alterações",
              width=18,
              command=salvar_edicao).grid(row=9, column=1, pady=20, sticky="e")

def excluir_usuario():
    selecionado = tabela.focus()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um usuário na tabela para excluir.")
        return

    valores = tabela.item(selecionado, "values")
    if not valores:
        return

    id_usuario = valores[0]
    nome = valores[1]

    confirm = messagebox.askyesno("Confirmar", f"Excluir usuário '{nome}' (ID {id_usuario})?")
    if not confirm:
        return

    con = None
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM Usuario WHERE ID_usuario = %s", (id_usuario,))
        con.commit()
        messagebox.showinfo("Sucesso", f"Usuário '{nome}' excluído com sucesso.")
        listar_usuarios()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao excluir usuário:\n{e}")
    finally:
        if con:
            con.close()

# ================== FUNÇÕES AUXILIARES ==================
def atualizar_tabela(colunas, dados):
    tabela.delete(*tabela.get_children())
    tabela["columns"] = colunas
    tabela["show"] = "headings"
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=160, anchor="center")
    for linha in dados:
        tabela.insert("", "end", values=linha)

# ================== JANELA: CADASTRAR USUÁRIO ==================
def abrir_janela_cadastrar_usuario():
    win = tk.Toplevel(janela)
    win.title("Cadastrar Usuário")
    win.geometry("700x350")
    win.configure(bg="#000")

    frm = tk.Frame(win, bg="#000", padx=12, pady=12)
    frm.pack(fill="both", expand=True)

    def criar_campo(parent, label_texto, placeholder, linha, coluna):
        tk.Label(
            parent, 
            text=label_texto, 
            bg="black",
            fg="white",
            font=("Segoe UI", 9, "bold")
        ).grid(row=linha, column=coluna, sticky="w", padx=5)

        entrada = tk.Entry(
            parent,
            width=25,
            font=("Segoe UI", 10),
            bg="#000",          # fundo escuro
            fg="#888",             # texto inicial cinza (placeholder)
            insertbackground="white"  # cursor branco
        )
        entrada.grid(row=linha+1, column=coluna, padx=5, pady=5)

        # ----- Placeholder -----
        entrada.insert(0, placeholder)

        def focar_in(event):
            if entrada.get() == placeholder:
                entrada.delete(0, tk.END)
                entrada.config(fg="white")

        def focar_out(event):
            if entrada.get() == "":
                entrada.insert(0, placeholder)
                entrada.config(fg="#888")

        entrada.bind("<FocusIn>", focar_in)
        entrada.bind("<FocusOut>", focar_out)

        return entrada

    nome_e = criar_campo(frm, "Nome completo:", "Digite o nome do usuário", 0, 0)
    email_e = criar_campo(frm, "E-mail:", "Digite o e-mail", 0, 1)
    dtnasc_e = criar_campo(frm, "Data de Nascimento:", "AAAA-MM-DD", 0, 2)

    logradouro_e = criar_campo(frm, "Logradouro:", "Rua / Avenida", 2, 0)
    numero_e = criar_campo(frm, "Número:", "Ex: 123", 2, 1)
    cep_e = criar_campo(frm, "CEP:", "Ex: 81220000", 2, 2)

    complemento_e = criar_campo(frm, "Complemento:", "Ex: Casa, Apto, etc", 4, 0)


    def salvar_usuario():
        nome = nome_e.get().strip()
        email = email_e.get().strip()
        dtnasc = dtnasc_e.get().strip()
        logradouro = logradouro_e.get().strip()
        numero = numero_e.get().strip()
        cep = cep_e.get().strip()
        complemento = complemento_e.get().strip()

        if not (nome and email and dtnasc and logradouro and numero and cep):
            messagebox.showwarning("Aviso", "Preencha os campos obrigatórios!")
            return

        con = None
        try:
            con = conectar()
            cur = con.cursor()
            novo_id = None

            cur.execute("""
                INSERT INTO Usuario
                (Nome, Email, DtNasc, Logradouro, Numero, CEP, Complemento)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (nome, email, dtnasc, logradouro, numero, cep, complemento))

            novo_id = cur.lastrowid

            con.commit()
            messagebox.showinfo("Sucesso", f"Usuário '{nome}' cadastrado (ID {novo_id}).")
            win.destroy()
            listar_usuarios()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário:\n{e}")
        finally:
            if con:
                con.close()

    btn_salvar = ttk.Button(frm, text="Salvar Usuário",
                           width=18, command=salvar_usuario)
    btn_salvar.grid(row=5, column=1, pady=12)

# ================== JANELA: GERAR MULTA ==================
def abrir_janela_gerar_multa():
    win = tk.Toplevel(janela)
    win.title("Gerar Multa")
    win.geometry("700x320")
    win.configure(bg="#fff8f0")

    frm = tk.Frame(win, bg="#000", padx=12, pady=12)
    frm.pack(fill="both", expand=True)

    tk.Label(frm, text="Selecione o Empréstimo:", bg="#000000", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=6)
    cb_emprestimos = ttk.Combobox(frm, width=60)
    cb_emprestimos.grid(row=1, column=0, padx=6, pady=6)

    tk.Label(frm, text="Motivo:", bg="#000000", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", padx=6)
    motivo_e = tk.Entry(frm, width=60, font=("Segoe UI", 10))
    motivo_e.grid(row=3, column=0, padx=6, pady=6)

    tk.Label(frm, text="Data (AAAA-MM-DD):", bg="#000000", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w", padx=6)
    data_e = tk.Entry(frm, width=20, font=("Segoe UI", 10))
    data_e.grid(row=5, column=0, sticky="w", padx=6, pady=6)
    hoje = datetime.today().strftime("%Y-%m-%d")
    data_e.insert(0, hoje)

    tk.Label(frm, text="Validade (AAAA-MM-DD):", bg="#000000", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="e", padx=6)
    validade_e = tk.Entry(frm, width=20, font=("Segoe UI", 10))
    validade_e.grid(row=5, column=0, sticky="e", padx=(0,6), pady=6)
    validade_e.insert(0, (datetime.today() + timedelta(days=30)).strftime("%Y-%m-%d"))

    # preencher combobox com empréstimos existentes (id, usuario, status)
    con = None
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT E.ID_emprestimo, U.Nome, L.Titulo
            FROM Emprestimo_Empresta E
            JOIN Usuario U ON E.fk_Usuario_ID_usuario = U.ID_usuario
            JOIN Copia C ON E.fk_Copia_ID_copia = C.ID_copia
            JOIN Livro L ON C.fk_Livro_ID_livro = L.ID_livro
            ORDER BY U.Nome
        """)
        rows = cur.fetchall()
        options = [f"{r[0]} - {r[1]} / {r[2]}" for r in rows]
        cb_emprestimos["values"] = options
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar empréstimos:\n{e}")
    finally:
        if con:
            con.close()

    def salvar_multa():
        sel = cb_emprestimos.get().strip()
        motivo = motivo_e.get().strip()
        data = data_e.get().strip()
        validade = validade_e.get().strip()

        if not sel:
            messagebox.showwarning("Aviso", "Escolha um empréstimo.")
            return
        if not motivo:
            messagebox.showwarning("Aviso", "Informe o motivo da multa.")
            return

        id_emprestimo = int(sel.split(" - ")[0])

        con = None
        try:
            con = conectar()
            cur = con.cursor()

            cur.execute("""
                INSERT INTO Multa
                (Motivo, Data, Validade, fk_Emprestimo_Empresta_ID_emprestimo)
                VALUES (%s, %s, %s, %s)
            """, (motivo, data, validade, id_emprestimo))

            con.commit()
            novo_id = cur.lastrowid

            messagebox.showinfo("Sucesso", f"Multa gerada (ID {novo_id}) para empréstimo {id_emprestimo}.")
            win.destroy()
            listar_multas()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar multa:\n{e}")
        finally:
            if con:
                con.close()
    ttk.Button(frm, text="Criar Multa",
        width=20, command=salvar_multa).grid(row=6, column=0, pady=12)

# ================== JANELA: FAZER EMPRÉSTIMO ==================
def abrir_janela_fazer_emprestimo():
    win = tk.Toplevel(janela)
    win.title("Fazer Empréstimo")
    win.geometry("760x380")
    win.configure(bg="#f0fff4")

    frm = tk.Frame(win, bg="#000", padx=12, pady=12)
    frm.pack(fill="both", expand=True)

    tk.Label(frm, text="Selecione Usuário:", bg="#000000", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=6)
    cb_usuario = ttk.Combobox(frm, width=40)
    cb_usuario.grid(row=1, column=0, padx=6, pady=6)

    tk.Label(frm, text="Selecione Cópia disponível:", bg="#000000", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", padx=6)
    cb_copia = ttk.Combobox(frm, width=60)
    cb_copia.grid(row=3, column=0, padx=6, pady=6)

    tk.Label(frm, text="Data do Empréstimo (AAAA-MM-DD):", bg="#000000", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w", padx=6)
    dt_emp_e = tk.Entry(frm, width=20, font=("Segoe UI", 10))
    dt_emp_e.grid(row=5, column=0, padx=6, pady=6, sticky="w")
    hoje = datetime.today().strftime("%Y-%m-%d")
    dt_emp_e.insert(0, hoje)

    tk.Label(frm, text="Data Prevista (AAAA-MM-DD):", bg="#000000", font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="e", padx=6)
    dt_prev_e = tk.Entry(frm, width=20, font=("Segoe UI", 10))
    dt_prev_e.grid(row=5, column=0, padx=6, pady=6, sticky="e")
    dt_prev_e.insert(0, (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d"))

    # carregar usuários e cópias disponíveis
    con = None
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT ID_usuario, Nome FROM Usuario ORDER BY Nome")
        usuarios = cur.fetchall()
        cb_usuario["values"] = [f"{u[0]} - {u[1]}" for u in usuarios]

        # cópias disponíveis (Disponibilidade = 'Disponível')
        cur.execute("""
            SELECT C.ID_copia, L.Titulo
            FROM Copia C
            JOIN Livro L ON C.fk_Livro_ID_livro = L.ID_livro
            WHERE C.Disponibilidade LIKE 'Disponível'
            ORDER BY L.Titulo
        """)
        copias = cur.fetchall()
        cb_copia["values"] = [f"{c[0]} - {c[1]}" for c in copias]
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")
    finally:
        if con:
            con.close()

    def salvar_emprestimo():
        sel_user = cb_usuario.get().strip()
        sel_copia = cb_copia.get().strip()
        dt_emp = dt_emp_e.get().strip()
        dt_prev = dt_prev_e.get().strip()

        if not sel_user:
            messagebox.showwarning("Aviso", "Selecione um usuário.")
            return
        if not sel_copia:
            messagebox.showwarning("Aviso", "Selecione uma cópia disponível.")
            return

        id_usuario = int(sel_user.split(" - ")[0])
        id_copia = int(sel_copia.split(" - ")[0])

        con = None
        try:
            con = conectar()
            cur = con.cursor()
            novo_id = None

            status = "Em andamento"

            cur.execute("""
                INSERT INTO Emprestimo_Empresta
                (DtEmprestimo, DtDevolucao, DtDevolucaoPrevista, Status, fk_Usuario_ID_usuario, fk_Copia_ID_copia)
                VALUES (%s, NULL, %s, %s, %s, %s)
            """, (dt_emp, dt_prev, status, id_usuario, id_copia))

            # marcar copia como Indisponível
            cur.execute("UPDATE Copia SET Disponibilidade = %s WHERE ID_copia = %s", ("Indisponível", id_copia))
            con.commit()
            messagebox.showinfo("Sucesso", f"Empréstimo criado (ID {novo_id}) para usuário {id_usuario} e cópia {id_copia}.")
            win.destroy()
            listar_usuarios()  # opcional: atualizar listagens
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar empréstimo:\n{e}")
        finally:
            if con:
                con.close()

    ttk.Button(frm, text="Criar Empréstimo",
              width=20, command=salvar_emprestimo).grid(row=6, column=0, pady=12)

# ================== INTERFACE PRINCIPAL ==================
janela = tk.Tk()
janela.title("📚 CodeTeca - Sistema da Biblioteca")
janela.geometry("1100x720")
janela.configure(bg="#000")

style = ttk.Style()
style.configure("TButton", padding=6)
style.configure("Treeview.Heading")
style.configure("Treeview")

titulo = tk.Label(janela, text="CodeTeca - Sistema da Biblioteca", bg="#003366", fg="white",
                  font=("Segoe UI", 18, "bold"), pady=12)
titulo.pack(fill="x")

frame_botoes = tk.Frame(janela, bg="#000")
frame_botoes.pack(pady=12)

# botões principais (abrir janelas)
ttk.Button(frame_botoes, text="💸 Gerar Multa",
          width=18, command=abrir_janela_gerar_multa).grid(row=1, column=0, padx=8)
ttk.Button(frame_botoes, text="🤝 Fazer Empréstimo",
          width=18, command=abrir_janela_fazer_emprestimo).grid(row=1, column=1, padx=8)

# botões de listagem existentes
ttk.Button(frame_botoes, text="📝 Cadastrar Usuário", 
           width=18, command=abrir_janela_cadastrar_usuario).grid(row=2, column=0, pady=6, padx=8)
ttk.Button(frame_botoes, text="✏️ Editar Usuário", 
           width=18, command=abrir_janela_editar_usuario).grid(row=2, column=1, pady=6, padx=8)
ttk.Button(frame_botoes, text="🗑️ Excluir Usuário", 
           width=18, command=excluir_usuario).grid(row=2, column=2, pady=6, padx=8)
# === BOTÕES PRINCIPAIS (SUBSTITUIR TUDO O QUE VOCÊ TINHA) ===
frame_botoes.pack(pady=10)

ttk.Button(frame_botoes, text="👤 Listar Usuários",
           width=18, command=listar_usuarios).grid(row=0, column=0, padx=8, pady=5)

ttk.Button(frame_botoes, text="📚 Listar Livros",
           width=18, command=listar_livros).grid(row=0, column=1, padx=8, pady=5)

ttk.Button(frame_botoes, text="💲 Listar Multas",
           width=18, command=listar_multas).grid(row=0, column=2, padx=8, pady=5)

ttk.Button(frame_botoes, text="🎒 Listar Empréstimos",
           width=18, command=listar_emprestimos).grid(row=0, column=3, padx=8, pady=5)


# tabela de resultados (mantida)
frame_tabela = tk.Frame(janela, bg="#000")
frame_tabela.pack(fill="both", expand=True, padx=16, pady=6)

tabela = ttk.Treeview(frame_tabela)
tabela.pack(fill="both", expand=True, side="left")

scroll_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
tabela.configure(yscroll=scroll_y.set)
scroll_y.pack(side="right", fill="y")

rodape = tk.Label(janela, text="CodeTeca", bg="#003366", fg="white",
                  font=("Segoe UI", 10, "italic"), pady=6)
rodape.pack(fill="x", side="bottom")

# inicializa com listagem de usuários para mostrar algo
listar_usuarios()

janela.mainloop()
