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
        page_numbers=False,
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
    # config.doc.generate_tex(f"{parent_parent_parent_dir}/generated_cv/result")

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
        f"{parent_parent_parent_dir}/data_folder/plain_text_resume.yaml", "r"
    ) as file:
        plain_text_resume_ymal = yaml.safe_load(file)
        print(f"plain_text_resume_ymal: {plain_text_resume_ymal}")

        if not plain_text_resume_ymal:
            raise Exception("plain_text_resume_ymal is not loaded correctly")

        file.close()

    with open(
        f"{parent_parent_parent_dir}/data_folder/plain_text_resume.yaml", "r"
    ) as file:
        plain_text_resume = file.read()
        print(f"plain_text_resume: {plain_text_resume}")

        file.close()

    # load latex header template
    with open(
        f"{parent_dir}/lib_resume_builder_AIHawk/resume_style/latex_resume_template_header.tex"
    ) as file:
        latex_resume_template_header = file.read()
        print(
            f"\n================================latex_resume_template_header start:=====================\n{latex_resume_template_header}\n================================latex_resume_template_header end:=====================\n"
        )
        file.close()

    # load latex sections template
    with open(
        f"{parent_dir}/lib_resume_builder_AIHawk/resume_style/latex_resume_template_sections.tex"
    ) as file:
        latex_resume_template_sections = file.read()
        print(
            f"\n================================latex_resume_template_sections start:=====================\n{latex_resume_template_sections}\n================================latex_resume_template_sections end:=====================\n"
        )
        file.close()

    # 1. set the job application profile
    job_application_profile_object = JobApplicationProfile(plain_text_resume)

    # 2. set job application resume
    resume_object = Resume(plain_text_resume)
    print(f"\n================resume object==============================\n")
    print(resume_object)
    print(f"\n================resume object==============================\n")

    # 3. set gpt answer
    gpt_answerer = GPTAnswerer(openai_api_key, model_name="gpt-4o", temperature=0.8)

    # 4. set the resume generator
    # TODO: 4.1 analyze the job description
    # NOTE: this is just a random job post I found on LinkedIn, no offense to anyone/any company
    job_example = Job(
        title="Machine Learning Engineer, Core Ranking ",
        company="Reddit, Inc.",
        location="United States",
        link="https://www.linkedin.com/jobs/view/3992823175/",
        apply_method="LinkedIn",
        description="""
        About the job
        Reddit is a community of communities. It’s built on shared interests, passion, and trust and is home to the most open and authentic conversations on the internet. Every day, Reddit users submit, vote, and comment on the topics they care most about. With 100,000+ active communities and approximately 82M+ daily active unique visitors, Reddit is one of the internet’s largest sources of information. For more information, visit redditinc.com.

        Location:

        This role is completely remote-friendly. If you happen to live close to one of our physical office locations, our doors are open for you to come into the office as often as you'd like.

        Team Description

        As a member of the Core Ranking ML team, you’ll work with the billions of events and terabytes of data generated every day to personalize Reddit for each of our over 50 million daily users, helping them to connect with their communities and discover the best of Reddit.

        Role Description

        As a Machine Learning Engineer, Core Ranking, this person will own projects from ideation to production, not just make small incremental gains on enterprise systems. This person will collaborate with other software engineers to improve the recommendation systems and models that power personalization and discovery across all of Reddit!

        Responsibilities

            Train, evaluate, and deploy sophisticated machine learning models to improve experiences for millions of users
            Participate in the full software development cycle: design, develop, QA, deploy, experiment, analyze and iterate
            Collaborate across disciplines and with other ML teams at Reddit to find technical solutions to complex challenges


        Required Qualifications

            2-3+ years of hands-on, post-grad, non-internship professional experience with Machine Learning in a production-based environment
            Solid theoretical knowledge of Machine Learning and Statistical concepts, including Deep Learning, as well as performance tradeoffs. Experience with recommender and/or ranking systems is a plus.
            Experience with at least 1 of: Tensorflow, Keras, PyTorch
            Experience working with data-intensive systems and writing production-quality software. Preferred Python or golang. Experience with kafka, ksql, and flink are a plus.
            The ability to extract insight from data; proficient with SQL
            Passionate about building delightful products for users
            Strong communication and team-work skills


        Benefits

            Comprehensive Healthcare Benefits
            401k Matching
            Workspace benefits for your home office
            Personal & Professional development funds
            Family Planning Support
            Flexible Vacation (please use them!) & Reddit Global Wellness Days
            4+ months paid Parental Leave
            Paid Volunteer time off


        Pay Transparency

        This job posting may span more than one career level.

        In addition to base salary, this job is eligible to receive equity in the form of restricted stock units, and depending on the position offered, it may also be eligible to receive a commission. Additionally, Reddit offers a wide range of benefits to U.S.-based employees, including medical, dental, and vision insurance, 401(k) program with employer match, generous time off for vacation, and parental leave. To learn more, please visit https://www.redditinc.com/careers/.

        To provide greater transparency to candidates, we share base pay ranges for all US-based job postings regardless of state. We set standard base pay ranges for all roles based on function, level, and country location, benchmarked against similar stage growth companies. Final offer amounts are determined by multiple factors including, skills, depth of work experience and relevant licenses/credentials, and may vary from the amounts listed below.

        The Base Pay Range For This Position Is

        $185,800—$260,100 USD

        Reddit is proud to be an equal opportunity employer, and is committed to building a workforce representative of the diverse communities we serve. Reddit is committed to providing reasonable accommodations for qualified individuals with disabilities and disabled veterans in our job application procedures. If you need assistance or an accommodation due to a disability, please contact us at ApplicationAssistance@Reddit.com.
        """,
        summarize_job_description="""
        About the job
        Reddit is a community of communities. It’s built on shared interests, passion, and trust and is home to the most open and authentic conversations on the internet. Every day, Reddit users submit, vote, and comment on the topics they care most about. With 100,000+ active communities and approximately 82M+ daily active unique visitors, Reddit is one of the internet’s largest sources of information. For more information, visit redditinc.com.

        Location:

        This role is completely remote-friendly. If you happen to live close to one of our physical office locations, our doors are open for you to come into the office as often as you'd like.

        Team Description

        As a member of the Core Ranking ML team, you’ll work with the billions of events and terabytes of data generated every day to personalize Reddit for each of our over 50 million daily users, helping them to connect with their communities and discover the best of Reddit.

        Role Description

        As a Machine Learning Engineer, Core Ranking, this person will own projects from ideation to production, not just make small incremental gains on enterprise systems. This person will collaborate with other software engineers to improve the recommendation systems and models that power personalization and discovery across all of Reddit!

        Responsibilities

            Train, evaluate, and deploy sophisticated machine learning models to improve experiences for millions of users
            Participate in the full software development cycle: design, develop, QA, deploy, experiment, analyze and iterate
            Collaborate across disciplines and with other ML teams at Reddit to find technical solutions to complex challenges


        Required Qualifications

            2-3+ years of hands-on, post-grad, non-internship professional experience with Machine Learning in a production-based environment
            Solid theoretical knowledge of Machine Learning and Statistical concepts, including Deep Learning, as well as performance tradeoffs. Experience with recommender and/or ranking systems is a plus.
            Experience with at least 1 of: Tensorflow, Keras, PyTorch
            Experience working with data-intensive systems and writing production-quality software. Preferred Python or golang. Experience with kafka, ksql, and flink are a plus.
            The ability to extract insight from data; proficient with SQL
            Passionate about building delightful products for users
            Strong communication and team-work skills


        Benefits

            Comprehensive Healthcare Benefits
            401k Matching
            Workspace benefits for your home office
            Personal & Professional development funds
            Family Planning Support
            Flexible Vacation (please use them!) & Reddit Global Wellness Days
            4+ months paid Parental Leave
            Paid Volunteer time off


        Pay Transparency

        This job posting may span more than one career level.

        In addition to base salary, this job is eligible to receive equity in the form of restricted stock units, and depending on the position offered, it may also be eligible to receive a commission. Additionally, Reddit offers a wide range of benefits to U.S.-based employees, including medical, dental, and vision insurance, 401(k) program with employer match, generous time off for vacation, and parental leave. To learn more, please visit https://www.redditinc.com/careers/.

        To provide greater transparency to candidates, we share base pay ranges for all US-based job postings regardless of state. We set standard base pay ranges for all roles based on function, level, and country location, benchmarked against similar stage growth companies. Final offer amounts are determined by multiple factors including, skills, depth of work experience and relevant licenses/credentials, and may vary from the amounts listed below.

        The Base Pay Range For This Position Is

        $185,800—$260,100 USD

        Reddit is proud to be an equal opportunity employer, and is committed to building a workforce representative of the diverse communities we serve. Reddit is committed to providing reasonable accommodations for qualified individuals with disabilities and disabled veterans in our job application procedures. If you need assistance or an accommodation due to a disability, please contact us at ApplicationAssistance@Reddit.com.
        """,
        pdf_path="data_folder/output/",
        recruiter_link="https://www.linkedin.com/jobs/view/3992823175/?alternateChannel=search&refId=32LBAOEiHtA2yZTxTJ2qug%3D%3D&trackingId=s22SvXsf7uVOJKURLoQZKQ%3D%3D",
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
    print("\n=============Generate Resume Section: Header=========================\n")

    resume_prompt_template = """
        Act as an HR expert and resume writer specializing in ATS-friendly resumes. Your task is to create a professional and polished content for the resume. 

        The header should:

        1. **Contact Information**: Include your full name, city and country, phone number, email address, LinkedIn profile, GitHub profile, ande personal website.
        2. **Formatting**: Ensure the contact details are presented clearly and are easy to read.

        - **My information:**  
        {personal_information}

        - **Template to Use**

        For the header, use the following template:
        ```LaTex
            {latex_resume_template_header}
        ```

        The header components: address, email, phone number, linkedin, Github, personal website shouled be in one row and centered.

        For body, use the following template:
        ```LaTex
            {latex_resume_template_sections}
        ```

        The body components: education, skills, experience, projects, certifications, and languages should be in separate sections.

        IMPORTANT: If one page counldn't fit all the body components, then ONLY include education, skills, experience and projects, since these are more important.

        IMPORTANT: If the address is too long to fit, ONLY write city, abbreviation of the country.

        IMPORTANT: You should ALWAYS ALWAYS make sure the resume is ONE PAGE.

        The key word `COMPLETE_ME_`+ attribute is the where you need to fill in the information. 

        The information needed to fill the `COMPLETE_ME` attributes have all been provided in `My information` section. 

        The result should be a filled one page resume in Latex format. The keywords for teach stacks which are matched with the job description SHOULD BE BOLD.

        DO NOT LEAVE TOO MUCH WHITE SPACE. MAKE SURE THERES ONE PAGE OF CONTENT.

        The result should be provided in Latex format, Provide only the latex code for the resume, without any explanations or additional text and also without ```tex ```
    """

    resume_prompt = ChatPromptTemplate.from_template(resume_prompt_template)
    resume_chain = resume_prompt | llm | StrOutputParser()
    resume_latex_str = resume_chain.invoke(
        {
            "personal_information": plain_text_resume_ymal["personal_information"],
            "job_description": job_description,
            "latex_resume_template_header": latex_resume_template_header,
            "latex_resume_template_sections": latex_resume_template_sections,
        }
    )
    print("\n=============Generate Resume =========================\n")
    print(f"resume_latex_str:\n {resume_latex_str}\n")
    print("\n=============Generate Resume =========================\n")

    print("\n===saving tex file===\n")
    with open(f"{parent_parent_parent_dir}/generated_cv/result.tex", "w") as f:
        f.write(resume_latex_str)
        f.close()
    print("\n===saving tex file===\n")

    # 4.2.2 generate the pdf file
    # TODO:
    # print("\n===generate the pdf file===\n")
    # config.doc.generate_pdf(
    #     f"{parent_parent_parent_dir}/generated_cv/result",
    #     clean=True,  # Whether non-pdf files created that are created during compilation should be removed.
    #     clean_tex=False,  # whether remove the generated tex file.
    #     silent=True,  # whether show the output of the compilation
    #     compiler="xelatex",  # for the package fontspec
    # )
    # ! Package keyval Error: [ undefined.
    # See the keyval package documentation for explanation.
    # Type  H <return>  for immediate help.
    #  ...
    #
    # l.24 \geometry[
    #                scale=0.9,top=.4in,bottom=.4in]%
    # Try typing  <return>  to proceed.
    # If that doesn't work, type  X <return>  to quit.
    #
    #
    # Package geometry Warning: Over-specification in `v'-direction.
    #     `height' (787.23175pt) is ignored.
    #
    #
    # ! LaTeX Error: Missing \begin{document}.
    #
    # See the LaTeX manual or LaTeX Companion for explanation.
    # Type  H <return>  for immediate help.
    #
    # print("\n===generate the pdf file===\n")
