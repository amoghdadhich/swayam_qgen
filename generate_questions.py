import requests

API_URL = "https://api-inference.huggingface.co/models/Salesforce/mixqg-3b"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def generate_questions(keywords_list: list, context: str):
	# Format the input query for the API 
    '''Sends a request to Mix-QG API to generate the questions for
    each keyword in <keywords_list> based on the text present in <context>
    
    INPUTS:
    keywords_list : list : list of keywords for which questions need to be generated
    context : str : paragraph of text for which the questions are generated
    
    RETURNS:
    response_dict : dict : dictionary that maps keyword in <keywords_list> to question generated
                           response_dict[keyword] = question 
    '''

    
    input_dicts_list = [{"inputs": keyword + '\\n' + context, "options": {"wait_for_model":True}} for keyword in keywords_list]

    response_dict = {}

    for i, input_dict in enumerate(input_dicts_list):
          response_dict[keywords_list[i]] = query(input_dict)[0]['generated_text']
    
    return response_dict
