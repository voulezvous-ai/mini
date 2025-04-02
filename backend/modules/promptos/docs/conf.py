# Configuração básica para a geração da documentação com Sphinx

project = 'PromptOS'
copyright = '2025, Your Name'
author = 'Your Name'

extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']