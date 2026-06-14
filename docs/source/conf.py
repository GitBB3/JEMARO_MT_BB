# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'Simulation Study of Ant Stigmergy for Multi-Agent Post-disaster remapping of Uncertain Environments'
copyright = '2026, Bertille BEAUJEAN'
author = 'Bertille BEAUJEAN'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_show_sourcelink = False

html_context = {
    "display_github": True,
    "github_user": "GitBB3",
    "github_repo": "JEMARO_MT_BB",
    "github_version": "main",
    "conf_py_path": "/docs/source/",
}