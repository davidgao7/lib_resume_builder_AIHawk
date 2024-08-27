from pylatex import Document, Command
from pylatex.utils import NoEscape

# Example function to create a LaTeX document with the default config
def create_latex_document(
    default_filepath: str = 'default_filepath',
    documentclass: str = 'article',
    document_options: str | list = None,
    fontenc: str = 'T1',
    inputenc: str = 'utf8',
    font_size: str = 'normalsize',
    lmodern: bool = True,
    textcomp: bool = True,
    page_numbers: bool = True,
    indent: bool = True,
    geometry_options: dict = None,
    data: list = None
):
    """
    A class that contains a full LaTeX document.

    If needed, you can append stuff to the preamble or the packages. For instance, if you need to use \maketitle you can add the title, author and date commands to the preamble to make it work.

    Parameters:
    - default_filepath (str): The default path to save files.
    - documentclass (str): The LaTeX class of the document.
    - document_options (str or list): The options to supply to the documentclass.
    - fontenc (str): The option for the fontenc package. If None, the package is not loaded.
    - inputenc (str): The option for the inputenc package. If None, the package is not loaded.
    - font_size (str): The font size to declare as normalsize.
    - lmodern (bool): Use the Latin Modern font.
    - textcomp (bool): Adds additional glyphs, like the Euro (€) sign.
    - page_numbers (bool): Whether or not to add page numbers to the document.
    - indent (bool): Determines whether or not the document requires indentation.
    - geometry_options (dict): The options to supply to the geometry package.
    - data (list): Initial content of the document.

    Returns:
    - Document: A configured LaTeX Document object.
    """
    doc = Document(
        default_filepath,
        documentclass=documentclass,
        document_options=document_options,
        fontenc=fontenc,
        inputenc=inputenc,
        font_size=font_size,
        lmodern=lmodern,
        textcomp=textcomp,
        page_numbers=page_numbers,
        indent=indent,
        geometry_options=geometry_options,
        data=data
    )

    # Apply additional configurations as needed
    # For example, if there are custom commands or packages to add
    if lmodern:
        doc.packages.append(Command('usepackage', 'lmodern'))
    
    if textcomp:
        doc.packages.append(Command('usepackage', 'textcomp'))

    # Configure the geometry package with the provided options
    if geometry_options:
        geometry_command = Command('geometry', options=geometry_options)
        doc.packages.append(geometry_command)

    return doc


# TODO: how to create function to generate a LaTeX document with a custom template using pylatex and gpt
