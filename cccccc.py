import json
datoss = []
with open('datosEntrenamiento.json') as file:
    data = json.load(file)
cont=0
for datos in data:
    print(datos)
    mensaje5 = datos['abstract'].lower()
    x = datos['answer'].lower()
    datoss.append({
        'title': datos['title'],
        'question': datos['question'],
        'answer': {
            "text": datos['answer'],
            "answer_start": mensaje5.find(x),
        },
        'context': datos['abstract']})

print(cont)
with open('data.json', 'w') as file:
    json.dump(datoss, file, indent=4)