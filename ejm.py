import time
from time import sleep
import streamlit
import streamlit as st
import pandas as pd

import Tesis1

### Encabezado ###
st.set_page_config(page_title="Chatbot Covid-19")
st.markdown('_')
st.markdown("<h4 style='text-align: center; color:grey;'>Universidad Nacional de Loja</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color:grey;'>Ingeniería en Sistemas</h4>", unsafe_allow_html=True)
st.markdown(
    "<h1 style='text-align: center; color:Black;frameborder=1;'>""Agente virtual para brindar asistencia acerca del Covid-19""</h1>",
    unsafe_allow_html=True)
# [![Star](https://unl.edu.ec/sites/default/files/inline-images/logo_0.png?style=social)](https://unl.edu.ec/)

st.markdown('_')


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
        cont2 = 0
        cont_Resp = 0
        almacenamiento = ""

        # CONSULTA AVANZADA CHECK
        if consultaAvanz:
            print("funciona el check")

            while cont > 1:
                if cont2 > 20:
                        break
                articulos = Tesis1.consultaAPI(query, cont2)
                print("Tamaño: ", len(articulos))
                # print(articulos)
                if articulos == None:
                    if len(almacenamiento) > 1:
                        st.success(almacenamiento)
                        break
                    else:
                        streamlit.error("No se encontraron respuestas relacionadas." + "\n\n Reformula tu pregunta.")
                        break
                with st.spinner('Búscando una respuesta a su pregunta..'):
                    time.sleep(15)
                respuesta, c = Tesis1.respuesta(traducido, articulos)
                cont = cont + c
                cont2 = cont2 + 1
                print("contador2", cont2)
                almacenamiento = almacenamiento + respuesta
                if len(respuesta) > 1:
                    cont_Resp = cont_Resp + 1
            if len(almacenamiento) > 1:
                st.success(almacenamiento)
            else:
                streamlit.error("No se encontraron respuestas relacionadas." + "\n\n Reformula tu pregunta.")

        else:
            while cont == 0:
                if cont2 >50:
                    break
                articulos = Tesis1.consultaAPI(query, cont2)
                print("Tamaño: ", len(articulos))
                # print(articulos)

                if articulos == None:
                    streamlit.error("No se encontraron respuestas relacionadas." + "\n\n Reformula tu pregunta.")
                    break
                with st.spinner('Búscando una respuesta a su pregunta..'):
                    time.sleep(15)
                respuesta, c = Tesis1.respuesta(traducido, articulos)
                cont2 = cont2 + 1
                cont = cont + c
                print("contador2", cont2)
                almacenamiento = almacenamiento + respuesta
                if len(respuesta) > 1:
                    cont_Resp = cont_Resp + 1
            if len(almacenamiento) > 1:
                st.success(almacenamiento)
            else:
                streamlit.error("No se encontraron respuestas relacionadas." + "\n\n Reformula tu pregunta.")
                streamlit.error('Si no obtuvo una respuesta acorde, pruebe la \"Consulta Avanzada\"')

    st.markdown('_')


if _name_ == '_main_':
    main()