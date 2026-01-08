import random
import time
import statistics
import matplotlib.pyplot as plt
import xmltodict
import xmlpydict
import requests

SMALL_XML = """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">
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

url = "https://aiweb.cs.washington.edu/research/projects/xmltk/xmldata/data/tpc-h/partsupp.xml"
LARGE_XML = requests.get(url).text

ITERATIONS = 20
TRIALS = 10

parsers = [
    ("xmlpydict", lambda s: xmlpydict.parse(s)),
    ("xmltodict", lambda s: xmltodict.parse(s)),
]


def benchmark(xml_string):
    results = {name: [] for name, _ in parsers}

    for _ in range(TRIALS):
        funcs = parsers[:]
        random.shuffle(funcs)

        for name, fn in funcs:
            start = time.perf_counter()
            for _ in range(ITERATIONS):
                fn(xml_string)
            elapsed = time.perf_counter() - start
            results[name].append(elapsed)

    return results


small_results = benchmark(SMALL_XML)
large_results = benchmark(LARGE_XML)


def plot_results(results, title):
    names = list(results.keys())
    means = [statistics.mean(results[n]) for n in names]
    stds = [statistics.stdev(results[n]) for n in names]

    plt.figure()
    plt.bar(names, means, yerr=stds, capsize=6)
    plt.ylabel("Time (seconds)")
    plt.title(title)
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(f"{title}.png", dpi=200)
    plt.close()


plot_results(small_results, "small_xml_document")
plot_results(large_results, "large_xml_document")
