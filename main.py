#import principal
import streamlit as st
#imports relacionados
from PIL import Image
import pytesseract
#metodos internos
import functions.functions as fc

class OCR:

    def __init__(self):
        # titolo della pagina
        st.set_page_config(page_title="Python OCR")
        # inizializza variabili
        self.texto = ""
        self.analisar_texto = False

    def inicial(self):
        # contenuto iniziale della pagina
        st.title("OCR per estrarre testi da immagini")
        st.write("Forked by: https://github.com/guilhermedonizetti/OCR_Python")
        st.write("Optical Character Recognition (OCR) in Python")
        imagem = st.file_uploader("Seleziona un'immagine", type=["png","jpg"])
        # se selezioni un'immagine
        if imagem:
            img = Image.open(imagem)
            st.image(img, width=350)
            st.info("Texto extraído")
            self.texto = self.extrair_texto(img)
            st.write("{}".format(self.texto))
            
            # Opzione analisi del testo
            self.analisar_texto = st.sidebar.checkbox("Analisar texto")
            if self.analisar_texto==True:
                self.mostrar_analise()
    
    def extrair_texto(self, img):
        # Comando che estrae testo dalle immagini con Tesseract
        texto = pytesseract.image_to_string(img, lang="ita")
        return texto
    
    def mostrar_analise(self):
        #busca CPF, datas e palavras boas e mas na extracao
        # DA CAMBIARE: usare Spacy per analisi del testo
        cpf = fc.buscar_cpf(self.texto)
        datas = fc.buscar_data(self.texto)
        p_boas, percentual_bom = fc.buscar_palavras_boas(self.texto)
        p_mas, percentual_mau = fc.buscar_palavras_mas(self.texto)
        
        if cpf==None:
            st.warning("Nessuna voce di autorità trovata.")
        else:
            cpf = fc.sumarizar_cpf(cpf)
            st.success("Voci di autorità estratte:")
            st.write(cpf)

        if datas==None:
            st.warning("Nessuna data trovata.")
        else:
            datas = fc.sumarizar_datas(datas)
            st.success("Date estratte:")
            st.write(datas)
        
        if p_boas==0:
        # TO-DO: togliere?
            st.warning("Não identificado palavras de bem.")
        else:
            st.success("Palavras de bem:")
            st.write("{} palavra(s). Representam das palavras do texto: {:.2f}%".format(p_boas, percentual_bom))
        
        if p_mas==0:
            st.warning("Não identificado palavras más.")
        else:
            st.success("Palavras más:")
            st.write("{} palavra(s). Representam das palavras do texto: {:.2f}%".format(p_mas, percentual_mau))

ocr = OCR()
ocr.inicial()