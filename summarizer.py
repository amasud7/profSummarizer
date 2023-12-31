# imports needed
from selenium import webdriver
from selenium.webdriver.common.by import By
import google.generativeai as palm
import key


# for getting reviews from website
driver = webdriver.Firefox() # which browser it opens
driver.implicitly_wait(1) # wait for elements to load in page
driver.get("https://www.ratemyprofessors.com/professor/2510723") # currently manual link, but prof search bar?
driver.find_element(By.XPATH, "/html/body/div[5]/div/div/button").click() # find pop up button for cookies and click to exit
driver.implicitly_wait(1)
elements = driver.find_elements(By.CLASS_NAME, "gRjWel") # list of the reviews

# creates a list and get the actual text from the html elements stored in elements
reviews = []
for element in elements:
    reviews.append(element.text)

driver.close() # closes the window 

# configuring key
palm.configure(api_key=key.API_KEY)
 
# getting the LLM model
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

# function that uses model and scraped data
def summarize(reviews, model):
    # prompt to feed into LLM, which then uses the reviews according to what the 
    prompt = "Take these reviews of professors from students and write me a list of the best and worst things about this professor."

    # adding each review and prompt into one string to feed to the LLM
    for element in reviews:
        prompt += "\n" + element

    # LLM parameters 
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=500,
    )
    return completion.result

# call function
print(summarize(reviews, model))








