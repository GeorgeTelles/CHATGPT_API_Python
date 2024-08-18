# Importando Bibliotecas

from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import os

# Initialize the API key

api_key = "xyz"

# Definindo funções

def gerar_resposta(messages):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].message['content'], response['usage']]

def talk(text):
    engine.say(text)
    engine.runAndWait()

def save_file(data):
    with open(os.path.join(path, filename), "wb") as f:
        f.write(data)
        f.flush()

# Configurações e variaveis

# Inicial Config
messages = [{"role": "system", "content": "Você é um assistente gente boa."}]

r = sr.Recognizer()
mic = sr.Microphone()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('rate', 220)

voice_index = 0
engine.setProperty('voice', voices[voice_index].id)

path = os.getcwd()
filename = "audio.wav"

#Inicializando o CHAT GPT
print("Escolha uma opção:")
print("1. Digitar")
print("2. Falar")

opcao = input("Opção: ")

if opcao == "1":
    entrada_por_texto = True
else:
    entrada_por_texto = False

ajustar_ambiente_noise = True

while True:
    question = ""

    if entrada_por_texto:
        question = input("Perguntar pro ChatGPT: ")
    else:
        with mic as source:
            if ajustar_ambiente_noise:
                r.adjust_for_ambient_noise(source)
                ajustar_ambiente_noise = False
            print("Fale alguma coisa")
            audio = r.listen(source)
            print("Enviando para reconhecimento")

            question = r.recognize_google(audio, language="pt-BR")

    if question == "":
        print("Nenhum som detectado.")
        continue

    print("Você:", question)
    messages.append({"role": "user", "content": question})

    answer = gerar_resposta(messages)

    print("ChatGPT:", answer[0])

    messages.append({"role": "assistant", "content": answer[0]})

    talk(answer[0])

    print("Opções:")
    print("1. Continuar")
    print("2. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "2":
        print("Encerrando.")
        talk("Desligando")
        break

print("Até logo!")
