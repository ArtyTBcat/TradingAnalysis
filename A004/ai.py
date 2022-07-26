import openai
import pyttsx3
openai.api_key = "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"

# list engines
engine = pyttsx3.init()
engines = openai.Engine.list()

# print the first engine's id
print(engines.data[0].id)

# create a completion
completion = openai.Completion.create(engine="ada", prompt="Hello?")

# print the completion
engine.say(completion.choices[0].text)
engine.runAndWait()
print(completion.choices[0].text)

while True:
    inp = input(">  ")
    completion = openai.Completion.create(engine="ada", prompt=inp)
    respond = inp + completion.choices[0].text
    
    engine.say(respond)
    print(respond, "\n")
    engine.runAndWait()
    