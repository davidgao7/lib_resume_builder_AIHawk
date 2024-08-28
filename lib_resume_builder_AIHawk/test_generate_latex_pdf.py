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
from resume import Resume
from src.job import Job
from langchain_community.document_loaders import TextLoader
from langchain_core.messages.ai import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import StringPromptValue
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_text_splitters import TokenTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pylatex import Command, Document, Section, Subsection
from pylatex.utils import NoEscape, italic, bold
from dotenv import load_dotenv

load_dotenv()


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

    # 1. set the job application profile
    job_application_profile_object = JobApplicationProfile(plain_text_resume)

    # 2. set job application resume
    resume_object = Resume(plain_text_resume)
    print(f"\n================resume object==============================\n")
    print(resume_object)
    print(f"\n================resume object==============================\n")

    # 3. set gpt answer
    gpt_answerer = GPTAnswerer(
        openai_api_key, model_name="gpt-4o-mini", temperature=0.8
    )

    # 4. set the resume generator
    # TODO: 4.1 analyze the job description
    # NOTE: this is just a random job post I found on LinkedIn, no offense to anyone/any company
    job_example = Job(
        title="Senior Machine Learning Engineer",
        company="Orbis Group",
        location="United States",
        link="https://www.linkedin.com/jobs/view/4009774636",
        apply_method="LinkedIn",
        description="""
        About the job

        Principal ML Engineer - Recommendation and Personalization


        A conversational AI start-up is expanding it's engineering team with the hire of a Staff or Principal-level ML Engineer to research, develop and deploy models for a consumer-facing conversational AI agent.


        You'd report to the CTO as one of the most senior individual contributor hires, owning a wide breadth of responsibilities and having a huge sphere of influence.


        Principal ML Engineer Responsibilities


            Set the technical direction and drive the strategy and systems design for the team
            Hands-on work - research, development, deployment, optimization etc.
            Act as a senior IC working closely with leadership and some mentoring of juniors


        Principal ML Engiener Requirements


            PhD in STEM subject - ideally CompSci or similar
            4+ years of professional, post academic experience, ideally in a start-up
            Knowledge of recommendation and personalization ML systems
            Knowledge of Python, Node, Pandas, Pytorch, Kubernetes, GCP etc.


        This is a unique opportunity to join a highly decorated founding team of ~30, where you can make a large impact from day one and get in on the ground floor of a rapidly scaling business.


        If you'd like to find out more, please don't hesitate to apply!
        """,
        summarize_job_description="""
        Position: Principal ML Engineer - Recommendation and Personalization
        Company: Conversational AI Start-Up
        Location: (Not specified)
        Reporting to: CTO

        Responsibilities:

            Set the technical direction and strategy for the ML team.
            Engage in hands-on work, including research, development, deployment, and optimization of ML models.
            Work closely with leadership and mentor junior team members.

        Requirements:

            PhD in a STEM subject (preferably Computer Science).
            4+ years of post-academic professional experience, ideally in a start-up environment.
            Experience with recommendation and personalization ML systems.
            Proficiency in Python, Node, Pandas, PyTorch, Kubernetes, and GCP.

        Opportunity:

            Join a small, high-impact team at a rapidly growing start-up.
            Significant influence from the start and a chance to contribute to a key technology initiative.

        Apply: (Apply if interested in joining a high-impact, scaling business.)
        """,
        pdf_path="data_folder/output/",
        recruiter_link="https://www.linkedin.com/in/matt-herselman/",
    )
    print(job_example)

    # write job description file if not exists
    if not os.path.exists(f"{parent_dir}/job_example.txt"):
        with open(f"{parent_dir}/job_example.txt", "w") as f:
            f.write(job_example.description)
            f.close()

    # Using langchain to customize prompt

    print("========================getting job description...=======================")
    job_description_prompt_template = PromptTemplate.from_template(
        """
        You are an expert job description analyst. Your role is to meticulously analyze and interpret job descriptions.
        After analyzing the job description, answer the following question in a clear, and informative manner.
                                                                                                                    
        Question: {question}                                                                                             
        Job Description: {context}                                                                                       
        Answer:                                                                                                          
        """
    )

    # 4.2.2 create vector store
    text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)
    loader = TextLoader(
        f"{parent_dir}/job_example.txt", encoding="utf-8", autodetect_encoding=True
    )
    document = loader.load()
    all_splits = text_splitter.split_documents(document)
    embedding_func = OpenAIEmbeddings(api_key=openai_api_key)
    vectorstore = FAISS.from_documents(documents=all_splits, embedding=embedding_func)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    context_formatter = vectorstore.as_retriever() | format_docs
    question_passthrough = RunnablePassthrough()

    # print(
    #     f"\n============vectorstore: ==========\n{vectorstore}\n============vectorstore: ==========\n"
    # )

    # 4.2.3 pass prompt to llm
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key, temperature=0.8)

    # gpt output job description summary
    chain_job_descroption = job_description_prompt_template | llm | StrOutputParser()

    chain_job_description = (
        {
            "context": context_formatter,
            "question": question_passthrough,
        }
        | chain_job_descroption
        | llm
        | StrOutputParser()
    )

    # get summary of job description
    summarize_prompt_template = """
        As a seasoned HR expert, your task is to identify and outline the key skills and requirements necessary for the position of this job. Use the provided job description as input to extract all relevant information. This will involve conducting a thorough analysis of the job's responsibilities and the industry standards. You should consider both the technical and soft skills needed to excel in this role. Additionally, specify any educational qualifications, certifications, or experiences that are essential. Your analysis should also reflect on the evolving nature of this role, considering future trends and how they might affect the required competencies.

        Rules:
        Remove boilerplate text
        Include only relevant information to match the job description against the resume

        # Analysis Requirements
        Your analysis should include the following sections:
        Technical Skills: List all the specific technical skills required for the role based on the responsibilities described in the job description.
        Soft Skills: Identify the necessary soft skills, such as communication abilities, problem-solving, time management, etc.
        Educational Qualifications and Certifications: Specify the essential educational qualifications and certifications for the role.
        Professional Experience: Describe the relevant work experiences that are required or preferred.
        Role Evolution: Analyze how the role might evolve in the future, considering industry trends and how these might influence the required skills.

        # Final Result:
        Your analysis should be structured in a clear and organized document with distinct sections for each of the points listed above. Each section should contain:
        This comprehensive overview will serve as a guideline for the recruitment process, ensuring the identification of the most qualified candidates.

        You should ALWAYS provide a [Yes/No/Not mentioned] answer at the end for whether the job can sponsor a visa or not.

        # Job Description:
        ```
        {text}
        ```

        ---

        # Job Description Summary"""

    prompt_summarize = ChatPromptTemplate.from_template(summarize_prompt_template)
    chain_summarize = prompt_summarize | llm | StrOutputParser()

    qa_chain = (
        {
            "context": context_formatter,
            "question": question_passthrough,
        }
        | chain_job_descroption
        | (lambda output: {"text": output})
        | chain_summarize
    )

    job_description = qa_chain.invoke("Provide, full job description")

    print(f"job_description:\n {job_description}\n")
    print("========================job description done=======================")

    # TODO: 4.2 construct the corresponding resume section acording to the job description
    #
    # 4.2.1 create resume according to job description
    # 4.2.1.1 create resume object
    #
