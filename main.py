import pandas as pd
from PyPDF2 import PdfReader
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import helper

from gensim.summarization.summarizer import summarize

import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Get Word Frequency and Summary of a Given Text')
st.write("Please upload a PDF file")

uploaded_file = st.file_uploader("Choose a file")
print(uploaded_file)
if uploaded_file is None:
    st.write('Please upload a File')
else:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    total_words = len(text)
    word_frequency = helper.count_word_frequency(text)
    col1, col2 = st.columns([1, 2])

    # to generate words cloud
    with col2:
        wc = WordCloud(height=200).generate_from_frequencies(word_frequency)
        plt.imshow(wc)
        plt.axis('off')
        st.pyplot()

    # to generate word's frequency
    with col1:
        min_freq = st.number_input('Input the minimum Frequency value', min_value=1)
        # get the word based on given frequency
        df = pd.DataFrame.from_dict(word_frequency, orient='index')
        df = df[df[0] >= min_freq].sort_values(by=[0], ascending=False).reset_index()
        df = df[df['index'].map(len) > 2]
        df = df.rename(columns= {'index': 'Words', 0: 'Frequency'})
        print(df.columns)
        st.write(df, width=400, height=200)

    # to generate the summary
    # here we are using gensim 3.8.3 version newer version don't support summarization
    # Hugging face for abstractive or other ml method (frequency count) can be use for extractive summarization.
    words_for_summary = st.number_input('Input a Number for Expected word\'s summary e.g.200', max_value=total_words/2)
    if st.button('Generate Summary'):
        summary = summarize(text, word_count=words_for_summary)
        st.write(summary)