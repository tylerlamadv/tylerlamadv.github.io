# --------------------------------------------
# C++ to Java Test Method Converter
# --------------------------------------------
# Make sure the following libraries are installed:
# flask, openai, openpyxl, matplotlib, pandas, plotly, scikit-learn, scipy, tenacity, tiktoken
# To install a library, inside your terminal, run: pip install {library_name}
# --------------------------------------------
# Create an account with OpenAI to create an API key
# Follow these instructions to set your API key 
# https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety
# --------------------------------------------
# Paste this link into your browser once script is running: http://127.0.0.1:5000


# imports
from flask import Flask, render_template, request
import openai
from openai.embeddings_utils import get_embedding
import os
import pandas as pd
import tiktoken

# API key
openai.api_key = os.environ['OPENAI_API_KEY']

# completions model
GPT_MODEL = 'text-davinci-003'

# encoding
gpt_encoding = tiktoken.encoding_for_model(GPT_MODEL)

MAX_TOKENS = 500
TEMPERATURE = 0

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])  
def main():
    input_ = '' 
    output_ = ''
    # when convert button is pressed
    if request.method == 'POST':
        input_ = request.form.get('textarea_input')
        if input_ != '':
            num_tokens = len(gpt_encoding.encode(input_))
            if num_tokens < MAX_TOKENS:
                    prompt = f'''Translate the C++ code to Java code.
                    C++ code:
                    {input_}
                    
                    Java code:
                    '''
                    response = openai.Completion.create(model = GPT_MODEL, prompt = prompt, max_tokens = MAX_TOKENS, temperature = TEMPERATURE)['choices'][0]['text'] + "\n"
                    output_ += response
            else:
                output_ = 'Error: too many tokens used. Please shorten your input.'
    return render_template('c++_to_java_converter.html', input = input_, output = output_)


if __name__ == '__main__':
    app.run(debug = True)