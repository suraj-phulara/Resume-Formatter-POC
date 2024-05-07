from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict, List, Optional, Union



class Location(BaseModel):
    address: str = Field(description="Street address")
    postalCode: str = Field(description="Postal code")
    city: str = Field(description="City")
    countryCode: str = Field(description="Country code")
    region: str = Field(description="Region or state")

class Profile(BaseModel):
    network: str = Field(description="Social network or platform")
    username: str = Field(description="Username on the platform")
    url: str = Field(description="URL to the profile")

class Basics(BaseModel):
    name: str = Field(description="Full name")
    label: str = Field(description="Label or job title")
    image: Optional[str] = Field(description="URL to the image")
    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number")
    url: str = Field(description="URL to personal website or portfolio")
    summary: str = Field(description="Summary or bio")
    location: Location
    profiles: List[Profile]

class Work(BaseModel):
    name: str = Field(description="Company name")
    position: str = Field(description="Position held at the company")
    url: Optional[str] = Field(description="URL to the company's website")
    startDate: str = Field(description="Start date of employment")
    endDate: Optional[str] = Field(description="End date of employment")
    summary: str = Field(description="Description of responsibilities")
    highlights: List[str] = Field(description="List of achievements or highlights")

class Volunteer(BaseModel):
    organization: str = Field(description="Organization name")
    position: str = Field(description="Volunteer position")
    url: Optional[str] = Field(description="URL to the organization's website")
    startDate: str = Field(description="Start date of volunteering")
    endDate: Optional[str] = Field(description="End date of volunteering")
    summary: str = Field(description="Description of volunteer work")
    highlights: List[str] = Field(description="List of achievements or highlights")

class Education(BaseModel):
    institution: str = Field(description="Educational institution name")
    url: Optional[str] = Field(description="URL to the institution's website")
    area: str = Field(description="Area of study")
    studyType: str = Field(description="Type of degree or qualification")
    startDate: str = Field(description="Start date of education")
    endDate: Optional[str] = Field(description="End date of education")
    score: Optional[str] = Field(description="Grade or score achieved")
    courses: Optional[List[str]] = Field(description="List of relevant courses")

class Award(BaseModel):
    title: str = Field(description="Title of the award")
    date: str = Field(description="Date of receiving the award")
    awarder: str = Field(description="Organization or entity presenting the award")
    summary: str = Field(description="Brief summary of the award")

class Certificate(BaseModel):
    name: str = Field(description="Name of the certificate")
    date: str = Field(description="Date of obtaining the certificate")
    issuer: str = Field(description="Organization or entity issuing the certificate")
    url: Optional[str] = Field(description="URL to the certificate or issuer's website")

class Publication(BaseModel):
    name: str = Field(description="Name of the publication")
    publisher: str = Field(description="Publisher of the publication")
    releaseDate: str = Field(description="Release date of the publication")
    url: Optional[str] = Field(description="URL to the publication")
    summary: str = Field(description="Brief summary of the publication")

class Skill(BaseModel):
    name: str = Field(description="Name of the skill")
    level: str = Field(description="Proficiency level of the skill")
    keywords: List[str] = Field(description="List of related keywords or technologies")

class Language(BaseModel):
    language: str = Field(description="Language name")
    fluency: str = Field(description="Fluency level in the language")

class Interest(BaseModel):
    name: str = Field(description="Interest or hobby")
    keywords: List[str] = Field(description="List of related keywords or topics")

class Reference(BaseModel):
    name: str = Field(description="Name of the reference")
    reference: str = Field(description="Reference information or testimonial")

class Project(BaseModel):
    name: str = Field(description="Name of the project")
    startDate: str = Field(description="Start date of the project")
    endDate: Optional[str] = Field(description="End date of the project")
    description: str = Field(description="Description of the project")
    highlights: List[str] = Field(description="List of project highlights or achievements")
    url: Optional[str] = Field(description="URL to the project")

class Resume(BaseModel):
    basics: Basics
    work: List[Work]
    volunteer: Optional[List[Volunteer]]
    education: Optional[List[Education]]
    awards: Optional[List[Award]]
    certificates: Optional[List[Certificate]]
    publications: Optional[List[Publication]]
    skills: Optional[List[Skill]]
    languages: Optional[List[Language]]
    interests: Optional[List[Interest]]
    references: Optional[List[Reference]]
    projects: Optional[List[Project]]


class Rewrite(BaseModel):
    summary: str = Field(description="rephrashed summary in exactly same length")


















# class SocialMedia(BaseModel):
#     platform: str = Field(description="Social media platform")
#     username: str = Field(description="Username on the platform")
#     url: Optional[str] = Field(description="URL to the profile")

# class PersonalInfo(BaseModel):
#     name: str = Field(description="Full name")
#     email: str = Field(description="Email address")
#     phone: str = Field(description="Phone number")
#     address: Optional[str] = Field(description="Home address")
#     summary: Optional[Union[str, List[str]]] = Field(description="Summary information. Can be a single line, a paragraph, or a list of bullet points.")
#     social_media: Optional[Dict[str, str]] = Field(description="Dictionary of social media handles")

# class WorkExperience(BaseModel):
#     position: str = Field(description="Position held")
#     company: str = Field(description="Company name")
#     start_date: str = Field(description="Start date of employment")
#     end_date: Optional[str] = Field(description="End date of employment")
#     summary: Optional[Union[str, List[str]]] = Field(description="Brief description of responsibilities")

# class Education(BaseModel):
#     degree: str = Field(description="Degree obtained")
#     major: str = Field(description="Field of study")
#     institution: str = Field(description="Institution name")
#     graduation_date: str = Field(description="Graduation date")
#     grade: Optional[str] = Field(description="Percentage or grade achieved")

# class Skill(BaseModel):
#     name: str = Field(description="Skill name")
#     level: Optional[str] = Field(description="Proficiency level")

# class Interest(BaseModel):
#     name: str = Field(description="Interest or hobby")

# class Project(BaseModel):
#     name: str = Field(description="Project name")
#     start_date: str = Field(description="Start date of the project")
#     end_date: Optional[str] = Field(description="End date of the project")
#     description: str = Field(description="Description of the project")
#     highlights: Optional[List[str]] = Field(description="List of project highlights or achievements")
#     url: Optional[str] = Field(description="URL to the project")

# class Resume(BaseModel):
#     personal_info: PersonalInfo
#     work_experience: Optional[List[WorkExperience]] = Field(description="List of work experiences")
#     education: Optional[List[Education]] = Field(description="List of educational qualifications")
#     skills: Optional[List[Skill]] = Field(description="List of skills")
#     interests: Optional[List[Interest]] = Field(description="List of interests")
#     projects: Optional[List[Project]] = Field(description="List of projects")
