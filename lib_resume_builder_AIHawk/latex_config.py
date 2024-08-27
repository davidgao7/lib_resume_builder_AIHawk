from pylatex import Document, Command, Package
from pylatex.utils import NoEscape
from dotenv import load_dotenv
import os


class LatexConfig:
    def __init__(
        self,
        OPENAI_API_KEY: str = None,
    ):
        """
        API_KEY (str): The LLM API key to use for the document, if None, use environment variable.
        """
        if not OPENAI_API_KEY:
            load_dotenv()
        else:
            os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    # Example function to create a LaTeX document with the default config
    def create_latex_document(
        self,
        packages: dict,
        default_filepath: str = "default_filepath",
        documentclass: str = "article",
        document_options: str | list = None,
        fontenc: str = "T1",
        inputenc: str = "utf8",
        font_size: str = "normalsize",
        lmodern: bool = True,
        textcomp: bool = True,
        page_numbers: bool = True,
        indent: bool = True,
        geometry_options: dict = None,
        data: list = None,
    ):
        """
        A class that contains a full LaTeX document.

        If needed, you can append stuff to the preamble or the packages. For instance, if you need to use \\maketitle you can add the title, author and date commands to the preamble to make it work.

        Parameters:
        - packages (dict): A dict of packages required.
          * {
                package_name(str) – Name of the package: options(str, list or Options) – Options of the package.
            }
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
            data=data,
        )

        # TODO: latex document settings are not registered!
        print(doc)

        for package_name, package_options in packages.items():
            if len(package_options) > 0:
                doc.packages.append(Package(package_name, options=package_options))
            else:
                doc.packages.append(Package(package_name))

        # Apply additional configurations as needed
        # For example, if there are custom commands or packages to add
        if lmodern:
            doc.packages.append(Command("usepackage", "lmodern"))

        if textcomp:
            doc.packages.append(Command("usepackage", "textcomp"))

        # Configure the geometry package with the provided options
        if geometry_options:
            geometry_command = Command("geometry", options=geometry_options)
            doc.packages.append(geometry_command)

        self.doc = doc

    def get_document(self):
        return self.doc

    # TODO: how to create function to generate a LaTeX document with a custom template using pylatex and gpt
    #


global_config = LatexConfig()
