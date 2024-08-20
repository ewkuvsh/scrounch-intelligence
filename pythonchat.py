from openai import OpenAI
import os
import sys
import json
import search  #local file search.py
from datetime import date
from dotenv import load_dotenv




load_dotenv()
client = OpenAI()
args = sys.argv
GPT_MODEL = "gpt-4o-mini"



def get_secret_code():
    
        return 'twiddlevee!'


print("\n")



tools = [

    {
        "type": "function",
        "function": {
            "name": "get_secret_code",
            "description": "Gets the secret code",
           
        },
    },

    {
      "type": "function",
      "function": {
        "name": "search_web",
        "description": "performs a web search and returns the body text of a relevant website. Use this function to find real time information that you don't know",
        "parameters": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "the search query that will be used to search the internet. use this to find up to date information."
            }
          },
          "required": ["query"]
        }
      }
    }



  

            


]


del(args[0])
date = date.today()


prompt = ''.join(str(arg)+" " for arg in args)

messages=[
    {"role": "system", "content": "You are an assistant who doesn't use text formatting and don't try to bold or italicize text. Your output should have newlines around every 55 characters. Use your tools to best answer questions." + str(date)},
    {"role": "user", "content": prompt}
  ]

completion = client.chat.completions.create(
    model = GPT_MODEL,
    messages = messages,
    tools = tools)

response_message = completion.choices[0].message
messages.append(response_message)





tool_calls = response_message.tool_calls
if tool_calls:
    tool_call_id = tool_calls[0].id
    tool_function_name = tool_calls[0].function.name
    if tool_function_name == 'get_secret_code':
        results = get_secret_code()
        
        messages.append({
            "role":"tool", 
            "tool_call_id":tool_call_id, 
            "name": tool_function_name, 
            "content":results
        })
        
        model_response_with_function_call = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
        ) 


    elif tool_function_name == 'search_web':
        results = "search failed"

        
        data = json.loads(str(tool_calls[0].function.arguments))

        
        query = data.get("query")

        
        
        results = search.search(query)
        
        messages.append({
            "role":"tool", 
            "tool_call_id":tool_call_id, 
            "name": tool_function_name, 
            "content":results
        })

        
        model_response_with_function_call = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
        ) 
        print(model_response_with_function_call.choices[0].message.content)

else:
        print(completion.choices[0].message.content)

print("\n")
