from flask import Flask, render_template, request
import os
import sys


print(os.getcwd())

app=Flask(__name__, static_folder='./static')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



@app.route('/introduction', methods = ['post'])
def introduction():
    if request.method == 'POST':

        topic = "xxx"
        domain = "xxx"

        #content.append(domain)


        # querying gpt3
        query = topic # + " (" + domain + ")"
        quest=f"What is "  + "?" 
        what = "Natural language processing (NLP) is a subfield of linguistics, computer science, information engineering, and artificial intelligence concerned with the interactions between computers and human (natural) languages, in particular how to program computers to process and analyze large amounts of natural language data."
        #what = str(ask(quest, openai_key)).strip()


        quest=f"What topics are related to "  + "?" 
        what_topics = "Some topics that are related to NLP include: -How to process and analyze text data -How to extract meaning from text -How to generate text -How to build chatbots -How to build language models -How to do sentiment analysis -How to do topic modeling -How to do text classification" 
        #what_topics = str(ask(quest, openai_key)).strip()

        quest=f"What are the latest developments of " + "?"
        latest = "Some of the latest developments in the field of NLP include: - the use of deep learning for NLP tasks - the use of reinforcement learning for NLP tasks - the use of transfer learning for NLP tasks - the use of natural language processing for predictive maintenance"
        #latest = str(ask(quest, openai_key)).strip()




if __name__ == "__main__":
    app.debug=True 
    app.run()