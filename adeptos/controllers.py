# Inquerito para saber qual a equipa com maior número de adeptos de Portugal

import sqlite3 as sql
import csv

class Adeptos:
    def __init__(self):
        self.conn = sql.connect('adeptos.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute( """
        CREATE TABLE IF NOT EXISTS adeptos (
            nome TEXT,
            idade INT,
            distrito TEXT,
            equipa TEXT);
        """)

        self.conn.commit()

    def cadastro_adepto(self, nome, idade, distrito, equipa):
        self.cursor.execute('INSERT INTO adeptos (nome, idade, distrito, equipa) VALUES (?, ?, ?, ?)',
                            (nome, idade, distrito, equipa))
                   
        self.conn.commit()

    def export_csv(self, filename):

        self.cursor.execute("""
        SELECT * FROM adeptos
        """)

        adeptos = self.cursor.fetchall()

        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            csv_writer.writerow(['Nome', 'Idade', 'Distrito', 'Equipa'])

            for row in adeptos:
                csv_writer.writerow(row)

    def get_dados_para_grafico(self):
        self.cursor.execute("""
        SELECT equipa, distrito, COUNT(*) as quantidade, AVG(idade) as media_idade
        FROM adeptos GROUP BY equipa, distrito
        """)
        dados = self.cursor.fetchall()
        return dados   
    
    def fechar_conexao(self):
        self.conn.close()