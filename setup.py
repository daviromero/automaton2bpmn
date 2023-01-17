from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='automaton2bpmn',
    version='0.0.3',
    license='MIT',
    author="Davi Romero de Vasconcelos",
    author_email='daviromero@ufc.br',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/daviromero/automaton2bpmn',
    description='''Automaton2bpmn is a library for converting automata (teocomp package) to bpmn.''',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='Theory of Computing, Automata Theory, Languages, Lambda-Calculus, Recursive Function (Kleene), Teaching Theory of Computing, Educational Software', 
    install_requires=[
        'graphviz',
        'teocomp',
        'pm4py'
      ],

)
