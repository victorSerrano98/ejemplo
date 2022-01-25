import time
from time import sleep
import streamlit
import streamlit as st
import pandas as pd

import Tesis1

### Encabezado ###
st.set_page_config(page_title="Chatbot Covid-19")
st.markdown('___')
st.markdown("<h4 style='text-align: center; color:grey;'>Universidad Nacional de Loja</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color:grey;'>Ingeniería en Sistemas</h4>", unsafe_allow_html=True)
st.markdown(
    "<h1 style='text-align: center; color:Black;frameborder=1;'>""Agente virtual para brindar asistencia acerca del Covid-19""</h1>",
    unsafe_allow_html=True)
# ![Star (https://unl.edu.ec/sites/default/files/inline-images/logo_0.png?style=social)](https://unl.edu.ec/)

st.markdown('___')


######

def classify(num):
    if num == 0:
        return 'setosa'
    else:
        return 'virginica'


def main():
    # st.title('Agente Virtual (Covid-19):')
    # st.sidebar.header('Universidad Nacional de Loja')

    def parametros():
        pregunta = st.text_input('Ingrese su pregunta sobre el Covid-19:')

        return pregunta

    consultaAvanz = st.checkbox('Consulta Avanzada')

    pregunta = parametros()
    if st.button('Enviar pregunta'):
        traducido = Tesis1.traductor(pregunta)
        print(traducido)
        query = Tesis1.spa(traducido)
        print(query)
        articulos = Tesis1.consultaAPI(query, 0)
        # print(articulos)
        cont = 0
        cont2 = 2
        contadorr = 0
        cont_Resp = 0
        almacenamiento = ""

        # CONSULTA AVANZADA CHECK
        if consultaAvanz:
            print("funciona el check")

            while cont < 3 and cont2 < 3:
                articulos = Tesis1.consultaAPI(query, cont2)
                print("Tamaño: ", len(articulos["data"]))
                # print(articulos)
                if articulos == None:
                    streamlit.error("No se encontraron respuestas relacionadas." + "\n\n Reformula tu pregunta.")
                    break
                with st.spinner('Búscando una respuesta a su pregunta..'):
                    time.sleep(15)
                respuesta, cc = Tesis1.respuesta(traducido, articulos)
                cont = cont + cc
                cont2 = cont2 + 1
                print("contador", cont)
                print("contador2", cont2)
                almacenamiento = almacenamiento + respuesta
                if len(respuesta) > 1:
                    print("XXXXXXXXXXX: ", contadorr)
                    cont_Resp = cont_Resp + 1
            if len(almacenamiento) > 1:
                st.success(almacenamiento)
            else:
                streamlit.error("No se encontraron respuestas relacionadas." + "\n\n Reformula tu pregunta.")

        else:
            while cont < 4 and cont2 < 3:
                articulos = Tesis1.consultaAPI(query, cont2)
                contadorr = len(articulos["data"]) + contadorr
                print("Tamaño: ", len(articulos["data"]))
                if articulos == None:
                    streamlit.error("No se encontraron respuestas relacionadas." + "\n\n Reformula tu pregunta.")
                    break
                with st.spinner('Búscando una respuesta a su pregunta..'):
                    time.sleep(10)
                respuesta, cc = Tesis1.respuesta(traducido, articulos)
                almacenamiento = almacenamiento + respuesta
                cont = cont + cc
                cont2 = cont2 + 1
                print("contador", cont)
                print("contador2", cont2)
            if len(almacenamiento) > 1:
                print("XXXXXXXXXXX: ",contadorr)
                st.success(almacenamiento)
            else:
                streamlit.error("No se encontraron respuestas relacionadas." + "\n\n Reformula tu pregunta.")
                streamlit.error('Si no obtuvo una respuesta acorde, pruebe la \"Consulta Avanzada\"')

    st.markdown('___')

if __name__ == '__main__':
    main()
