from streamlit_text_label import label_select
import streamlit as st
import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet

from streamlit_text_label import Selection, label_select

def main():
    txt = st.text_input("Input paragraph here")
    selections = label_select(body=txt, labels=['IDK'])
    for selection in selections:
        word = selection.text
        word = word.lower()
        video_url = find_word_asl(word)
        st.subheader(word)
        if video_url != []:
            if type(video_url) == list:
                for video in video_url:
                    st.video(video)
            else:
                st.video(video_url)
        else:
            find_similar_words(word, video_url)


def find_similar_words(word, video_url):
    st.write("Exact word not found.  Similar word: ")
    lstsyn = set(video_url)
    for words in lstsyn:
        if words in word:
            lstsyn = root_word(words)
            
    for wordsym in lstsyn:
        video = find_word_asl(wordsym)
        if type(video) != list:
            st.write(wordsym)
            st.video(video)
            st.write("Other similar words: ")
            lstsyn = list(lstsyn)
            for wrd in lstsyn[1:5]:
                st.write(wrd)

def root_word(words):
    video = find_word_asl(words)
    if type(video) == list:
        lstsyn = set(video)
    else:
        st.write(words)
        st.video(video)
        lstsyn=[]
    return lstsyn

def find_word_asl(word):
    web_url = f"https://www.signingsavvy.com/search/{word}"
    r = requests.get(web_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    video_tags = soup.findAll('video')
    if len(video_tags) == 0:
        soup2 = BeautifulSoup(r.content, 'html.parser')
        results = soup2.find( class_="search_results")
        if results != None:
            return single_result(results)
        else:
            return try_signasl(word)

                
    else:
        for tag in video_tags:
            video_url = tag.find("source")['src']
            return video_url

def try_signasl(word):
    web_url = f"https://www.signasl.org/sign/{word}"
    r = requests.get(web_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    video_tags = soup.findAll('video')
    possible_urls = []
    for tag in video_tags:
        video_url = tag.find("source")['src']
        possible_urls.append(video_url)
    return possible_urls

def single_result(results):
    for result in results:
        tag = result.find("a")['href']
        web_url = f"https://www.signingsavvy.com/" + tag
        r = requests.get(web_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        video_tags = soup.findAll('video')
        urls = []
        for tag in video_tags:
            video_url = tag.find("source")['src']
            urls.append(video_url)
            return urls
        

def find_synonyms(word):
    synonyms = []

    for syn in wordnet.synsets(word):
        for i in syn.lemmas():
            synonyms.append(i.name())

    return synonyms


if __name__ == "__main__":
    main()
