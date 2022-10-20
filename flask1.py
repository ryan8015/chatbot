from flask import Flask, redirect, render_template, request, url_for
import os
import openai

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


path="/tmp"
os.chdir(path)


with open("/prompt.txt", "w") as f:
    f.write("The following is a conversation is with an AI called Sarah, she is very nice, funny and will laugh at anything")


@app.route("/gen", methods=("GET", "POST"))
def generate_per():
    if request.method=="POST":
        personality = request.form["personality"]
        with open("prompt.txt", "w") as f:
            str(f.write(personality))
        
        return redirect(url_for("generate_per", personality=personality))

    result = request.args.get("personality")
    return render_template("index.html", result=result)

@app.route("/", methods=("GET", "POST"))

def index():
    if request.method=="POST":
        with open("prompt.txt","r") as f:
            prompt=f.read()
        bot = request.form["bot"]
        start_sequence = "\nAI:"
        restart_sequence = "\nHuman: "
        ai=10
        if bot=="stop":
            return "Thank You"
        prompt=str(prompt) + "\nHuman: " + str(bot) + "\nAI:"
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0.9,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0.3,
            presence_penalty=0.8,
            stop=[" Human:", " AI:"]
        )
        answer = str(response["choices"][0]["text"])
        prompt=str(prompt) + answer
        with open("prompt.txt", "w") as f:
            f.write(prompt)
        print("AI:" + answer)
        return redirect(url_for("index", result="AI: " + answer))

    result = request.args.get("result")
    return render_template("index.html", result=result)


app.run(host="0.0.0.0",port=80)
