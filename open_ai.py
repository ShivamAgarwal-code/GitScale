import openai

def chatgpt(api_key, product_details, prompt):
  openai.api_key = api_key
  final_prompt = f"Convert the following dependencies into featurewise JIRA Tasks with detailed description, 3 subtasks as unordered list, labels and priority for developers to implement: \n {prompt}"
  res = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
      {
        "role":
        "system",
        "content": f"You are a product manager. Convert all requests into detailed JIRA tickets with voice tasks" 
        # Do not report the deadline, so each individual team can fill it in as per their schedule."
      },
      {
        "role": "user",
        "content": final_prompt
      },
    ],
    temperature=0,

  )["choices"][0]["message"]["content"]

  return res

def chat(api_key, product_details, prompt):
#   results = vector_search(prompt,4)
#   result_str = ""
#   for result in results:
#     result_str+=result
  # new_prompt = "Convert the relevant information from following into jira tickets for the tech team to implement: \n"+prompt
#   +"\nSome context for the decision:\n"+result_str
  return chatgpt(api_key, product_details, prompt)