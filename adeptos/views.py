import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import matplotlib.offsetbox as offsetbox


class AdeptosView:
    def __init__(self, master, adeptos_controller, cadastrar_callback):
        self.master = master
        self.adeptos_controller = adeptos_controller
        self.cadastrar_callback = cadastrar_callback

        master.title("Inquérito de Adeptos")
        master.geometry("750x500")

        # Carregar a imagem usando o Pillow (PIL)
        background_image = Image.open(
            "/Users/rodrigo/Documents/Estudos/Projetos pessoais/Projetos/Projetos Python/Tkinter/adeptos/images/campo.png"
        )
        self.background_photo = ImageTk.PhotoImage(background_image)

        # Configurar a imagem de fundo na janela
        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.photo = self.background_photo
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_widgets()

        icon = Image.open(
            r"/Users/rodrigo/Documents/Estudos/Projetos pessoais/Projetos/Projetos Python/Tkinter/adeptos/images/form.png"
        )  # ícone
        icon_photo = ImageTk.PhotoImage(icon)
        master.tk.call("wm", "iconphoto", master._w, icon_photo)

    def create_widgets(self):
        style = ttk.Style()

        # Configure o estilo do botão para remover a borda
        style.configure(
            "TButton",
            relief="flat",
            background="#0074cc",
            foreground="white",
            padding=-5,
            font=("Helvetica", 14),
            borderwidth=1,
        )

        style.configure(
            'TFrame', 
            background="yellow",
            foreground="darkblue"
        )

        # Frame para informações do adepto (coluna da esquerda)
        frame_info_adepto = ttk.Frame(self.master, padding=(20, 20), style='TFrame')
        frame_info_adepto.grid(row=0, column=0, padx=35, pady=170, sticky="n")

        title_label_adepto = ttk.Label(
            frame_info_adepto, text="Cadastrar adepto", font=("Helvetica", 22, "bold")
        )
        title_label_adepto.grid(row=0, column=0, columnspan=2, pady=10, sticky="N")
        self.add_icon_to_label(
            title_label_adepto,
            "/Users/rodrigo/Documents/Estudos/Projetos pessoais/Projetos/Projetos Python/Tkinter/adeptos/images/bola.png",
        )

        ttk.Label(frame_info_adepto, text="Nome:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.entry_nome = ttk.Entry(frame_info_adepto)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_info_adepto, text="Idade:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.entry_idade = ttk.Entry(frame_info_adepto)
        self.entry_idade.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_info_adepto, text="Distrito:").grid(
            row=3, column=0, padx=5, pady=5, sticky="w"
        )
        self.distrito = [
            "Aveiro",
            "Beja",
            "Braga",
            "Bragança",
            "Castelo Branco",
            "Coimbra",
            "Évora",
            "Faro",
            "Guarda",
            "Leiria",
            "Lisboa",
            "Portalegre",
            "Porto",
            "Santarém",
            "Setúbal",
            "Viana do Castelo",
            "Vila Real",
            "Viseu",
        ]
        self.selected_distrito = tk.StringVar(frame_info_adepto)
        self.dropdown_distrito = ttk.Combobox(
            frame_info_adepto, textvariable=self.selected_distrito, values=self.distrito
        )
        self.dropdown_distrito.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame_info_adepto, text="Equipa:").grid(
            row=4, column=0, padx=5, pady=5, sticky="w"
        )
        self.equipas = ["Benfica", "Porto", "Sporting", "Outros"]
        self.selected_equipa = tk.StringVar(frame_info_adepto)
        self.dropdown_equipa = ttk.Combobox(
            frame_info_adepto, textvariable=self.selected_equipa, values=self.equipas
        )
        self.dropdown_equipa.grid(row=4, column=1, padx=5, pady=5)

        self.btn_cadastrar = ttk.Button(
            frame_info_adepto, text="Cadastrar", command=self.cadastrar_callback
        )
        self.btn_cadastrar.grid(row=5, column=0, columnspan=2, pady=10, sticky="N")

        # Frame para botões de gráficos (coluna da direita)
        frame_botoes = ttk.Frame(self.master, padding=(50, 27))
        frame_botoes.grid(row=0, column=1, padx=0, pady=170, columnspan=6, sticky="n")
        self.set_transparent_background(frame_botoes)

        title_label_botoes = ttk.Label(
            frame_botoes, text="Gerar gráficos", font=("Helvetica", 22, "bold")
        )
        title_label_botoes.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="N")
        self.add_icon_to_label(
            title_label_botoes,
            "/Users/rodrigo/Documents/Estudos/Projetos pessoais/Projetos/Projetos Python/Tkinter/adeptos/images/form.png",
        )

        self.btn_plot_barras = ttk.Button(
            frame_botoes, text="Qtde de Adeptos", command=self.plot_barras
        )
        self.btn_plot_barras.grid(row=1, column=0, padx=5, pady=10, sticky="N")

        self.btn_plot_linha = ttk.Button(
            frame_botoes, text="Média de idade dos Adeptos", command=self.plot_linha
        )
        self.btn_plot_linha.grid(row=2, column=0, padx=5, pady=10, sticky="N")

        self.btn_plot_barras_empilhadas = ttk.Button(
            frame_botoes,
            text="Adeptos por Distrito",
            command=self.plot_barras_empilhadas,
        )
        self.btn_plot_barras_empilhadas.grid(
            row=3, column=0, padx=5, pady=10, sticky="N"
        )

        self.btn_exportar_relatorio = ttk.Button(
            frame_botoes,
            text="Exportar Relatório PDF",
            command=self.exportar_relatorio_pdf,
        )
        self.btn_exportar_relatorio.grid(row=4, column=0, padx=5, pady=(10, 33), sticky="N")

    def get_adepto_info(self):
        nome = self.entry_nome.get()
        idade = self.entry_idade.get()
        distrito = self.selected_distrito.get()
        equipa = self.selected_equipa.get()
        return nome, idade, distrito, equipa
        self.btn_exportar_relatorio = ttk.Button(
            frame_botoes,
            text="Exportar Relatório PDF",
            command=self.exportar_relatorio_pdf,
        )
        self.btn_exportar_relatorio.grid(row=4, column=0, padx=5, pady=(10, 33), sticky="N")

    def clear_fields(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)
        self.selected_distrito.set(None)
        self.selected_equipa.set(None)
    
    def set_transparent_background(self, widget):
        img = tk.PhotoImage(width=1, height=1)
        widget.configure(image=img)
        widget.image = img

    def add_icon_to_widget(self, widget, icon_path):
        icon = Image.open(icon_path)
        icon = icon.resize((25, 25))
        icon = ImageTk.PhotoImage(icon)
        icon_label = ttk.Label(widget, image=icon)
        icon_label.image = icon
        icon_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    def add_icon_to_label(self, label, icon_path):
        icon = Image.open(icon_path)
        icon = icon.resize((25, 25))
        icon = ImageTk.PhotoImage(icon)

        # Create a frame to hold both the icon and the label text
        frame = ttk.Frame(label, padding=(5, 5))
        frame.grid(row=0, column=0, sticky="w")

        # Add the icon to the frame
        icon_label = ttk.Label(frame, image=icon)
        icon_label.image = icon
        icon_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")

        # Add the label text to the frame
        text_label = ttk.Label(frame, text=label.cget("text"), font=label.cget("font"))
        text_label.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="w")

        return frame

    def set_transparent_background(self, widget):
        # Criar uma imagem transparente
        img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        transparent_img = ImageTk.PhotoImage(img)

        # Criar um label para exibir a imagem
        img_label = tk.Label(widget, image=transparent_img)
        img_label.image = transparent_img
        img_label.place(relwidth=1, relheight=1)

    def exportar_relatorio_pdf(self):
        # Pede ao usuário para escolher a pasta de destino
        folder_selected = filedialog.askdirectory(title="Escolha a Pasta para Exportar")

        # Se o usuário cancelar a seleção, saia sem exportar
        if not folder_selected:
            return

        # Nome do arquivo PDF
        pdf_filename = "Relatório de Inquérito de Adeptos.pdf"

        # Caminho completo do arquivo PDF
        pdf_path = os.path.join(folder_selected, pdf_filename)

        # Se o arquivo já existe, adiciona um número ao nome do arquivo
        count = 1
        while os.path.exists(pdf_path):
            pdf_filename = f"Relatório de Inquérito de Adeptos_{count}.pdf"
            pdf_path = os.path.join(folder_selected, pdf_filename)
            count += 1

        # Cria um objeto PdfPages para salvar os gráficos no PDF
        with PdfPages(pdf_path) as pdf:
            # Adiciona um cabeçalho ao PDF
            self.adicionar_cabecalho(pdf)

            # Gera e salva o gráfico de barras no PDF
            self.plot_barras(pdf)

            # Gera e salva o gráfico de linha no PDF
            self.plot_linha(pdf)

            # Gera e salva o gráfico de barras empilhadas no PDF
            self.plot_barras_empilhadas(pdf)

        # Mensagem de sucesso
        messagebox.showinfo(
            "Relatório Exportado",
            f"O relatório foi exportado com sucesso para {pdf_path}",
        )

    def adicionar_cabecalho(self, pdf):
        # Adiciona um cabeçalho ao PDF
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(
            0.5,
            0.95,
            "Relatório de Inquérito de Adeptos",
            ha="center",
            va="center",
            fontsize=16,
        )

        # Adiciona texto descritivo
        descricao = (
            "Este relatório apresenta informações sobre os adeptos de diferentes equipas em vários distritos.\n"
            "Os gráficos fornecem uma visão detalhada da distribuição de adeptos por equipa, distrito e média de idade."
        )
        ax.text(
            0.5,
            0.85,
            descricao,
            ha="center",
            va="center",
            fontsize=12,
            color="gray",
            wrap=True,
        )

        ax.axis("off")  # Desativa os eixos para um cabeçalho limpo
        pdf.savefig()
        plt.close()

    def plot_barras(self, pdf=None):
        dados = self.adeptos_controller.get_dados_para_grafico()

        soma_por_equipa = {"Benfica": 0, "Sporting": 0, "Porto": 0, "Outros": 0}

        for row in dados:
            equipe = row[0]
            quantidade = row[2]
            soma_por_equipa[equipe] += quantidade

        equipas = list(soma_por_equipa.keys())
        quantidades = list(soma_por_equipa.values())

        cores = {
            "Benfica": "red",
            "Sporting": "green",
            "Porto": "blue",
            "Outros": "orange",
        }

        fig, ax = plt.subplots(figsize=(12, 6))

        for equipe, quantidade, bar in zip(
            equipas,
            quantidades,
            ax.bar(
                equipas,
                quantidades,
                color=[cores.get(equipe, "gray") for equipe in equipas],
            ),
        ):
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval,
                round(yval, 2),
                ha="center",
                va="bottom",
            )

            img_paths = {
                "Benfica": "images/benfica.png",
                "Sporting": "images/sporting.png",
                "Porto": "images/porto.png",
                "Outros": "images/port.png",
            }

            img_path = img_paths.get(
                equipe, "images/port.png"
            )
            img = plt.imread(img_path)

            img_height = bar.get_height() * 0.8
            img_width = bar.get_width() * 0.8
            img_x = (
                bar.get_x() + bar.get_width() * 0.5
            )

            imagebox = AnnotationBbox(
                OffsetImage(img, zoom=0.3, resample=True, clip_path=None, clip_box=None),
                (img_x, yval - img_height / 2),
                frameon=False,
                xycoords="data",
                boxcoords="data",
                pad=0,
            )
            ax.add_artist(imagebox)

        plt.xlabel("")
        plt.ylabel("Quantidade de Adeptos")
        plt.title("Quantidade de Adeptos por Equipa")

        ax.set_xticks([])
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        if pdf is None:
            plt.show()
        else:
            pdf.savefig()
            plt.close()

    def plot_linha(self, pdf=None):
        dados = self.adeptos_controller.get_dados_para_grafico()

        media_idade_por_equipa = {"Benfica": 0, "Sporting": 0, "Porto": 0, "Outros": 0}

        contagem_por_equipa = {"Benfica": 0, "Sporting": 0, "Porto": 0, "Outros": 0}

        for row in dados:
            equipe = row[0]
            quantidade = row[2]
            idade_media = row[3]

            media_idade_por_equipa[equipe] += idade_media * quantidade
            contagem_por_equipa[equipe] += quantidade

        for equipe in media_idade_por_equipa:
            if contagem_por_equipa[equipe] > 0:
                media_idade_por_equipa[equipe] /= contagem_por_equipa[equipe]

        equipas = list(media_idade_por_equipa.keys())
        medias_idade = list(media_idade_por_equipa.values())

        cores = {
            "Benfica": "red",
            "Sporting": "green",
            "Porto": "blue",
            "Outros": "orange",
        }

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(equipas, medias_idade, marker="o")

        for i, txt in enumerate(medias_idade):
            ax.annotate(round(txt, 1), (equipas[i], medias_idade[i]))

        plt.xlabel("Equipa")
        plt.ylabel("Média de Idade")
        plt.title("Média de Idade dos Adeptos por Equipa")

        # Salva o gráfico no PDF
        if pdf is None:
            plt.show()
        else:
            # Se pdf for fornecido, salva o gráfico no PDF
            pdf.savefig()
            plt.close()

    def plot_barras_empilhadas(self, pdf=None):
        dados = self.adeptos_controller.get_dados_para_grafico()
        distritos = sorted(list(set([row[1] for row in dados])))
        equipas = ["Benfica", "Sporting", "Porto", "Outros"]

        quantidades_por_equipe_e_distrito = np.zeros((len(equipas), len(distritos)))

        for row in dados:
            equipe = row[0]
            distrito = row[1]
            quantidade = row[2]
            indice_equipe = equipas.index(equipe)
            indice_distrito = distritos.index(distrito)
            quantidades_por_equipe_e_distrito[
                indice_equipe, indice_distrito
            ] += quantidade

        soma_por_distrito = np.sum(quantidades_por_equipe_e_distrito, axis=0)

        distritos_ordenados = [
            distrito
            for _, distrito in sorted(zip(soma_por_distrito, distritos), reverse=True)
        ]

        cores = {
            "Benfica": "red",
            "Sporting": "green",
            "Porto": "blue",
            "Outros": "orange",
        }

        fig, ax = plt.subplots(
            figsize=(12, 6)
        )  # Ajuste os valores de largura e altura conforme necessário
        bottom = np.zeros(len(distritos_ordenados))

        for i, equipe in enumerate(equipas):
            barra = ax.barh(
                distritos_ordenados,
                [
                    quantidades_por_equipe_e_distrito[i, distritos.index(distrito)]
                    for distrito in distritos_ordenados
                ],
                color=cores.get(equipe, "gray"),
                label=equipe,
                left=bottom,
            )
            bottom += [
                quantidades_por_equipe_e_distrito[i, distritos.index(distrito)]
                for distrito in distritos_ordenados
            ]

            for rect, quantidade in zip(
                barra,
                [
                    quantidades_por_equipe_e_distrito[i, distritos.index(distrito)]
                    for distrito in distritos_ordenados
                ],
            ):
                if quantidade > 0:
                    width = rect.get_width()
                    height = rect.get_height()
                    ax.text(
                        rect.get_x() + width / 2,
                        rect.get_y() + height / 2,
                        f"{int(quantidade)}",
                        ha="center",
                        va="center",
                        color="white",
                    )

        plt.ylabel("Distrito")
        plt.xlabel("Quantidade de Adeptos")
        plt.title("Quantidade de Adeptos por Distrito por Equipa")
        plt.legend()

        # Salva o gráfico no PDF
        if pdf is None:
            plt.show()
        else:
            # Se pdf for fornecido, salva o gráfico no PDF
            pdf.savefig()
            plt.close()
