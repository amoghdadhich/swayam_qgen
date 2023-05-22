import streamlit as st
import yake
import generate_questions as gq

st.title("Question answer generation")
st.markdown("The model outputs a set of questions and answers based on a paragraph")

# Text input widget
text = st.text_area(label="Enter text corpus here")

# For now we consider only single paragraphs of text
# paragraphs = parse_text(text) would break the text into multiple paragraphs

# Initialize the keyword extractor
kw_extractor = yake.KeywordExtractor()
keywords = kw_extractor.extract_keywords(text)

st.markdown("The keywords picked from the paragraph are given below")

# Display the words in columns 
NUM_COLS = 5
NUM_WORDS_PER_COL = 4

# The columns are generated as a list
cols = st.columns(NUM_COLS)

# Each word is shown as a button which can be included in the set of keywords
if 'selected_keywords' not in st.session_state:
    st.session_state.selected_keywords = set()

for i,word in enumerate(keywords):
    column = i // NUM_WORDS_PER_COL
    with cols[column]:

        button = st.button(label= word[0])

        if button:
            st.session_state.selected_keywords.add(word[0])

    # Draw a separating line after all words have been printed
    if i == len(keywords) - 1:
        st.markdown("""---""")


for i,word in enumerate(st.session_state.selected_keywords):
    column = i // NUM_WORDS_PER_COL
    with cols[column]:
        st.write(word)

gen_qs_button = st.button(label= "GENERATE QUESTIONS")

if gen_qs_button:
    # Generate the questions for the keywords
    response = gq.generate_questions(list(st.session_state.selected_keywords), text)
    
    # Print out the keywords
    for keyword in st.session_state.selected_keywords:
        st.write(f'Q. {response[keyword]}')
        st.write(f'A. {keyword}')