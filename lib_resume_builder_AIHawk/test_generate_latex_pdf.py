"""
currently the markdown pdf is not good engough, so I want to use latex to generate the pdf
This file means to test generate latex pdf
"""

# add src folder to sys.path
import sys
import os
import yaml

# get project root directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
parent_parent_parent_dir = os.path.abspath(os.path.join(parent_dir, os.path.pardir))
parent_parent_dir = os.path.join(parent_parent_parent_dir, "src")
print(f"parent_dir: {parent_dir}")
print(f"parent_parent_dir: {parent_parent_dir}")
print(f"parent_parent_parent_dir: {parent_parent_parent_dir}")

# Add the parent directory to the system path
sys.path.append(parent_dir)
sys.path.append(parent_parent_dir)
sys.path.append(parent_parent_parent_dir)

from latex_config import LatexConfig
from gpt import GPTAnswerer
from job_application_profile import JobApplicationProfile


if __name__ == "__main__":
    config = LatexConfig()
    defualt_path = (
        os.path.join(__file__).replace(
            "lib_resume_builder_AIHawk/lib_resume_builder_AIHawk/test_generate_latex_pdf.py",
            "generated_cv/result.tex",
        ),
    )
    defualt_path = defualt_path[0]

    print(f"defualt_path: {defualt_path}")

    config.create_latex_document(
        default_filepath=defualt_path,
        documentclass="article",
        font_size="11pt",
        lmodern=True,
        textcomp=True,
        page_numbers=True,
        indent=True,
        geometry_options={"scale": 0.9, "top": ".4in", "bottom": ".4in"},
        packages={
            "parskip": [],
            "hologo": [],
            "fontspec": [],
            "color": [],
            "graphicx": [],
            "xcolor": ["usenames", "dvipsnames"],
            "tabularx": [],
            "enumitem": [],
            "supertabular": [],
            "titlesec": [],
            "multicol": [],
            "multirow": [],
            "biblatex": ["style=authoryear", "sorting=ynt", "maxbibnames=2"],
            "hyperref": ["unicode", "draft=false"],
            "fontawesome5": [],
            "ulem": ["normalem"],
        },
        document_options=["a4paper", "8pt"],
        fontenc="T1",
        inputenc="utf8",
        font_type="Arial",
        document_style="empty",
    )

    # genterate the .tex file
    config.doc.generate_tex(f"{parent_parent_parent_dir}/generated_cv/result")

    # NOTE: can also get doc object by config.doc

    # generate the pdf file
    # config.doc.generate_pdf(
    #     "/Users/tengjungao/linkedIn_auto_jobs_applier_with_AI/generated_cv/result",
    #     clean=True,  # Whether non-pdf files created that are created during compilation should be removed.
    #     clean_tex=False,  # whether remove the generated tex file.
    #     silent=True,  # whether show the output of the compilation
    # )

    # read secrets
    with open(
        f"{parent_parent_parent_dir}/data_folder/secrets.yaml",
        "r",
    ) as file:
        secrets = yaml.load(file, Loader=yaml.FullLoader)
        openai_api_key = secrets["openai_api_key"]

    # test use gpt to generate the content in .tex
    with open(
        f"{parent_parent_parent_dir}/data_folder/plain_text_resume.yaml",
        "r",
    ) as file:
        plain_text_resume = file.read()
    job_application_profile_object = JobApplicationProfile(plain_text_resume)
    gpt_answerer_component = GPTAnswerer(openai_api_key)

    # TODO: 1. set the job application profile
    # 2. set job application resume
    # 3. set gpt answer
    # 4. set the resume generator
