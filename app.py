import streamlit as st
import yake
import generate_questions as gq

st.title("Question answer generation")
st.markdown("The model outputs a set of questions and answers based on a paragraph")

# Text input widget
text = st.text_area(label="Enter text corpus here. Press ctrl + enter to generate keywords for this paragraph")

# The current question generation pipeline has the following steps

# STEP 1: Generate keywords

# Initialize the keyword extractor
kw_extractor = yake.KeywordExtractor()
keywords = kw_extractor.extract_keywords(text)

# Initialize the set into which the keywords will be written
if 'selected_keywords' not in st.session_state:
    st.session_state.selected_keywords = set()

# STEP 2: Decide how the keywords will be displayed
# The keywords will be aligned in <NUM_COLS> columns with <NUM_WORDS_PER_COL> words in each column
st.markdown("The keywords picked from the paragraph are given below. Click on the keyword to choose it")

NUM_COLS = 5
NUM_WORDS_PER_COL = 4

# The columns are generated as a list <cols>. Each element of this list refers to one displayed column
cols = st.columns(NUM_COLS)


# STEP 3: Pick the keywords which will be used to generate questions
# Each word is shown as a button which can be included in the set of keywords

for i,word in enumerate(keywords):
    column = i // NUM_WORDS_PER_COL                             # Pick the column in which the keyword would be displayed
    with cols[column]:

        button = st.button(label= word[0])                      # Create a button for each keyword

        if button:
            st.session_state.selected_keywords.add(word[0])     # The keyword is added upon button click

    # Draw a separating line after all words have been printed
    if i == len(keywords) - 1:
        st.markdown("""---""")

# STEP 4: Display each of the chosen keywords present in <selected_keywords
selected_cols = st.columns(NUM_COLS)

# STEP 5: Add more keywords manually

# Text input widget
new_keyword = st.text_input(label="Enter additional keywords here. Press Enter to add")

if new_keyword != "":
    st.session_state.selected_keywords.add(new_keyword)

if st.session_state.selected_keywords != set():
    for i,word in enumerate(st.session_state.selected_keywords):
        column = i % NUM_COLS
        with selected_cols[column]:
            st.write(word)

gen_qs_button = st.button(label= "GENERATE QUESTIONS")

# STEP 5: Generate the questions

if gen_qs_button:
    # Generate the questions for the keywords
    response = gq.generate_questions(list(st.session_state.selected_keywords), text)
    
    # Print out the question and the respective keyword (which is the answer) to each question
    for keyword in st.session_state.selected_keywords:
        st.write(f'Q. {response[keyword]}')
        st.write(f'A. {keyword}')

    # Clear the keywords set
    st.session_state.selected_keywords = set()