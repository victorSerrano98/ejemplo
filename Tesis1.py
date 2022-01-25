import spacy
import requests
import torch
from transformers import pipeline
from googletrans import Translator
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, BertForQuestionAnswering, BertConfig

#CARGA DE MODELO AJUSTADO
modelname = 'twmkn9/bert-base-uncased-squad2'
model = BertForQuestionAnswering.from_pretrained(modelname)
tokenizer = AutoTokenizer.from_pretrained(modelname)
# tokenizer = AutoTokenizer.from_pretrained("graviraja/covidbert_squad")
# model = AutoModelForQuestionAnswering.from_pretrained("graviraja/covidbert_squad")
# config = BertConfig.from_json_file('C:/Users/Alexis/PycharmProjects/ModeloBERT/model/config.json')
# tokenizer = AutoTokenizer.from_pretrained("C:/Users/Alexis/PycharmProjects/ModeloBERT/model/tokenizer/")
# model = AutoModelForQuestionAnswering.from_pretrained("C:/Users/Alexis/PycharmProjects/ModeloBERT/model")

#https://huggingface.co/twmkn9/bert-base-uncased-squad2
#PARAMETROS DE LAS PREGUNTAS Y CONTEXTO QUE ABARCARA
max_length = 512 # The maximum length of a feature (question and context)
#doc_stride = 128 # The authorized overlap between two part of the context when splitting it is needed.

#question_answerer = pipeline("question-answering")
nlp = pipeline("question-answering", model=model, tokenizer=tokenizer)
nlpPipe = pipeline("question-answering")
# question = "¿Cuánto tiempo tardan en aparecer los síntomas del covid-19?"
def traductor(question):
    translator = Translator()
    translation = translator.translate(question, dest='en')
    question = translation.text
    return question

def spa(question):
    nlpSp = spacy.load("en_core_web_sm")
    preguntaFormt = " ".join(question.split())
    query = ""
    print(preguntaFormt)
    doc = nlpSp(preguntaFormt)
    a = [token.dep_ for token in doc]
    print("Estructura Frase: ", a)

    # Create list of word tokens
    token_list = []
    for token in doc:
        token_list.append(token.text)
    # Create list of word tokens after removing stopwords
    filtered_sentence = []

    for word in token_list:
        lexeme = nlpSp.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence.append(word)
    #print(token_list)
    #print(filtered_sentence)
    query = filtered_sentence

    my_stopwords = ['?', '¿', '!', 'covid-19', 'covid', 'coronavirus', 'COVID-19', 'COVID19', 'covid19' 'SARS-COV2', 'SARS-COV 2', 'sarscov2', 'sars cov 2']
    tokens_filtered = [word for word in query if not word in my_stopwords]
    #print("111: ", tokens_filtered)
    query = tokens_filtered
    var = ""
    for i in query:
        var = var + " " + "\"" + i + "\""
        #print(var)

    var = var + " \"covid-19\""
    var = " ".join(var.split())
    print("formateada: ", var)
    return var

def consultaAPI(query, num):
    data = {
        "query": query,
        "offset": num*50,
        "limit": 50,
        "fields": "title,abstract,url,year"

    }
    r = requests.get('https://api.semanticscholar.org/graph/v1/paper/search', params=data).json()
    # print("r::::", r)
    try:
        if r['message']:
            print("Heyyyyyyy")
            return None
    except:
        output_dict = [x for x in r["data"] if x['year'] == 2021]
        #print(output_dict)

        return r

def sp_Abstract(abstract):
    nlpAbst = spacy.load("en_core_web_sm")
    preguntaFormt = " ".join(abstract.split())
    query = ""
    print(preguntaFormt)
    doc = nlpAbst(preguntaFormt)
    a = [token.dep_ for token in doc]
    #print("Estructura Frase: ", a)

    # Create list of word tokens
    token_list = []
    for token in doc:
        token_list.append(token.text)
    # Create list of word tokens after removing stopwords
    filtered_sentence = []

    for word in token_list:
        lexeme = nlpAbst.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence.append(word)
    #print(token_list)
    #print(filtered_sentence)
    query = filtered_sentence

    my_stopwords = ['?', '¿', '!', '\n']
    tokens_filtered = [word for word in query if not word in my_stopwords]
    #print("111: ", tokens_filtered)
    query = tokens_filtered
    var = ""
    for i in query:
        var = var + " " + i + " "

    # print("RESUMEN CORREGIDO: ", var)
    return var


def respuesta(question,text):
    list = ""
    cont = 0
    contArtc = 0
    contArtcTotal = 0
    for res in text['data']:
        contArtcTotal = contArtcTotal + 1
        try:
            abstracCrrg = res["abstract"]
            result = nlp(question=question, context=abstracCrrg)
            rest = nlpPipe(question=question, context=abstracCrrg)
            x = (round(rest['score'], 4))

            # TOKENIZADOR DE LA PREGUNTA PARA OBTENER RESPUESTA ACORDE
            inputs = tokenizer.encode_plus(question, abstracCrrg,
                                           add_special_tokens=True,  # Add '[CLS]' and '[SEP]'
                                           truncation=True,
                                           max_length=512,
                                           return_tensors='pt')  # Return pytorch tensors.
            #nlp({'question': question, 'context': res["abstract"]})
            print(res["title"])
            if x > 0.90:
                cont = cont + 1

                #print(res["abstract"])
                # print(result['answer'])
                # translator = Translator()
                # translation = translator.translate(result['answer'], dest='es')
                # resp = translation.text
                # print(res["abstract"])
                titulo = res["title"]
                # print(resp +str(round(result['score'], 4)))
                print(x)

                input_ids = inputs["input_ids"].tolist()[0]
                text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
                answer_start_scores, answer_end_scores = model(**inputs, return_dict=False)
                answer_start = torch.argmax(answer_start_scores)
                answer_end = torch.argmax(answer_end_scores) + 1
                answer = tokenizer.convert_tokens_to_string(
                    tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
                translator = Translator()
                if answer:
                    if '[CLS]' in answer:
                        translation = translator.translate(result['answer'], dest='es')
                    else:
                        translation = translator.translate(answer, dest='es')
                    respTraducida = translation.text
                else:
                    translation = translator.translate(result['answer'], dest='es')
                    respTraducida = translation.text
                print(f"Question: {question}")
                print(f"Answer: {answer}\n")
                list =  list + "Respuesta: " + respTraducida + "\n \n Fuente: " + titulo + "\n \n" + "Score: " + str(x) + "\n \n"
                #print(res["abstract"])
                print("QA: ", result['answer'])

        except:
            print("Error")
        if contArtc == 9:
            contArtc = 0
            if cont > 10:
                break
        contArtc = contArtc + 1
    print("Art. Totales: ", contArtcTotal)
    return list, cont