# num = 100
# try:
#     a = float(input('Enter a number to divide by: '))
#     print(num / a)
# except ZeroDivisionError:
#     print("Error: Division by zero is not allowed")
# except ValueError:
#     print("Error: Invalid input. Please enter a number.")
# finally:
#     print('We still want to print this!')

# print("Let's move on to the next part of the code...")

# names = ['Alice', 'Bob', 123, 'Charlie']
# uppercase_names = []

# for name in names:
#     try:
#         print(name.upper())
#         uppercase_names.append(name.upper())
#     except AttributeError:
#         print(f"Error: '{name}' is not a string and cannot be converted to uppercase.")
        
# print("Uppercase names:", uppercase_names)

# print("Let's move on to the next part of the code...")

import requests
from pprint import pprint
from dotenv import load_dotenv
import os

# response = requests.get('https://oim.108122.xyz/words/random')
# print(response.json())   # a random word!

# response = requests.get(
#     'https://oim.108122.xyz/mass',
#     headers={'X-Token': 'joejoe'},  # your first name x2
# )
# data = response.json()

# print(data['name'])       # 'Massachusetts'
# print(data['governor'])   # 'Maura Healey'

# print(len(data))
# print(data.keys())

# towns = data['data']
# # print(type(data['data'])) # do this for explore the data structure
# print(type(towns)) # do this for explore the data structure

# pprint(data['data'])
# print(len(towns))  #351

# requests.post('https://oim.108122.xyz/message',
#               json={'message': 'Hello from Joe!'},
#               headers={'X-Token': 'joejoe'})

load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv('OPENWEATHER_API_KEY')  # Get the API key from environment variable

url = (f'https://api.openweathermap.org/data/2.5/weather'
       f'?q=Boston&appid={API_KEY}&units=imperial')

print(url)
data = requests.get(url).json()
print(f"Boston: {data['main']['temp']}°F")
