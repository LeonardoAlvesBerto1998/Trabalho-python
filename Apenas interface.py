##APENAS INTERFACE##
import tkinter as tk
from tkinter import filedialog, messagebox


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

