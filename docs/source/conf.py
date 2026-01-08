# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'financial_planner_app'
copyright = '2026, Zvezdin Andrey'
author = 'Zvezdin Andrey'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys

# Указываем путь к папке с кодом (относительно этого файла)
sys.path.insert(0, os.path.abspath('../../'))

extensions = [
    'sphinx.ext.autodoc',    # Извлекает docstrings из модулей
    'sphinx.ext.napoleon',   # Поддерживает Google и NumPy стили
    'sphinx.ext.viewcode',   # Добавляет ссылки на исходный код (опционально)
    'myst_parser',           # Позволяет использовать Markdown вместо/вместе с reStructuredText (rST)
    ]

# -- Настройки Napoleon -----------------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False # Отключите, если используете только Google Style
napoleon_use_param = True
napoleon_use_rtype = True

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
