import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        context = request.form["context"]
        question = request.form["question"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(context, question),
            temperature=0,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=[" END"]
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)

def generate_prompt(context, question):
    return """Based on this context {}, answer the following question.
Question: {}
Answer:""".format(context, question)
