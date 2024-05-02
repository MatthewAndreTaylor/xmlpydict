import xmlpydict
import xmltodict
import timeit

s = """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">
  <rect x="50" y="50" width="100" height="50" fill="blue" />
  <circle cx="200" cy="100" r="50" fill="red" />
  <ellipse cx="350" cy="75" rx="50" ry="25" fill="green" />
  <line x1="50" y1="200" x2="150" y2="300" stroke="orange" />
  <polyline points="200,200 250,250 300,200 350,250" fill="none" stroke="purple" />
  <polygon points="350,200 400,250 400,150" fill="yellow" />
  <path d="M50,350 L100,350 Q125,375 150,350 T200,350" fill="none" stroke="black"/>

  <rect x="10" y="10" height="100" width="100"
        style="stroke:#ff0000; fill: #0000ff"/>
        <path d="M50,350 L100,350 Q125,375 150,350 T200,350" fill="none" stroke="black"/><polygon points="350,200 400,250 400,150" fill="yellow" />


  <circle cx="200" cy="100" r="50" fill="red"></circle>

  <polygon points="350,200 400,250 400,150" fill="yellow" />
</svg>"""
print(timeit.timeit(lambda: xmlpydict.parse(s), number=100))
print(timeit.timeit(lambda: xmltodict.parse(s), number=100))

import requests

# Get a large sample XML file from the web (show the speed of both libraries is linear)
url = "https://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/tpc-h/part.xml"
response = requests.get(url)
s = response.text

print(timeit.timeit(lambda: xmlpydict.parse(s), number=100))
print(timeit.timeit(lambda: xmltodict.parse(s), number=100))
