import matplotlib.pyplot as plt
import csv

import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager

#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from garden_matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

periodo = '2023'
#url = 'https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top_10_empresas_2021.csv'


def leer_csv_from_github(file):
    response = requests.get(file)
    if response.status_code == 200:
        datos = list(csv.reader(response.text.splitlines()))
        return datos
    else:
        return []

contratos_2023 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top10_2023.csv')
contratos_2022 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top10_2022.csv')
contratos_2021 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top10_2021.csv')
contratos_30 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top10_30.csv')



empresas_2023 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top_10_empresas_2023.csv')
empresas_2022 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top_10_empresas_2022.csv')
empresas_2021 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top_10_empresas_2021.csv')
empresas_30 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top_10_empresas_30.csv')



instituciones_2023 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top_10_instituciones_2023.csv')
instituciones_2022 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top_10_instituciones_2022.csv')
instituciones_2021 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top_10_instituciones_2021.csv')
instituciones_30 = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top_10_instituciones_30.csv')


top100alfa = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/top100alfabetica.csv')
listatop100 = top100alfa[0]
las100empresas= leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/las100empresas.csv')

resumen = leer_csv_from_github('https://raw.githubusercontent.com/adolforosas/kivy-arsemed/main/resumenes.csv')


#leer_csv_from_github(url)


def calcula_contratos(periodo):
    if periodo == '2021':
        contratos = contratos_2021
    elif periodo == '2022':
        contratos = contratos_2022
    elif periodo =='30 Dias':
        contratos = contratos_30
    else:
        contratos = contratos_2023

    return contratos

def calcula_empresas(periodo):
    if periodo == '2021':
        top_10_empresas = empresas_2021
    elif periodo =='30 Dias':
        top_10_empresas = empresas_30
    elif periodo == '2022':
        top_10_empresas = empresas_2022
    else:
        top_10_empresas = empresas_2023

    return top_10_empresas


def calcula_instituciones(periodo):
    if periodo == '2021':
        top_10_instituciones = instituciones_2021
    elif periodo =='30 Dias':
        top_10_instituciones = instituciones_30
    elif periodo == '2022':
        top_10_instituciones = instituciones_2022
    else:
        top_10_instituciones = instituciones_2023

    return top_10_instituciones



def calcula_resumen(periodo):
    #resumenes = resumen
    if periodo == '2021':
        return resumen[2]
    elif periodo == '2022':
        return resumen[1]
    elif periodo == '30 Dias':
        return resumen[3]
    else:
        return resumen[0]


#calcula_resumen(periodo='periodo')


class Interface(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.entrada1.text = "Total Contratado \n " + resumen[0][0]
        self.ids.entrada2.text = "Contratos \n " + resumen[0][1]
        self.ids.entrada3.text = "Empresas \n " + resumen[0][2]
        self.ids.entrada4.text = "Instituciones \n " + resumen[0][3]
        self.grafica_institucion()
        self.grafica_empresa()
        self.display_info(periodo)
        self.display_screen2()
        self.muestra_resultados(proveedor='GE SISTEMAS MEDICOS DE MEXICO SA DE CV')
        self.ids.emp_sel.text = 'GE SISTEMAS MEDICOS DE MEXICO SA DE CV   (Montos en millones de pesos)'


    def switching_back(self):
        self.transition.duration = 0.5
        self.current = "Main Screen"
        self.transition.direction = "right"

    def switching(self):
        print(self.current_screen)
        self.transition.duration = 0.5
        self.transition.direction = "left"
        self.current = "Profile"
        print(self.current_screen)

    def actualizar_textos(self,periodo):
        self.resumen = calcula_resumen(periodo=periodo)
        self.ids.etiqueta2.text = str(periodo)
        self.ids.entrada1.text = "Total Contratado \n " + self.resumen[0]
        self.ids.entrada2.text = "Contratos \n " + self.resumen[1]
        self.ids.entrada3.text = "Empresas \n " + self.resumen[2]
        self.ids.entrada4.text = "Instituciones \n " + self.resumen[3]
        self.grafica_institucion()
        self.grafica_empresa()
        self.display_info(periodo)


    def muestra_resultados(self, proveedor):
        print(f"Botón presionado: {proveedor}")
        self.ids.emp_sel.text = f'{proveedor}   (Montos en millones de pesos)'
        # Lista para almacenar todas las filas que cumplen con la condición
        filas_coincidentes = []

        # Recorrer la lista y buscar por el nombre
        for fila in las100empresas:
            if fila and fila[0] == proveedor:
                filas_coincidentes.append(fila)

        # Imprimir todas las filas que cumplen con la condición
        for fila in filas_coincidentes:
            print(fila)

        tabla = GridLayout(cols=6, spacing=2, size_hint_y=None)

        tabla.add_widget(Label(text='Año', font_size=27, halign='center', text_size=(70, None)))
        tabla.add_widget(Label(text='Ranking', font_size=27, halign='center', text_size=(110, None)))
        tabla.add_widget(Label(text='Contratos', font_size=27, halign='center', text_size=(120, None)))
        tabla.add_widget(Label(text='Servicios', font_size=27, halign='center', text_size=(160, None)))
        tabla.add_widget(Label(text='Equipo', font_size=27, halign='center', text_size=(160, None)))
        tabla.add_widget(Label(text='Monto Total', font_size=27, halign='center', text_size=(160, None)))

        for fila in filas_coincidentes:
            Año = fila[1]
            Ranking = fila[2]
            Contratos = fila[3]
            Servicio = fila[4]
            Equipo = fila[5]
            Monto = fila[6]
            button = Button(
                text=Año,
                background_normal='',
                background_color=[31/256, 44/256, 86/256, 1],
                font_size=27,
                halign='center',
                text_size=(70, None)  # Ajusta el ancho
            )
            tabla.add_widget(button)
            button = Button(
                text=Ranking,
                background_normal='',
                background_color=[31/256, 44/256, 86/256, 1],
                font_size=27,
                halign='center',
                text_size=(110, None)  # Ajusta el ancho (200) y deja la altura como None
            )
            tabla.add_widget(button)

            button = Button(
                text=Contratos,
                background_normal='',
                background_color=[31/256, 44/256, 86/256, 1],
                font_size=27,
                halign='center',
                text_size=(120, None)  # Ajusta el ancho (200) y deja la altura como None
            )
            tabla.add_widget(button)

            importe_millones = float(Servicio) / 1000000  # Convierte a millones
            importe_formateado = "${:,.2f} ".format(importe_millones)  # Formatea el monto
            button = Button(
                text=importe_formateado,
                background_normal='',
                background_color=[31/256, 44/256, 86/256, 1],
                font_size=27,
                halign='center',
                text_size=(160, None)  # Ajusta el ancho (200) y deja la altura como None
            )
            tabla.add_widget(button)

            importe_millones = float(Equipo) / 1000000  # Convierte a millones
            importe_formateado = "${:,.2f} ".format(importe_millones)  # Formatea el monto
            button = Button(
                text=importe_formateado,
                background_normal='',
                background_color=[31/256, 44/256, 86/256, 1],
                font_size=27,
                halign='center',
                text_size=(160, None)  # Ajusta el ancho (200) y deja la altura como None
            )
            tabla.add_widget(button)

            importe_millones = float(Monto) / 1000000  # Convierte a millones
            importe_formateado = "${:,.2f} ".format(importe_millones)  # Formatea el monto
            button = Button(
                text=importe_formateado,
                background_normal='',
                background_color=[31/256, 44/256, 86/256, 1],
                font_size=27,
                halign='center',
                text_size=(160, None)  # Ajusta el ancho (200) y deja la altura como None
            )
            tabla.add_widget(button)

        #tabla.size_hint_y = None
        tabla.height = 160  # Ajusta el valor según tus necesidades

        self.ids.resultados.clear_widgets()  # Borra cualquier tabla anterior
        self.ids.resultados.add_widget(tabla)  # Agrega la nueva tabla

    def display_info(self,periodo):
        contratos = calcula_contratos(periodo=periodo)
        #dfk = df[df['año'] == int(self.ids.etiqueta2.text)]
        tabla = GridLayout(cols=4, spacing=2, row_default_height=74, size_hint_y=None)
        tabla.bind(minimum_height=tabla.setter('height'))
        tabla.cols_minimum = {0: 150, 1: 400, 2: 150, 3: 180}
        tabla.add_widget(Label(text='Institución', font_size=28, text_size=(150, None)))
        tabla.add_widget(Label(text='Proveedor', font_size=28, halign='center', text_size=(400, None)))
        tabla.add_widget(Label(text='Importe', font_size=28, halign='center', text_size=(150, None)))
        tabla.add_widget(Label(text='Producto', font_size=28, halign='center', text_size=(180, None)))

        for fila in contratos:
            institucion = fila[0]
            proveedor = fila[1]
            monto = fila[2]
            producto = fila[3]
            button = Button(
                text=institucion,
                background_normal='',
                background_color=[73/255, 116/255, 165/255, 1],
                font_size=24,
                halign='center',
                text_size=(150, None)  # Ajusta el ancho
            )

            tabla.add_widget(button)
            button = Button(
                text=proveedor,
                background_normal='',
                background_color=[73 / 255, 116 / 255, 165 / 255, 1],
                font_size=24,
                halign='center',
                text_size=(400, None)  # Ajusta el ancho (200) y deja la altura como None
            )
            tabla.add_widget(button)


            importe_millones = float(monto) / 1000000  # Convierte a millones
            importe_formateado = "${:,.2f} M".format(importe_millones)  # Formatea el monto
            button = Button(
                text=importe_formateado,
                background_normal= '',
                background_color= [73/255, 116/255, 165/255, 1],
                font_size=24,
                halign='center',
                text_size=(150, None)  # Ajusta el ancho (200) y deja la altura como None
            )
            tabla.add_widget(button)

            button = Button(
                text=producto,
                background_normal='',
                background_color=[73 / 255, 116 / 255, 165 / 255, 1],
                font_size=24,
                halign='center',
                text_size=(180, None)  # Ajusta el ancho (200) y deja la altura como None
            )
            tabla.add_widget(button)

        self.ids.tabla_contratos.clear_widgets()  # Borra cualquier tabla anterior
        self.ids.tabla_contratos.add_widget(tabla)  # Agrega la nueva tabla

    def display_screen2(self):
        tabla = GridLayout(cols=3, spacing=3, row_default_height=92, size_hint_y=None)
        tabla.bind(minimum_height=tabla.setter('height'))

        for proveedor in listatop100:
            boton = Button(
                text=proveedor,
                font_size=22,
                halign='center',
                background_normal='',
                background_color=[25 / 255, 36 / 255, 68 / 255, 1],
                color=(1, 0.647, 0, 1),
                text_size=(240, None)
            )
            boton.bind(on_press=lambda instance, proveedor=proveedor: self.muestra_resultados(proveedor))
            tabla.add_widget(boton)

        self.ids.empresas.clear_widgets()  # Borra cualquier tabla anterior
        self.ids.empresas.add_widget(tabla)  # Agrega la nueva tabla

    def grafica_institucion(self):
        periodo = self.ids.etiqueta2.text
        top_10_instituciones2 = calcula_instituciones(periodo)
        data = top_10_instituciones2
        importes = [float(row[1].replace(',', '')) for row in data[1:]]
        instituciones = [row[0] for row in data[1:]]
        fig_instituciones, ax_instituciones = plt.subplots(figsize=(10.4, 4),facecolor='#192444',dpi=100)
        ax_instituciones.set_facecolor('#182243')


        bars = ax_instituciones.barh(instituciones, importes, color='#4974A5')
        for bar, valor in zip(bars, importes):
            ax_instituciones.text(valor * 1.01, bar.get_y() + bar.get_height() / 2, "${:,.0f}".format(valor / 1e6),
                                  va='center', color='white',fontsize=18)
        ax_instituciones.set_yticklabels(['      ' + label for label in instituciones])
        ax_instituciones.tick_params(axis='y', labelcolor='white',labelsize=18)  # Cambiar el color de las etiquetas del eje y a lightcyan
        ax_instituciones.tick_params(axis='x', colors='white')
        ax_instituciones.set_xticks([])

        #ax_instituciones.set_xlim(right=-0)


        plt.tick_params(labelbottom=False, bottom=False)
        title = ax_instituciones.set_title('Instituciones con mas compras (Millones)',
                                   color='white',fontsize=18)
        title.set_position([.48, .95])  # Ajusta las coordenadas [x, y]
        #plt.subplots_adjust(left=0.05, right=1, top=0.95, bottom=0.05)
        plt.margins(0.30, .07)
        plt.tight_layout(pad=0.08)
        for spine in ['top', 'right', 'left', 'bottom']:
            ax_instituciones.spines[spine].set_visible(False)
        self.ids.grafica.clear_widgets()
        self.ids.grafica.add_widget(FigureCanvasKivyAgg(plt.gcf()))


    def grafica_empresa(self):
        periodo = self.ids.etiqueta2.text
        top_10_empresas = calcula_empresas(periodo)
        data = top_10_empresas
        importes = [float(row[1].replace(',', '')) for row in data[1:]]
        empresas = [row[0] for row in data[1:]]
        fig_empresas, ax_empresas = plt.subplots(figsize=(4.5, 4,), facecolor='#192444', dpi=100)
        ax_empresas.set_facecolor('#192444')

        #inicio_barras = [18] * len(importes)  # Ajusta la posición inicial aquí
        # Crea la gráfica de barras utilizando los datos de top_10_empresas y la posición inicial ajustada
        bars = ax_empresas.barh(empresas, importes, left=8, color='#4974A5')

        #bars = ax_empresas.barh(empresas, importes, color='#ffa500')
        #for bar, valor in zip(bars, importes):
        #    ax_empresas.text(valor +15, bar.get_y() + bar.get_height() / 2, "${:,.0f}".format(valor),
        #                          va='center', color='lightcyan',fontsize=18)

        for bar, valor in zip(bars, importes):
            valor_x = max(importes) * 1.3  # Alinea los valores con el mayor valor
            ax_empresas.text(valor_x, bar.get_y() + bar.get_height() / 2, "${:,.0f}".format(valor),
                             va='center', ha='right', color='white', fontsize=18)

        #for i, bar in enumerate(reversed(bars)):
         #   ax_empresas.text(-20, bar.get_y() + bar.get_height() / 2, str(i + 1) +'', va='center', color='white')

        ax_empresas.set_yticklabels(['    ' + label for label in empresas])
        title = ax_empresas.set_title('Empresas con mas Ventas (Millones)',
                                           color='lightcyan', fontsize=18)
        title.set_position([.48, .95])  # Ajusta las coordenadas [x, y]
        plt.margins(0.30, .07)
        ax_empresas.tick_params(axis='y',labelcolor='white')  # Cambiar el color de las etiquetas del eje y a lightcyan
        ax_empresas.tick_params(axis='x', colors='white')
        plt.tick_params(labelbottom=False, bottom=False)
        plt.yticks(rotation=0, ha='left')

        # plt.margins(0.20, 0.20)
        plt.tight_layout(pad=0.08)
        # Establece el límite inferior del eje x en cero
        ax_empresas.set_xlim(left=0)
        ax_empresas.tick_params(axis='y', labelsize=18)  # Ajusta el tamaño (8 es un ejemplo)

        for spine in ['top', 'right', 'left', 'bottom']:
            ax_empresas.spines[spine].set_visible(False)
        self.ids.grafica2.clear_widgets()
        self.ids.grafica2.add_widget(FigureCanvasKivyAgg(plt.gcf()))


class DashboardApp(App):
    def build(self):
        return Interface()



if __name__ == '__main__':
    DashboardApp().run()

