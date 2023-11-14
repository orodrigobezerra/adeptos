import tkinter as tk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import numpy as np

class AdeptosView:
    def __init__(self, master, adeptos_controller, cadastrar_callback):
        self.master = master
        self.adeptos_controller = adeptos_controller
        self.cadastrar_callback = cadastrar_callback
        
        master.title('Inquérito de Adeptos')
        master.geometry('600x400')

        icon = Image.open(r"/Users/rodrigo/Documents/Estudos/Projetos pessoais/Projetos/Projetos Python/Tkinter/adeptos/form.png") # icon
        icon_photo =ImageTk.PhotoImage(icon)
        master.tk.call("wm","iconphoto", master._w,icon_photo)
        
        self.create_widgets()

    def create_widgets(self):
        self.label_nome = tk.Label(self.master, text="Nome:")
        self.label_nome.pack()
        self.entry_nome = tk.Entry(self.master)
        self.entry_nome.pack()

        self.label_idade = tk.Label(self.master, text="Idade:")
        self.label_idade.pack()
        self.entry_idade = tk.Entry(self.master)
        self.entry_idade.pack()

        self.label_distrito = tk.Label(self.master, text="Escolha o Distrito:")
        self.label_distrito.pack()
        self.distrito = ['Aveiro', 'Beja', 'Braga', 'Bragança', 'Castelo Branco', 'Coimbra', 'Évora', 'Faro', 'Guarda', 'Leiria', 'Lisboa', 'Portalegre', 'Porto', 'Santarém', 'Setúbal', 'Viana do Castelo', 'Vila Real', 'Viseu']  
        self.selected_distrito = tk.StringVar(self.master)
        self.dropdown = tk.OptionMenu(self.master, self.selected_distrito, *self.distrito)
        self.dropdown.pack()
        
        self.label_equipa = tk.Label(self.master, text="Escolha a equipa:")
        self.label_equipa.pack()

        self.equipas = ['Benfica', 'Porto', 'Sporting', 'Outros']  
        self.selected_equipa = tk.StringVar(self.master)
        self.dropdown = tk.OptionMenu(self.master, self.selected_equipa, *self.equipas)
        self.dropdown.pack()

        self.btn_cadastrar = tk.Button(self.master, text="Cadastrar", command=self.cadastrar_callback)
        self.btn_cadastrar.pack()

        self.btn_plot_barras = tk.Button(self.master, text="Qtde de Adeptos", command=self.plot_barras)
        self.btn_plot_barras.pack()

        self.btn_plot_linha = tk.Button(self.master, text="Média de idade dos Adeptos ", command=self.plot_linha)
        self.btn_plot_linha.pack()

        self.btn_plot_barras_empilhadas = tk.Button(self.master, text="Adeptos por Distrito", command=self.plot_barras_empilhadas)
        self.btn_plot_barras_empilhadas.pack()


    def get_adepto_info(self):
        nome = self.entry_nome.get()
        idade = self.entry_idade.get()
        distrito = self.selected_distrito.get()
        equipa = self.selected_equipa.get()
        return nome, idade, distrito, equipa

    def clear_fields(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)

    
    def plot_barras(self):
        dados = self.adeptos_controller.get_dados_para_grafico()

        soma_por_equipa = {'Benfica': 0, 'Sporting': 0, 'Porto': 0, 'Outros': 0}

        for row in dados:
            equipe = row[0]
            quantidade = row[2]
            soma_por_equipa[equipe] += quantidade

        equipas = list(soma_por_equipa.keys())
        quantidades = list(soma_por_equipa.values())

        cores = {'Benfica': 'red', 'Sporting': 'green', 'Porto': 'blue', 'Outros': 'orange'}

        fig, ax = plt.subplots()
        bars = ax.bar(equipas, quantidades, color=[cores.get(equipe, 'gray') for equipe in equipas])

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

        plt.xlabel('Equipa')
        plt.ylabel('Quantidade de Adeptos')
        plt.title('Quantidade de Adeptos por Equipa')
        plt.show()


    def plot_linha(self):
        dados = self.adeptos_controller.get_dados_para_grafico()

        media_idade_por_equipa = {'Benfica': 0, 'Sporting': 0, 'Porto': 0, 'Outros': 0}

        contagem_por_equipa = {'Benfica': 0, 'Sporting': 0, 'Porto': 0, 'Outros': 0}

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

        cores = {'Benfica': 'red', 'Sporting': 'green', 'Porto': 'blue', 'Outros': 'orange'}

        fig, ax = plt.subplots()
        ax.plot(equipas, medias_idade, marker='o')

        for i, txt in enumerate(medias_idade):
            ax.annotate(round(txt, 1), (equipas[i], medias_idade[i]))

        plt.xlabel('Equipa')
        plt.ylabel('Média de Idade')
        plt.title('Média de Idade dos Adeptos por Equipa')
        plt.show()


    def plot_barras_empilhadas(self):
        dados = self.adeptos_controller.get_dados_para_grafico()
        distritos = sorted(list(set([row[1] for row in dados])))
        equipas = ['Benfica', 'Sporting', 'Porto', 'Outros']

        # Inicializa uma matriz para armazenar as quantidades por equipe e distrito
        quantidades_por_equipe_e_distrito = np.zeros((len(equipas), len(distritos)))

        # Preenche a matriz com as quantidades
        for row in dados:
            equipe = row[0]
            distrito = row[1]
            quantidade = row[2]
            indice_equipe = equipas.index(equipe)
            indice_distrito = distritos.index(distrito)
            quantidades_por_equipe_e_distrito[indice_equipe, indice_distrito] += quantidade

        # Calcula a soma total de cada distrito
        soma_por_distrito = np.sum(quantidades_por_equipe_e_distrito, axis=0)

        # Ordena os distritos com base na soma total
        distritos_ordenados = [distrito for _, distrito in sorted(zip(soma_por_distrito, distritos), reverse=True)]

        # Configuração das cores
        cores = {'Benfica': 'red', 'Sporting': 'green', 'Porto': 'blue', 'Outros': 'orange'}

        # Cria o gráfico de barras empilhadas
        fig, ax = plt.subplots()
        bottom = np.zeros(len(distritos_ordenados))

        for i, equipe in enumerate(equipas):
            # Reorganiza as barras com base na ordem dos distritos ordenados
            barra = ax.bar(distritos_ordenados, [quantidades_por_equipe_e_distrito[i, distritos.index(distrito)] for distrito in distritos_ordenados],
                        color=cores.get(equipe, 'gray'), label=equipe, bottom=bottom)
            bottom += [quantidades_por_equipe_e_distrito[i, distritos.index(distrito)] for distrito in distritos_ordenados]

            # Adiciona o número de adeptos no meio de cada barra (quando a quantidade é maior que 0)
            for rect, quantidade in zip(barra, [quantidades_por_equipe_e_distrito[i, distritos.index(distrito)] for distrito in distritos_ordenados]):
                if quantidade > 0:
                    height = rect.get_height()
                    width = rect.get_width()
                    ax.text(rect.get_x() + width / 2, rect.get_y() + height / 2, f'{int(quantidade)}', ha='center', va='center', color='white')

        plt.xlabel('Distrito')
        plt.ylabel('Quantidade de Adeptos')
        plt.title('Quantidade de Adeptos por Distrito por Equipa')
        plt.legend()
        plt.show()



