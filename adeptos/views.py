import tkinter as tk
import matplotlib.pyplot as plt

class AdeptosView:
    def __init__(self, master, adeptos_controller, cadastrar_callback):
        self.master = master
        self.adeptos_controller = adeptos_controller
        self.cadastrar_callback = cadastrar_callback
        
        master.title('Inquérito de Adeptos')
        master.geometry('600x400')
        
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

        self.btn_plot_pizza = tk.Button(self.master, text="Adeptos por Distrito", command=self.plot_pizza)
        self.btn_plot_pizza.pack()


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
        self.plot_grafico(tipo_grafico='barras')

    def plot_linha(self):
        self.plot_grafico(tipo_grafico='linha')

    def plot_ambos(self):
        self.plot_grafico(tipo_grafico='ambos')
    
    def plot_barras(self):
        dados = self.adeptos_controller.get_dados_para_grafico()
        equipas = [row[0] for row in dados]
        quantidades = [row[2] for row in dados]

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
        equipas = [row[0] for row in dados]
        medias_idade = [row[3] for row in dados]

        fig, ax = plt.subplots()
        line = ax.plot(equipas, medias_idade, marker='o')

        for i, txt in enumerate(medias_idade):
            ax.annotate(round(txt, 2), (equipas[i], medias_idade[i]))

        plt.xlabel('Equipa')
        plt.ylabel('Média de Idade')
        plt.title('Média de Idade dos Adeptos por Equipa')
        plt.show()

    def plot_pizza(self):
        dados = self.adeptos_controller.get_dados_para_grafico()
        distritos = [row[1] for row in dados]
        quantidades = [row[2] for row in dados]
        equipas = [row[0] for row in dados]

        cores = {'Benfica': 'red', 'Sporting': 'green', 'Porto': 'blue', 'Outros': 'orange'}

        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(quantidades, labels=distritos, autopct='%1.1f%%', startangle=90,
                                        colors=[cores.get(equipe, 'gray') for equipe in equipas])

        # Adiciona o nome da equipe como legenda de cor
        for i, txt in enumerate(autotexts):
            txt.set_text(f'{equipas[i]} - {txt.get_text()}')

        plt.axis('equal')
        plt.title('Quantidade de Adeptos por Distrito por Equipa')
        plt.show()



