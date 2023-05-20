import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

st.set_page_config(page_title="Omform Email", page_icon=":robot:")
#st.set_page_config(page_title="Globalize Email")
 

template = """
    Nedenfor findes en email, som kan være dårligt skrevet.
    Dit mål er at:
    - Formatere denne email ordentligt
    - Omskrive teksten til en bestemt form
    - Omskrive teksten til en bestemt dialekt

    Her er eksempler på forskellige Former:
    - Formel: Hun besidder ikke den fornødne energi til at modtage informationer i en undervisningstime.
    - Uformel: Hun gider ikke høre efter.  

    Her er nogle eksempler på ord i forskellige dialekter:
    - Rigsdansk: således, skrive, skrev, mange, ikke, fordi at, selv, langt, løgn, bogen, stykker, købe, spørge
    - Himmerlandsk: sören, skryw, skröw, manne, et, fodé te, siel, lånt, lywlas, æbog, stomper, kyef, spör

    Eksempler på sætninger fra hver dialekt:
    - Rigsdansk: Det sikreste er vel at forsøge at sætte kriterier op for hvad sprog er uden skelnen til om vi mennesker alene er i besiddelse af sprogevnen. Alle de sprog der tales af mennesker, opfylder disse kriterier. En række af kriterierne, hvis ikke alle, er også opfyldt af de sprog man har lært visse højerestående primater.
    - Himmerlandsk: Sören blöw han ve mæ å spör å skryw åp. Ilaw han kam hjæm, skröw han en bog om hans ræjs. Mæn han hår manne fjender, især en studiere græsk mand, som hie Strabon, å som wa misundelig. fodé te han et siel hår ræjst så lånt. Å dæn hær Strabon, han kjæfte åp om, te de wa jænne lywlas, hwa Pytheas fortal. Så wa dæ jo ingen, dæ vild kyef æbog, å dæfo gæk dæn te grund så nær somno sölle bette stomper.
    
    Start gerne emailen med en varm introduktion. Tilføj introduktionen hvis det er nødvendigt.
    
    Nedenfor findes email, form, og dialekt:
    FORM: {form}
    DIALEKT: {dialekt}
    EMAIL: {email}
    
    DIT {dialekt} SVAR:
"""

prompt = PromptTemplate(
    input_variables=["form", "dialekt", "email"],
    template=template,
)


#import os
#os.environ["OPENAI_API_KEY"] = openai_api_key


def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key", help="Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

st.header("Omform tekst")

col1, col2 = st.columns(2)

with col1:
    option_tone = st.selectbox("Hvilken form skal din email have?", ("Formel", "Uformel"))
    st.write("")

with col2:
    option_dialect = st.selectbox("Hvilken dialekt skal din email have?", ("Rigsdansk", "Himmerlandsk"))
    st.write("")

st.markdown("## Indsæt den email tekst der skal omformes")

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    #input_text = st.text_area(label="", placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Indsæt venligst en kortere mail. Maksimumlængden er 700 ord.")
    st.stop()

def update_text_with_example1():
    print ("in updated")
    st.session_state.email_input = "Frederik jeg starte arbejde hos dig mandag hilsen viggo"

def update_text_with_example2():
    print ("in updated")
    st.session_state.email_input = "Morten. Kan du hente mig på tirsdag? Kærlig hilsen fra Ole"


def update_text_with_example(FirstOrSecond):
    if FirstOrSecond:
        print ("in updated")
        st.session_state.email_input = "Frederik jeg starte arbejde hos dig mandag hilsen viggo"
    else:
        print ("in updated")
        st.session_state.email_input = "Morten. Kan du hente mig på tirsdag? Kærlig hilsen fra Ole"

col1, col2 = st.columns(2)


with col1:
    st.button("*Se et eksempel*", key="Eksempel1", type='secondary', help="Tryk for at se et eksempel på en email der skal omformes.", on_click=update_text_with_example1)
    #st.write("")

with col2:
    st.button("*Se et andet eksempel*", key="Eksempel2", type='secondary', help="Tryk for at se et eksempel på en email der skal omformes.", on_click=update_text_with_example2)
    #st.write("")




#st.form_submit_button("*Se et eksempel*", key="Eksempel1", type='secondary', help="Tryk for at se et eksempel på en email der skal omformes.", on_click=update_text_with_example1)
#st.form_submit_("*Se et andet eksempel*", key="Eksempel2", type='secondary', help="Tryk for at se et eksempel på en email der skal omformes.", on_click=update_text_with_example2)



st.markdown("### Den omformede email:")

if email_input:
    #if not openai_api_key:
    #    st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
    #    st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(form=option_tone, dialekt=option_dialect, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)
