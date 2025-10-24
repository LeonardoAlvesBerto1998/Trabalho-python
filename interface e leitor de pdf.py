##APENAS INTERFACE##
import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import requests
import re

# Função para ler texto do PDF

def Get_text_from_PDFfiles_usingPyPDF2(in_PdfFile):
    # Abre o arquivo PDF e extrai o texto de todas as páginas
    reader = PyPDF2.PdfReader(in_PdfFile)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text()
    return texto

def extrair_datas(texto):
    # Expressão  para extrair datas no formato dd/mm/aaaa
    padrao = r'\d{4}-\d{2}-\d{2}'
    datas = re.findall(padrao, texto)
    return datas

def verificar_feriados(datas):
    feriados_encontrados = []

    for data in datas:
        # Separando o dia, mês e ano
        a, m, d = data.split("-")

        url = f"https://date.nager.at/api/v3/PublicHolidays/{a}/BR"
        try:
            resposta = requests.get(url)
            if resposta.status_code == 200:
                feriados_api = resposta.json()
                feriados = [f["date"] for f in feriados_api]  # Formato: 'aaaa-mm-dd'
                
                # Converte a data do PDF (dd/mm/aaaa) para o formato aaaa-mm-dd
                formato_api = f"{a}-{m}-{d}"
                if formato_api in feriados:
                    feriados_encontrados.append(data)
            else:
                messagebox.showerror("Erro", f"Erro ao acessar a API de feriados para o ano {a}.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao fazer a requisição à API para o ano {a}: {e}")

    return feriados_encontrados




# Interface Gráfica (Tkinter)

def InterfacePrincipal():
    root = tk.Tk()
    root.title("Verificador de Feriados")
    root.geometry("400x200")
    root.resizable(False, False)

    label = tk.Label(root, text="Escolha um arquivo PDF para verificar feriados", font=("Arial", 11))
    label.pack(pady=15)

    botao_escolher = tk.Button(root, text="Escolher Arquivo PDF", command=EscolherArquivoPDF, font=("Arial", 12))
    botao_escolher.pack(pady=20)

    root.mainloop()


# Função principal chamada pelo botão

def EscolherArquivoPDF():
    caminho_pdf = filedialog.askopenfilename(
        title="Escolha o arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )

    if not caminho_pdf:
        messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")
        return
    
    # Lê o conteúdo do PDF
    texto_pdf = Get_text_from_PDFfiles_usingPyPDF2(caminho_pdf)
    
    # Extrai as datas do texto
    datas_encontradas = extrair_datas(texto_pdf)

    if not datas_encontradas:
        messagebox.showinfo("Informação", "Nenhuma data encontrada no PDF.")
        return

    # Verifica feriados
    feriados = verificar_feriados(datas_encontradas)

    if feriados:
        msg = f"As seguintes datas são feriados:\n\n" + "\n".join(feriados)
    else:
        msg = "Nenhuma das datas encontradas é feriado."

    messagebox.showinfo("Resultado", msg)


# Executar interface

if __name__ == "__main__":
    InterfacePrincipal()

