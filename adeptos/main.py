import tkinter as tk
from tkinter import messagebox
from views import AdeptosView
from controllers import Adeptos

def cadastrar():
    nome, idade, distrito, equipa = view.get_adepto_info()
    adeptos_controller.cadastro_adepto(nome, idade, distrito, equipa)
    view.clear_fields()
    messagebox.showinfo("Sucesso", "Adepto cadastrado com sucesso.")
    icon_path = '/Users/rodrigo/Documents/Estudos/Projetos pessoais/Projetos/Projetos Python/Tkinter/adeptos/bola.png'
    top = tk.Toplevel()
    top.iconbitmap(icon_path)

"""     # Chama o método para plotar o gráfico
    view.plot_grafico() """


if __name__ == "__main__":
    root = tk.Tk()

    adeptos_controller = Adeptos()

    def on_cadastrar():
        cadastrar()

    view = AdeptosView(root, adeptos_controller, on_cadastrar)
    root.mainloop()
    adeptos_controller.export_csv('/Users/rodrigo/Documents/Estudos/Projetos pessoais/Projetos/Projetos Python/Tkinter/ADEPTOS/adeptos.csv')

    adeptos_controller.fechar_conexao()
