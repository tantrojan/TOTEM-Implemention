# TOTEM-Implemention

Python application to generate summary of a document.

## Summarization Approach
Convert the document into a set of topics and then rank the sentences under each topic. Finally choose top sentences from each topic to generate the summary.

### Idea from Research Paper
>[TOTEM: Personal Tweets Summarization on Mobile Devices](https://dl.acm.org/doi/10.1145/3077136.3084138)

## Usage

- Clone the project
- Install packages
```bash
pip install -r requirement.txt
```
- Run the project
```bash
python totem.py <document> <output_file> <number_of_topics>
```
>example :
python totem.py ./sample_datasets/1000_hydb.txt ./sample.txt 4
