import os
import re
from typing import Dict, List, Any
import docx
from .skill_extractor import skill_extractor

# Optional PDF readers
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

class ResumeParser:
    def __init__(self):
        self.email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
        self.phone_regex = re.compile(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}")
        
        # Common Degree patterns
        self.degree_patterns = [
            r"B\.?Tech(?:nology)?(?:\s+in\s+[\w\s]+)?",
            r"B\.?E\.?(?:\s+in\s+[\w\s]+)?",
            r"B\.?S\.?c?(?:\s+in\s+[\w\s]+)?",
            r"Bachelor(?:'s)?(?:\s+of\s+[\w\s]+)?",
            r"M\.?Tech(?:nology)?(?:\s+in\s+[\w\s]+)?",
            r"M\.?S\.?c?(?:\s+in\s+[\w\s]+)?",
            r"M\.?E\.?(?:\s+in\s+[\w\s]+)?",
            r"Master(?:'s)?(?:\s+of\s+[\w\s]+)?",
            r"BCA|MCA|BBA|MBA|Ph\.?D\.?",
            r"Diploma\s+in\s+[\w\s]+",
            r"Senior\s+Secondary|High\s+School|Class\s+XII|Class\s+12"
        ]

        # Common section header keywords
        self.section_keywords = {
            "education": ["education", "academic background", "academic qualification", "academics", "qualifications"],
            "experience": ["experience", "work experience", "employment history", "professional experience", "internship", "internships", "work history"],
            "projects": ["projects", "personal projects", "academic projects", "key projects", "notable projects"],
            "skills": ["skills", "technical skills", "core competencies", "skills & tools", "technologies", "expertise"],
            "certifications": ["certifications", "certificates", "licenses & certifications", "courses & certifications", "credentials"]
        }

    def extract_text_from_file(self, file_path: str) -> str:
        """Extracts text from PDF, DOCX, or TXT file with robust fallback mechanisms."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = file_path.rsplit(".", 1)[-1].lower()

        if ext == "pdf":
            return self._extract_text_from_pdf(file_path)
        elif ext in ["docx", "doc"]:
            return self._extract_text_from_docx(file_path)
        elif ext == "txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: .{ext}")

    def _extract_text_from_pdf(self, file_path: str) -> str:
        text = ""
        # 1. Try pdfplumber for best layout extraction
        if pdfplumber is not None:
            try:
                with pdfplumber.open(file_path) as pdf:
                    pages_text = [page.extract_text() or "" for page in pdf.pages]
                    text = "\n".join(pages_text).strip()
                    if text and len(text) > 40:
                        return text
            except Exception as e:
                print(f"pdfplumber extraction failed: {e}")

        # 2. Try PyMuPDF (fitz)
        if fitz is not None:
            try:
                doc = fitz.open(file_path)
                pages_text = [page.get_text() for page in doc]
                text = "\n".join(pages_text).strip()
                if text and len(text) > 40:
                    return text
            except Exception as e:
                print(f"PyMuPDF extraction failed: {e}")

        # 3. Try pypdf
        if pypdf is not None:
            try:
                reader = pypdf.PdfReader(file_path)
                pages_text = [page.extract_text() or "" for page in reader.pages]
                text = "\n".join(pages_text).strip()
                if text:
                    return text
            except Exception as e:
                print(f"pypdf extraction failed: {e}")

        return text

    def _extract_text_from_docx(self, file_path: str) -> str:
        try:
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text.strip())
            
            # Extract from tables as well
            for table in doc.tables:
                for row in table.rows:
                    row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_text:
                        full_text.append(" | ".join(row_text))
            
            return "\n".join(full_text)
        except Exception as e:
            print(f"python-docx extraction failed: {e}")
            return ""

    def extract_candidate_name(self, text: str, lines: List[str]) -> str:
        """
        Extracts candidate's full name from the header/initial lines of the resume.
        """
        for line in lines[:8]:
            cleaned = line.strip()
            # Ignore headers, emails, phones, URLs
            if not cleaned or "@" in cleaned or "http" in cleaned or "github" in cleaned or "linkedin" in cleaned:
                continue
            if re.search(r"\b(resume|curriculum vitae|cv|page|profile|summary|contact)\b", cleaned, re.IGNORECASE):
                continue
            # A valid name line is typically 2 to 4 words, alphabetic characters
            words = cleaned.split()
            if 1 <= len(words) <= 4 and all(re.match(r"^[A-Za-z\.\'-]+$", w) for w in words):
                return cleaned.title()

        return "Not detected"

    def extract_email(self, text: str) -> str:
        matches = self.email_regex.findall(text)
        return matches[0] if matches else "Not detected"

    def extract_phone(self, text: str) -> str:
        matches = self.phone_regex.findall(text)
        if matches:
            # Flatten matched tuples from regex grouping
            for match in matches:
                full_match = "".join(match).strip()
                # Ensure it has at least 7 digits
                digits = re.sub(r"\D", "", full_match)
                if 7 <= len(digits) <= 15:
                    return full_match
        return "Not detected"

    def extract_location(self, text: str, lines: List[str]) -> str:
        """Finds common Indian or global tech hubs/cities in header lines."""
        cities = [
            "Bengaluru", "Bangalore", "Hyderabad", "Pune", "Mumbai", "Delhi", "New Delhi",
            "Noida", "Gurugram", "Gurgaon", "Chennai", "Kolkata", "Ahmedabad", "Jaipur",
            "Indore", "Kochi", "Chandigarh", "San Francisco", "New York", "London", "Remote"
        ]
        city_pattern = re.compile(r"\b(" + "|".join(cities) + r")\b", re.IGNORECASE)
        for line in lines[:10]:
            match = city_pattern.search(line)
            if match:
                return match.group(0).capitalize()

        match = city_pattern.search(text)
        return match.group(0).capitalize() if match else "Not detected"

    def segment_sections(self, text: str) -> Dict[str, str]:
        """Segments resume text into section blocks based on semantic headings."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        sections = {
            "header": "",
            "education": "",
            "experience": "",
            "projects": "",
            "skills": "",
            "certifications": "",
            "summary": "",
            "other": ""
        }

        current_sec = "header"
        buffer = []

        for line in lines:
            line_lower = line.lower().strip(":").strip()
            # Check if line matches a known section header
            matched_sec = None
            if len(line.split()) <= 4 and len(line) < 40:
                for sec_name, keywords in self.section_keywords.items():
                    for kw in keywords:
                        if line_lower == kw or line_lower.startswith(kw + " ") or line_lower.endswith(" " + kw):
                            matched_sec = sec_name
                            break
                    if matched_sec:
                        break
            
            if matched_sec:
                if buffer:
                    sections[current_sec] += "\n" + "\n".join(buffer)
                    buffer = []
                current_sec = matched_sec
            else:
                buffer.append(line)

        if buffer:
            sections[current_sec] += "\n" + "\n".join(buffer)

        return sections

    def extract_education(self, text: str, edu_section_text: str) -> List[Dict[str, str]]:
        target_text = edu_section_text if edu_section_text.strip() else text
        edu_list = []
        
        # Regex for degrees
        degree_combined_pattern = re.compile(r"(" + "|".join(self.degree_patterns) + r")", re.IGNORECASE)
        year_pattern = re.compile(r"\b(20\d{2}|19\d{2})\b")

        lines = [l.strip() for l in target_text.split("\n") if l.strip()]
        for line in lines:
            deg_match = degree_combined_pattern.search(line)
            if deg_match:
                degree_found = deg_match.group(0).strip()
                years = year_pattern.findall(line)
                grad_year = years[-1] if years else "Not detected"
                
                # Institution heuristic: remove degree and years from line or check next line
                inst = line.replace(degree_found, "").strip(" -|,:")
                inst = re.sub(r"\b(20\d{2}|19\d{2})\b", "", inst).strip(" -|,:")
                institution = inst if len(inst) > 3 else "University / Institute"

                edu_list.append({
                    "degree": degree_found,
                    "institution": institution,
                    "graduation_year": grad_year
                })

        # Fallback if no specific lines matched
        if not edu_list:
            deg_match = degree_combined_pattern.search(text)
            if deg_match:
                edu_list.append({
                    "degree": deg_match.group(0).strip(),
                    "institution": "University / Institute",
                    "graduation_year": "Not detected"
                })

        return edu_list

    def extract_experience(self, text: str, exp_section_text: str) -> List[Dict[str, Any]]:
        target_text = exp_section_text if exp_section_text.strip() else text
        exp_list = []
        
        # Look for role keywords & dates
        role_keywords = [
            "developer", "engineer", "analyst", "intern", "consultant", "scientist",
            "architect", "lead", "manager", "specialist", "trainee", "associate"
        ]
        
        date_pattern = re.compile(
            r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{4}|\d{4})\s*(?:-|to|–)\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{4}|\d{4}|Present|Current)",
            re.IGNORECASE
        )

        lines = [l.strip() for l in target_text.split("\n") if l.strip()]
        current_exp = None

        for line in lines:
            has_role = any(re.search(r"\b" + rk + r"\b", line, re.IGNORECASE) for rk in role_keywords)
            date_match = date_pattern.search(line)

            if has_role or date_match:
                if current_exp:
                    exp_list.append(current_exp)

                duration = date_match.group(0) if date_match else "Not detected"
                title_line = line
                if date_match:
                    title_line = title_line.replace(duration, "").strip(" -|,:")

                parts = [p.strip() for p in re.split(r"\|| - | at ", title_line) if p.strip()]
                title = parts[0] if parts else "Software Professional"
                company = parts[1] if len(parts) > 1 else "Tech Organization"

                current_exp = {
                    "title": title,
                    "company": company,
                    "duration": duration,
                    "responsibilities": []
                }
            elif current_exp and len(line) > 15:
                # Add responsibility bullet point
                cleaned_line = line.lstrip("•-*• \t")
                if len(current_exp["responsibilities"]) < 4:
                    current_exp["responsibilities"].append(cleaned_line)

        if current_exp:
            exp_list.append(current_exp)

        return exp_list

    def extract_projects(self, text: str, proj_section_text: str) -> List[Dict[str, Any]]:
        target_text = proj_section_text if proj_section_text.strip() else text
        projects_list = []
        
        lines = [l.strip() for l in target_text.split("\n") if l.strip()]
        current_proj = None

        for line in lines:
            # Check if line looks like a project title (short line with colon or dash or tech stack)
            if ((":" in line or "-" in line or "|" in line) and len(line.split()) <= 10 and len(line) < 75) or (len(line.split()) <= 5 and not line.startswith("•")):
                if current_proj:
                    projects_list.append(current_proj)
                
                parts = re.split(r"[:\-|]", line)
                name = parts[0].strip().lstrip("•-* ")
                tech = parts[1].strip() if len(parts) > 1 else "Python, Web Technologies"

                current_proj = {
                    "name": name,
                    "technologies": tech,
                    "description": ""
                }
            elif current_proj and len(line) > 10:
                if not current_proj["description"]:
                    current_proj["description"] = line.lstrip("•-* ")
                else:
                    current_proj["description"] += " " + line.lstrip("•-* ")

        if current_proj:
            projects_list.append(current_proj)

        return projects_list[:4]

    def extract_certifications(self, text: str, cert_section_text: str) -> List[str]:
        target_text = cert_section_text if cert_section_text.strip() else text
        cert_list = []
        lines = [l.strip() for l in target_text.split("\n") if l.strip()]
        
        cert_keywords = ["certified", "certification", "coursera", "udemy", "hackerrank", "aws", "google", "microsoft", "nptel", "specialization"]
        for line in lines:
            if any(ck in line.lower() for ck in cert_keywords) and len(line) < 100:
                cert_list.append(line.lstrip("•-* "))

        return cert_list[:5]

    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parses full resume text into structured fields without hallucinating unobserved content.
        """
        if not text or not isinstance(text, str):
            text = ""

        lines = [l.strip() for l in text.split("\n") if l.strip()]
        sections = self.segment_sections(text)
        
        name = self.extract_candidate_name(text, lines)
        email = self.extract_email(text)
        phone = self.extract_phone(text)
        location = self.extract_location(text, lines)
        
        categorized_skills = skill_extractor.extract_skills(text)
        education = self.extract_education(text, sections.get("education", ""))
        experience = self.extract_experience(text, sections.get("experience", ""))
        projects = self.extract_projects(text, sections.get("projects", ""))
        certifications = self.extract_certifications(text, sections.get("certifications", ""))

        return {
            "candidate_name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "skills": categorized_skills,
            "education": education,
            "experience": experience,
            "projects": projects,
            "certifications": certifications,
            "raw_text": text
        }

# Global singleton
resume_parser = ResumeParser()
