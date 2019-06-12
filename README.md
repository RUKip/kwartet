# kwartet
A simulation, playing a game of kwartet using logic rules. For the MAS course at RUG

## Installation
In order to be able to create graphs, we need to install graphviz libraries in our computer. 
The python package graphviz is just a wrapper to the C libraries.

For installation instructions to other OS check https://graphviz.gitlab.io/download/

For Ubuntu / Debian:
```
sudo apt update
sudo apt install graphviz
```
Create virtualenv in base repo directory:
```
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
source myenv/bin/activate
export PYTHONPATH="$PYTHONPATH:/<path_to_main_folder>"
```
### Report
The report can be found at: [https://rukip.github.io/MAS/kwartet.html]
