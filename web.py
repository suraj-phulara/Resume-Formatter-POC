import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv  
import os
import docx2txt
from openai import OpenAI
from jinja2 import Environment, FileSystemLoader
import json
from resume_models import Resume, Rewrite

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from latex_resumes import generate_latex_resume, generate_latex_resume2, generate_latex_resume3
import pdfkit



load_dotenv()
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)


def generate_resume_from_json(json_data, template_path):
    # Load Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("HTML_Resume_Template.html")

    # Render the template with JSON data
    rendered_resume = template.render({"resume":json_data})

    return rendered_resume


def getResume():
    st.title("Resume Uploader")
    st.write("Upload your resume below:")

    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx'])

    if uploaded_file is not None:
        # file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        # st.write(file_details)

        # Display file content
        if uploaded_file.type == "application/pdf":
            pdf_contents = read_pdf(uploaded_file)
            return pdf_contents
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            docx_contents = read_docx(uploaded_file)
            return docx_contents

def read_pdf(file):
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        # st.write(text)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF file: {e}")
        return None

def read_docx(file):
    return docx2txt.process(file)



# Define function to categorize resume data
def categorize_resume(resume_text):
    # Define the prompt for OpenAI API
    with open('HTML_Resume_Template.html', 'r') as file:
        resume_template = file.read()

    prompt = (
        f'analyze the following resume carefully and carefully extract all the key detaild from it like contact details, skills, education, experience, certifications, etc, etc. \n\n'
        f'Resume Data:\n'
        f'{resume_text}\n\n'
        f'--- Read the above resume and return me a detailed json containing the required info\n\n'
   
    )

    # Call OpenAI API to generate categories
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    json_data = response.choices[0].message.content
    json_data = json.loads(response.choices[0].message.content)
    print(json_data)
    return response






def remove_empty_lines(html_content):
    # Split the HTML content into lines
    lines = html_content.splitlines()

    # Filter out empty lines
    non_empty_lines = filter(lambda line: line.strip(), lines)

    # Join the non-empty lines back together
    cleaned_html_content = '\n'.join(non_empty_lines)

    return cleaned_html_content


def structured_output(text):
    # Initialize the GPT API model
    model = ChatOpenAI(temperature=0)

    # And a query intented to prompt a language model to populate the data structure.
    joke_query = f"read this text extracted from a user resume carefully and classify this based on different criteria into the json format.   text : {text} \n\n"

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=Resume)

    prompt = PromptTemplate(
        template="always write date in this format : %Y-%M-%D for example: '2014-10-01'.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    response = chain.invoke({"query": joke_query})

    # st.write(response)
    return response





def rewrite_with_ai(text):
    # Initialize the GPT API model
    model = ChatOpenAI(temperature=0.5)

    # And a query intented to prompt a language model to populate the data structure.
    joke_query = f"this text contains the summary of my one of the work experience in my resume. your task is to read it carefully and rewrite it in a humanised simpla and easy language. remember to not increse or decrease the length of the summary it should most importantly be exactly {len(text)} words. \n\n  text : {text} \n\n"

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=Rewrite)

    prompt = PromptTemplate(
        template="rewrite the given text making it ats friendly .\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    response = chain.invoke({"query": joke_query})
    # st.write(response["summary"])
    # print(response)

    # st.write(response)
    return response["summary"]







def display_basics(basics):
    st.header("**Basic Details**")  
    with st.expander("Basic Details"):
        # st.subheader("Name:")
        basics['name'] = st.text_input("**Name**", key="name_input", value=basics.get('name', ''))

        # st.subheader("Label:")
        basics['label'] = st.text_input("Label", key="label_input", value=basics.get('label', ''))

        # st.subheader("Email:")
        basics['email'] = st.text_input("Email", key="email_input", value=basics.get('email', ''))

        st.subheader("Phone:")
        basics['phone'] = st.text_input("Phone", key="phone_input", value=basics.get('phone', ''))

    if "location" in basics:
        st.subheader("Location:")
        with st.expander("Location"):
            location = basics.get('location', {})
            st.subheader("Address:")
            location['address'] = st.text_input("Address", key="address_input", value=location.get('address', ''))

            st.subheader("Postal Code:")
            location['postalCode'] = st.text_input("Postal Code", key="postal_code_input", value=location.get('postalCode', ''))

            st.subheader("City:")
            location['city'] = st.text_input("City", key="city_input", value=location.get('city', ''))

            st.subheader("Country Code:")
            location['countryCode'] = st.text_input("Country Code", key="country_code_input", value=location.get('countryCode', ''))

            st.subheader("Region:")
            location['region'] = st.text_input("Region", key="region_input", value=location.get('region', ''))

            basics['location'] = location

    st.subheader("Profiles:")
    with st.expander("Profiles"):
        profiles = basics.get('profiles', [])
        for index, profile in enumerate(profiles):
            st.subheader(f"Profile {index + 1}")
            profile['username'] = st.text_input("Username", key=f"profile_{index}_username_input", value=profile.get('username', ''))
            profile['url'] = st.text_input("URL", key=f"profile_{index}_url_input", value=profile.get('url', ''))



def rewrite_summary_with_ai(summary_ref):
    summary_ref = rewrite_with_ai(summary_ref)
    return summary_ref



def display_work(work):
    st.header("Work Experience")
    with st.expander("Work Experience"):
        st.markdown("---")
        for i, job in enumerate(work):
            st.subheader(f"Job {i + 1}")
            job['name'] = st.text_input(f"Name_{i}", job['name'])
            job['position'] = st.text_input(f"Position_{i}", job['position'])
            # job['url'] = st.text_input(f"URL_{i}", job['url'])
            job['startDate'] = st.text_input(f"Start Date_{i}", job['startDate'])
            job['endDate'] = st.text_input(f"End Date_{i}", job['endDate'])
            
            
            st.markdown("")
            st.subheader("Summary:")
            # Button to rewrite summary with AI
            if st.button("Rewrite with AI", key=i):
                job['summary']=rewrite_summary_with_ai( job['summary'])

            job['summary'] = st.text_area("", job['summary'])
                
            
            
            
            for j, highlight in enumerate(job.get('highlights', {})):
                job['highlights'][j] = st.text_input(f"Highlight {j + 1}_{i}", highlight)
            st.markdown("---")
            st.markdown("---")

def display_education(education):
    st.header("Education")
    with st.expander("Education"):
        for i, edu in enumerate(education):
            st.subheader(f"Educational Institution {i + 1}")
            edu['institution'] = st.text_input("Institution", edu.get('institution', ''), key=f"{i}_institution_input")
            # edu['url'] = st.text_input("URL", edu.get('url', ''), key=f"{i}_url_input")
            edu['area'] = st.text_input("Area", edu.get('area', ''), key=f"{i}_area_input")
            edu['studyType'] = st.text_input("Study Type", edu.get('studyType', ''), key=f"{i}_study_type_input")
            edu['startDate'] = st.text_input("Start Date", edu.get('startDate', ''), key=f"{i}_start_date_input")
            edu['endDate'] = st.text_input("End Date", edu.get('endDate', ''), key=f"{i}_end_date_input")
            edu['score'] = st.text_input("Score", edu.get('score', ''), key=f"{i}_score_input")
            st.markdown("---")


def display_skills(skills):
    st.header("Skills")
    with st.expander("Skills"):
        for skill in skills:
            name_key = f"Skill Name_{skill['name']}"
            skill['name'] = st.text_input("Skill Name", key=name_key, value=skill.get('name', ''))
            # Level and keywords can be added if needed

def display_certificates(certificates):
    st.header("Certificates")
    with st.expander("Certificates"):
        for cert in certificates:
            name_key = f"Certificate Name_{cert['name']}"
            cert['name'] = st.text_input("Certificate Name", key=name_key, value=cert.get('name', ''))
            # Date and issuer can be added if needed


def display_projects(projects):
    st.header("Projects")
    with st.expander("Projects"):
        for i, project in enumerate(projects):
            st.subheader(f"Project {i + 1}: {project.get('name', '')}")
            with st.container():
                project['name'] = st.text_input(f"Name_{i}", project.get('name', ''))
                project['description'] = st.text_area(f"Description_{i}", project.get('description', ''))
                project['startDate'] = st.text_input(f"Start Date_{i}", project.get('startDate', ''))
                project['endDate'] = st.text_input(f"End Date_{i}", project.get('endDate', ''))
                project['url'] = st.text_input(f"URL_{i}", project.get('url', ''))
                st.subheader("Highlights:")
                for j, highlight in enumerate(project.get('highlights', [])):
                    project['highlights'][j] = st.text_input(f"Highlight {j + 1}_{i}", highlight)
                st.subheader("Keywords:")
                for j, keyword in enumerate(project.get('keywords', [])):
                    project['keywords'][j] = st.text_input(f"Keyword {j + 1}_{i}", keyword)
                st.subheader("Roles:")
                for j, role in enumerate(project.get('roles', [])):
                    project['roles'][j] = st.text_input(f"Role {j + 1}_{i}", role)
                project['entity'] = st.text_input(f"Entity_{i}", project.get('entity', ''))
                project['type'] = st.text_input(f"Type_{i}", project.get('type', ''))



def printresume(resume_json_data):
    rendered_resume = generate_resume_from_json(resume_json_data, 'resume_template.html')
    rendered_resume = str(remove_empty_lines(rendered_resume))
    
    # Write the resume content
    st.write(rendered_resume, unsafe_allow_html=True)
    
    # Add a download button
    download_pdf(rendered_resume, 'resume.pdf')
    # if st.button("Download PDF"):
    #     download_pdf(rendered_resume, 'resume.pdf')

def generate_pdf(html_content, output_path):
    pdfkit.from_string(html_content, output_path)

def download_pdf(html_content, file_name):
    # Generate PDF from HTML content
    generate_pdf(html_content, file_name)
    # Provide download link
    with open(file_name, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    st.download_button(label="Click here to download",
                       data=pdf_bytes,
                       file_name=file_name,
                       mime="application/pdf")


def display_images_and_call_function(json_data):
    st.title("CHOOSE A DIFFERENT TEMPLATE :")

    # Define image filenames
    image_filenames = [
        "TemplateImg1.png",
        "TemplateImg2.png",
        "TemplateImg3.png"
    ]

    # Display images side by side in columns
    col1, col2, col3 = st.columns(3)
    
     
     # Display images and buttons
    with col1:
        st.image(image_filenames[0], use_column_width=True)
        if st.button("Select", key="button1"):
            generate_latex_resume(json_data)
    
    with col2:
        st.image(image_filenames[1], use_column_width=True)
        if st.button("Select", key="button2"):
            generate_latex_resume2(json_data)
    
    with col3:
        st.image(image_filenames[2], use_column_width=True)
        if st.button("Select", key="button3"):
            generate_latex_resume3(json_data)


    






# Sidebar navigation
def sidebar_navigation():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ["Upload Resume", "Resume Details", "Choose Theme"])
    return page



def main() :
    page = sidebar_navigation()
    text = ""
    if page == "Upload Resume":

        # Get the resume content
        resume_content = getResume()
        # Check if a resume is uploaded
        if resume_content:
            # Store the resume content in session state
            st.session_state.resume_content = resume_content


    if page == "Resume Details":
        # Check if resume content is in session state
        if "resume_content" not in st.session_state:
            # Redirect user to "Upload Resume" page
            st.sidebar.error("Please upload your resume first.")
            page = "Upload Resume"
        else:
            resume_content = st.session_state.resume_content


        if "resume_content" in st.session_state:
            # json_data = structured_output(resume_content)
            # if 'json_data':
            #     st.session_state.json_data = json_data 

            if "json_data" not in st.session_state:
                json_data = structured_output(resume_content)
                if json_data :
                    st.session_state['json_data'] = json_data

            
            if "json_data" in st.session_state:
                json_data = st.session_state['json_data']
                if json_data.get('basics'):
                    display_basics(json_data['basics'])

                if json_data.get('work'):
                    display_work(json_data['work'])

                # Uncomment the below line if you want to include education
                if json_data.get('education'):
                    display_education(json_data['education'])

                if json_data.get('skills'):
                    display_skills(json_data['skills'])

                if json_data.get('certificates'):
                    display_certificates(json_data['certificates'])

                if json_data.get('projects'):
                    display_projects(json_data['projects'])


    if page == "Choose Theme":
        # Call the function to display images
        if "resume_content" not in st.session_state:
            # Redirect user to "Upload Resume" page
            st.sidebar.error("Please upload your resume first.")
            page = "Upload Resume"
        elif "json_data" not in st.session_state:
            resume_content = st.session_state.resume_content
            json_data = structured_output(resume_content)
            st.session_state['json_data'] = json_data

        if "json_data" in st.session_state:

            json_data = st.session_state['json_data']
            printresume(json_data)
            display_images_and_call_function(json_data)
            



if __name__ == "__main__":
    main()
