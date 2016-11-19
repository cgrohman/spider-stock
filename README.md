# spider-stock
**Project Overview**

The objective of this project is to try to predict the outcome of a stock based on articles/historical performance data. The project flow is roughly as follows:
- Deploy scraping spider to identify and gather relevant text articles.
- Quantize the article data to reflect the positive and negative sentiment of the text.
- Use a genetic algorithm to optimally select a subset of these articles as inputs to a machine learning algorithm.
- Use trained machine learning algorithm to attempt to predict the performance of stock


**Detailed Description of each step:**

1. Scraping article data:
	1. Description of how data scraping and data storage will be handled

2. Quantize data:
	1. Description of data model and quantization methods

3. Genetic Algorithm:
	1. Description of genetic algorithm methodology

4. Machine Learnign Algorith:
	1. Description of possible implementations (NN). Training/testing/scoring descriptions.

**Environement Setup**

1. Install virtualenv and install requirements:
	1. $:pip install virtualenv
	2. $:virtualenv senv
	3. $:source senv/bin/activate
	4. $:pip install -r requirements.txt
