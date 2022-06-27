import pdftotext
import openai
import re
import logging
import json

class ResumeParser():
    def __init__(self, OPENAI_API_KEY):
        # set GPT-3 API key from the environment vairable
        openai.api_key = OPENAI_API_KEY
        # GPT-3 completion questions
        self.questions = \
"""Summarize the text below into a JSON with exactly the following structure {basic_info: {first_name, last_name, full_name, email, phone_number, location, portfolio_website_url, 
linkedin_url, github_main_page_url, university, education_level (BS, MS, or PhD), graduation_year, graduation_month, majors, GPA}, 
work_experience: [{job_title, company, location, duration, job_summary}], Research: [{title, company/university, location, duration, job_summary}], Seminars:[{university, event, month, year}]}
"""
       # set up this parser's logger
        logging.basicConfig(filename='logs/parser.log', level=logging.DEBUG)
        self.logger = logging.getLogger()

    def page2string(self, page):
        page_str = "\n\n".join([page])
        page_str = re.sub('\s[,.]', ',', page_str)
        page_str = re.sub('[\n]+', '\n', page_str)
        page_str = re.sub('[\s]+', ' ', page_str)
        page_str = re.sub('http[s]?(://)?', '', page_str)
        return page_str

    def query_completion(self, prompt, engine = 'text-curie-001', temperature = 0.0, max_tokens = 100, top_p = 1, frequency_penalty = 0, presence_penalty = 0):
        self.logger.info(f'query_completion: using {engine}')
        estimated_prompt_tokens = int(len(prompt.split()) * 1.6)
        self.logger.info(f'estimated prompt tokens: {estimated_prompt_tokens}')
        estimated_answer_tokens = 2049 - estimated_prompt_tokens
        if estimated_answer_tokens < max_tokens:
            self.logger.warning('estimated_answer_tokens lower than max_tokens, changing max_tokens to', estimated_answer_tokens)
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=min(4096-estimated_prompt_tokens, max_tokens),
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return response

    def merge(self, d1, d2):
        result = dict(d1)
        for k,v in d2.items():
            if k in result:
                if result[k] == "":
                    result[k] = v
            else:
                result[k] = v
        return result

    def query_resume(self, pdf_path):
        resume = {}
        max_tokens = 1500
        engine = 'text-davinci-002'
        with open(pdf_path, "rb") as f:
            pdf = pdftotext.PDF(f)
        for page in pdf:
            page_str = self.page2string(page)
            prompt = self.questions + '\n' + page_str
            response = self.query_completion(prompt, engine=engine, max_tokens=max_tokens)
            response_str = response['choices'][0]['text'].strip()
            print(response_str)
            temp_resume = json.loads(response_str)
            resume = self.merge(resume, temp_resume)
        return resume