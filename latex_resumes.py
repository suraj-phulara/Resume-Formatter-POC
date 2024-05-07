import json
import urllib.parse
import requests
import webbrowser

def generate_latex_resume(json_data):
    latex_content = ""
    latex_content += "\\documentclass{article}\n"
    latex_content += "\\usepackage{hyperref}\n"
    latex_content += "\\usepackage{enumitem}\n\n"
    latex_content += "\\begin{document}\n\n"
    
    basics = json_data.get("basics", {})
    latex_content += "\\title{" + basics.get("name", "") + "}\n"
    latex_content += "\\author{" + basics.get("label", "") + "}\n"
    latex_content += "\\date{}\n"
    latex_content += "\\maketitle\n\n"
    
    # Contact Information
    if basics:
        latex_content += "\\section{Contact Information}\n"
        latex_content += "\\begin{itemize}[label=]\n"
        latex_content += "\\item \\textbf{Name:} " + basics.get("name", "") + "\n"
        latex_content += "\\item \\textbf{Label:} " + basics.get("label", "") + "\n"
        latex_content += "\\item \\textbf{Email:} " + basics.get("email", "") + "\n"
        latex_content += "\\item \\textbf{Phone:} " + basics.get("phone", "") + "\n"
        location = basics.get("location", {})
        if location:
            latex_content += "\\item \\textbf{Location:} " + location.get("city", "") + ", " + location.get("countryCode", "") + "\n"
        latex_content += "\\end{itemize}\n\n"
    
    # Work Experience
    work = json_data.get("work", [])
    if work:
        latex_content += "\\section{Work Experience}\n"
        for item in work:
            latex_content += "\\subsection{" + item.get("name", "") + " - " + item.get("position", "") + "}\n"
            latex_content += "\\textbf{Date:} " + item.get("startDate", "") + " to " + item.get("endDate", "") + "\n"
            latex_content += "\\begin{itemize}[label=-]\n"
            latex_content += "\\item " + item.get("summary", "") + "\n"
            highlights = item.get("highlights", [])
            if highlights:
                latex_content += "\\item \\textbf{Highlights:}\n"
                latex_content += "\\begin{itemize}[label=--]\n"
                for highlight in highlights:
                    latex_content += "\\item " + highlight + "\n"
                latex_content += "\\end{itemize}\n"
            latex_content += "\\end{itemize}\n\n"
    
    # Volunteer Experience
    volunteer = json_data.get("volunteer", [])
    if volunteer:
        latex_content += "\\section{Volunteer Experience}\n"
        for item in volunteer:
            latex_content += "\\subsection{" + item.get("organization", "") + " - " + item.get("position", "") + "}\n"
            latex_content += "\\textbf{Date:} " + item.get("startDate", "") + " to " + item.get("endDate", "") + "\n"
            latex_content += "\\begin{itemize}[label=-]\n"
            latex_content += "\\item " + item.get("summary", "") + "\n"
            highlights = item.get("highlights", [])
            if highlights:
                latex_content += "\\item \\textbf{Highlights:}\n"
                latex_content += "\\begin{itemize}[label=--]\n"
                for highlight in highlights:
                    latex_content += "\\item " + highlight + "\n"
                latex_content += "\\end{itemize}\n"
            latex_content += "\\end{itemize}\n\n"
    
    # Education
    education = json_data.get("education", [])
    if education:
        latex_content += "\\section{Education}\n"
        for item in education:
            latex_content += "\\subsection{" + item.get("studyType", "") + " in " + item.get("area", "") + " at " + item.get("institution", "") + "}\n"
            latex_content += "\\textbf{Date:} " + item.get("startDate", "") + " to " + item.get("endDate", "") + "\n"
            latex_content += "\\begin{itemize}[label=-]\n"
            latex_content += "\\item \\textbf{Score:} " + item.get("score", "") + "\n"
            latex_content += "\\end{itemize}\n\n"
    
    # Awards
    awards = json_data.get("awards", [])
    if awards:
        latex_content += "\\section{Awards}\n"
        for item in awards:
            latex_content += "\\subsection{" + item.get("title", "") + "}\n"
            latex_content += "\\textbf{Date:} " + item.get("date", "") + "\n"
            latex_content += "\\textbf{Awarder:} " + item.get("awarder", "") + "\n"
            latex_content += "\\begin{itemize}[label=-]\n"
            latex_content += "\\item " + item.get("summary", "") + "\n"
            latex_content += "\\end{itemize}\n\n"
    
    # Publications
    publications = json_data.get("publications", [])
    if publications:
        latex_content += "\\section{Publications}\n"
        for item in publications:
            latex_content += "\\subsection{" + item.get("name", "") + "}\n"
            latex_content += "\\textbf{Publisher:} " + item.get("publisher", "") + "\n"
            latex_content += "\\textbf{Date:} " + item.get("releaseDate", "") + "\n"
            latex_content += "\\begin{itemize}[label=-]\n"
            latex_content += "\\item " + item.get("summary", "") + "\n"
            latex_content += "\\end{itemize}\n\n"
    
    # Skills
    skills = json_data.get("skills", [])
    if skills:
        latex_content += "\\section{Skills}\n"
        latex_content += "\\begin{itemize}\n"
        for skill in skills:
            latex_content += "\\item " + skill.get("name", "") + "\n"
        latex_content += "\\end{itemize}\n\n"
    
    # Languages
    languages = json_data.get("languages", [])
    if languages:
        latex_content += "\\section{Languages}\n"
        latex_content += "\\begin{itemize}\n"
        for lang in languages:
            latex_content += "\\item " + lang.get("language", "") + " - " + lang.get("fluency", "") + "\n"
        latex_content += "\\end{itemize}\n\n"
    
    # Interests
    interests = json_data.get("interests", [])
    if interests:
        latex_content += "\\section{Interests}\n"
        latex_content += "\\begin{itemize}\n"
        for interest in interests:
            latex_content += "\\item " + interest.get("name", "") + "\n"
        latex_content += "\\end{itemize}\n\n"
    
    # References
    references = json_data.get("references", [])
    if references:
        latex_content += "\\section{References}\n"
        for ref in references:
            latex_content += "\\subsection{" + ref.get("name", "") + "}\n"
            latex_content += ref.get("reference", "") + "\n\n"
    
    latex_content += "\\end{document}"

    # print(latex_content)

    # return urllib.parse.quote(latex_content)
    api_url = 'https://latexonline.cc/compile'
    api_call_url = api_url + "?text=" + latex_content
    webbrowser.open(api_call_url)





def generate_latex_resume2(json_data):
    latex_content = ""
    latex_content += "\\documentclass{article}\n"
    latex_content += "\\usepackage{hyperref}\n"
    latex_content += "\\usepackage{enumitem}\n"
    latex_content += "\\usepackage[left=0.5in,right=0.5in,top=0.5in,bottom=0.5in]{geometry}\n"
    latex_content += "\\usepackage{fontawesome}\n"
    latex_content += "\\usepackage{titlesec}\n\n"
    latex_content += "\\titleformat{\\section}[hang]{\\Large\\bfseries}{}{0em}{}[]\n"
    latex_content += "\\titlespacing*{\\section}{0pt}{*1.5}{*1.5}\n"
    latex_content += "\\titlespacing*{\\subsection}{0pt}{*1.2}{*1.2}\n\n"
    latex_content += "\\begin{document}\n\n"
    
    basics = json_data.get("basics", {})
    latex_content += "\\begin{center}\n"
    latex_content += "\\textbf{\\Huge{" + basics.get("name", "") + "}}\\\\\n"
    latex_content += "\\textit{" + basics.get("label", "") + "}\\\\[5pt]\n"
    latex_content += "\\begin{minipage}[t]{0.5\\textwidth}\n"
    latex_content += "\\begin{flushleft}\n"
    latex_content += "\\faEnvelope\\hspace{2pt}" + basics.get("email", "") + "\\\\\n"
    latex_content += "\\faPhone\\hspace{2pt}" + basics.get("phone", "") + "\\\\\n"
    latex_content += "\\faGlobe\\hspace{2pt}\\href{" + basics.get("url", "") + "}{" + basics.get("url", "") + "}\n"
    latex_content += "\\end{flushleft}\n"
    latex_content += "\\end{minipage}\n"
    latex_content += "\\begin{minipage}[t]{0.5\\textwidth}\n"
    latex_content += "\\begin{flushright}\n"
    location = basics.get("location", {})
    if location:
        latex_content += location.get("city", "") + ", " + location.get("countryCode", "") + "\\\\\n"
    latex_content += "\\end{flushright}\n"
    latex_content += "\\end{minipage}\n"
    latex_content += "\\end{center}\n\n"
    
    work = json_data.get("work", [])
    if work:
        latex_content += "\\section{Work Experience}\n"
        for item in work:
            latex_content += "\\subsection{" + item.get("name", "") + " - " + item.get("position", "") + "}\n"
            latex_content += "\\textit{" + item.get("location", "") + " | " + item.get("startDate", "") + " -- " + item.get("endDate", "") + "}\\\\\n"
            latex_content += "\\textbf{" + item.get("summary", "") + "}\\\\\n"
            latex_content += "\\textbf{Highlights:}\n"
            latex_content += "\\begin{itemize}\n"
            for highlight in item.get("highlights", []):
                latex_content += "\\item " + highlight + "\n"
            latex_content += "\\end{itemize}\n\n"
    
    volunteer = json_data.get("volunteer", [])
    if volunteer:
        latex_content += "\\section{Volunteer Experience}\n"
        for item in volunteer:
            latex_content += "\\subsection{" + item.get("organization", "") + " - " + item.get("position", "") + "}\n"
            latex_content += "\\textit{" + item.get("startDate", "") + " -- " + item.get("endDate", "") + "}\\\\\n"
            latex_content += "\\textbf{" + item.get("summary", "") + "}\\\\\n"
            latex_content += "\\textbf{Highlights:}\n"
            latex_content += "\\begin{itemize}\n"
            for highlight in item.get("highlights", []):
                latex_content += "\\item " + highlight + "\n"
            latex_content += "\\end{itemize}\n\n"
    
    education = json_data.get("education", [])
    if education:
        latex_content += "\\section{Education}\n"
        for item in education:
            latex_content += "\\subsection{" + item.get("studyType", "") + " in " + item.get("area", "") + " at " + item.get("institution", "") + "}\n"
            latex_content += "\\textit{" + item.get("startDate", "") + " -- " + item.get("endDate", "") + "}\\\\\n"
            latex_content += "\\textbf{Score:} " + item.get("score", "") + "\\\\\n\n"
    
    awards = json_data.get("awards", [])
    if awards:
        latex_content += "\\section{Awards}\n"
        for item in awards:
            latex_content += "\\subsection{" + item.get("title", "") + "}\n"
            latex_content += "\\textit{" + item.get("date", "") + "}\\\\\n"
            latex_content += "\\textbf{Awarder:} " + item.get("awarder", "") + "\\\\\n"
            latex_content += "\\textbf{" + item.get("summary", "") + "}\\\\\n\n"
    
    publications = json_data.get("publications", [])
    if publications:
        latex_content += "\\section{Publications}\n"
        for item in publications:
            latex_content += "\\subsection{" + item.get("name", "") + "}\n"
            latex_content += "\\textit{" + item.get("releaseDate", "") + "}\\\\\n"
            latex_content += "\\textbf{Publisher:} " + item.get("publisher", "") + "\\\\\n"
            latex_content += "\\textbf{" + item.get("summary", "") + "}\\\\\n\n"
    
    skills = json_data.get("skills", [])
    if skills:
        latex_content += "\\section{Skills}\n"
        for skill in skills:
            latex_content += "\\textbf{" + skill.get("name", "") + ":} "
            latex_content += ", ".join(skill.get("keywords", [])) + "\n\n"
    
    languages = json_data.get("languages", [])
    if languages:
        latex_content += "\\section{Languages}\n"
        for lang in languages:
            latex_content += "\\textbf{" + lang.get("language", "") + ":} " + lang.get("fluency", "") + "\n\n"
    
    interests = json_data.get("interests", [])
    if interests:
        latex_content += "\\section{Interests}\n"
        for interest in interests:
            latex_content += interest.get("name", "") + ": "
            latex_content += ", ".join(interest.get("keywords", [])) + "\n\n"
    
    references = json_data.get("references", [])
    if references:
        latex_content += "\\section{References}\n"
        for ref in references:
            latex_content += "\\subsection{" + ref.get("name", "") + "}\n"
            latex_content += ref.get("reference", "") + "\n\n"

    certifications = json_data.get("certificates", [])
    if certifications:
        latex_content += "\\section{Certifications}\n"
        for cert in certifications:
            latex_content += "\\subsection{" + cert.get("name", "") + "}\n\n"
    
    latex_content += "\\end{document}"


    # print(latex_content)
    
    api_url = 'https://latexonline.cc/compile'
    api_call_url = api_url + "?text=" + latex_content
    webbrowser.open(api_call_url)





def generate_latex_resume3(json_data):
    latex_content = ""
    latex_content += "\\documentclass{article}\n"
    latex_content += "\\usepackage{hyperref}\n"
    latex_content += "\\usepackage{enumitem}\n"
    latex_content += "\\usepackage[left=0.5in,right=0.5in,top=0.5in,bottom=0.5in]{geometry}\n"
    latex_content += "\\usepackage{fontawesome}\n"
    latex_content += "\\usepackage{titlesec}\n\n"
    latex_content += "\\titleformat{\\section}[block]{\\bfseries\\filcenter\\Large\\sffamily}{}{0em}{}[]\n"
    latex_content += "\\titlespacing*{\\section}{0pt}{*2.5}{*1.5}\n"
    latex_content += "\\titlespacing*{\\subsection}{0pt}{*1.2}{*1.2}\n\n"
    latex_content += "\\begin{document}\n\n"
    
    basics = json_data.get("basics", {})
    latex_content += "\\begin{center}\n"
    latex_content += "\\textbf{\\Huge{" + basics.get("name", "") + "}}\\\\[5pt]\n"
    latex_content += "\\textit{" + basics.get("label", "") + "}\\\\[10pt]\n"
    latex_content += "\\begin{minipage}[t]{0.5\\textwidth}\n"
    latex_content += "\\begin{flushleft}\n"
    latex_content += "\\faEnvelope\\hspace{2pt}" + basics.get("email", "") + "\\\\\n"
    latex_content += "\\faPhone\\hspace{2pt}" + basics.get("phone", "") + "\\\\\n"
    latex_content += "\\faGlobe\\hspace{2pt}\\href{" + basics.get("url", "") + "}{" + basics.get("url", "") + "}\n"
    latex_content += "\\end{flushleft}\n"
    latex_content += "\\end{minipage}\n"
    latex_content += "\\begin{minipage}[t]{0.5\\textwidth}\n"
    latex_content += "\\begin{flushright}\n"
    location = basics.get("location", {})
    if location:
        latex_content += location.get("city", "") + ", " + location.get("countryCode", "") + "\\\\\n"
    latex_content += "\\end{flushright}\n"
    latex_content += "\\end{minipage}\n"
    latex_content += "\\end{center}\n\n"
    
    work = json_data.get("work", [])
    if work:
        latex_content += "\\section{Work Experience}\n"
        for item in work:
            latex_content += "\\subsection{" + item.get("name", "") + " - " + item.get("position", "") + "}\n"
            latex_content += "\\textit{" + item.get("location", "") + " | " + item.get("startDate", "") + " -- " + item.get("endDate", "") + "}\\\\\n"
            latex_content += "\\textbf{" + item.get("summary", "") + "}\\\\\n"
            latex_content += "\\textbf{Highlights:}\n"
            latex_content += "\\begin{itemize}\n"
            for highlight in item.get("highlights", []):
                latex_content += "\\item " + highlight + "\n"
            latex_content += "\\end{itemize}\n\n"
    
    volunteer = json_data.get("volunteer", [])
    if volunteer:
        latex_content += "\\section{Volunteer Experience}\n"
        for item in volunteer:
            latex_content += "\\subsection{" + item.get("organization", "") + " - " + item.get("position", "") + "}\n"
            latex_content += "\\textit{" + item.get("startDate", "") + " -- " + item.get("endDate", "") + "}\\\\\n"
            latex_content += "\\textbf{" + item.get("summary", "") + "}\\\\\n"
            latex_content += "\\textbf{Highlights:}\n"
            latex_content += "\\begin{itemize}\n"
            for highlight in item.get("highlights", []):
                latex_content += "\\item " + highlight + "\n"
            latex_content += "\\end{itemize}\n\n"
    
    education = json_data.get("education", [])
    if education:
        latex_content += "\\section{Education}\n"
        for item in education:
            latex_content += "\\subsection{" + item.get("studyType", "") + " in " + item.get("area", "") + " at " + item.get("institution", "") + "}\n"
            latex_content += "\\textit{" + item.get("startDate", "") + " -- " + item.get("endDate", "") + "}\\\\\n"
            latex_content += "\\textbf{Score:} " + item.get("score", "") + "\\\\\n\n"
    
    awards = json_data.get("awards", [])
    if awards:
        latex_content += "\\section{Awards}\n"
        for item in awards:
            latex_content += "\\subsection{" + item.get("title", "") + "}\n"
            latex_content += "\\textit{" + item.get("date", "") + "}\\\\\n"
            latex_content += "\\textbf{Awarder:} " + item.get("awarder", "") + "\\\\\n"
            latex_content += "\\textbf{" + item.get("summary", "") + "}\\\\\n\n"
    
    publications = json_data.get("publications", [])
    if publications:
        latex_content += "\\section{Publications}\n"
        for item in publications:
            latex_content += "\\subsection{" + item.get("name", "") + "}\n"
            latex_content += "\\textit{" + item.get("releaseDate", "") + "}\\\\\n"
            latex_content += "\\textbf{Publisher:} " + item.get("publisher", "") + "\\\\\n"
            latex_content += "\\textbf{" + item.get("summary", "") + "}\\\\\n\n"
    
    skills = json_data.get("skills", [])
    if skills:
        latex_content += "\\section{Skills}\n"
        for skill in skills:
            latex_content += "\\textbf{" + skill.get("name", "") + ":} "
            latex_content += ", ".join(skill.get("keywords", [])) + "\n\n"
    
    languages = json_data.get("languages", [])
    if languages:
        latex_content += "\\section{Languages}\n"
        for lang in languages:
            latex_content += "\\textbf{" + lang.get("language", "") + ":} " + lang.get("fluency", "") + "\n\n"
    
    interests = json_data.get("interests", [])
    if interests:
        latex_content += "\\section{Interests}\n"
        for interest in interests:
            latex_content += interest.get("name", "") + ": "
            latex_content += ", ".join(interest.get("keywords", [])) + "\n\n"
    
    references = json_data.get("references", [])
    if references:
        latex_content += "\\section{References}\n"
        for ref in references:
            latex_content += "\\subsection{" + ref.get("name", "") + "}\n"
            latex_content += ref.get("reference", "") + "\n\n"

    certifications = json_data.get("certificates", [])
    if certifications:
        latex_content += "\\section{Certifications}\n"
        for cert in certifications:
            latex_content += "\\subsection{" + cert.get("name", "") + "}\n\n"
    
    latex_content += "\\end{document}"
    
    # print(latex_content)
    api_url = 'https://latexonline.cc/compile'
    api_call_url = api_url + "?text=" + latex_content
    webbrowser.open(api_call_url)