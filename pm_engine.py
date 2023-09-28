# -*- coding: utf-8 -*-
"""

@author: chris

\f = new page
\a = new paragraph

"""


from docxtpl import DocxTemplate, InlineImage
#from pyxml2pdf import xml2pdf 

import pandas as pd
import re
import random
import string

import spacy
nlp = spacy.load("en_core_web_sm")

def descr_independent_claim_1(_claim_df):
    descr_claim_ = _claim_df["claims"].split('\n')

    # first line
    descr_claim_first_line = descr_claim_[0].split(',')

    templates_first_line = ['{0} is provided. ', '{0} is disclosed. ', 'The present invention relates to {0}. ']
    first_line = random.choice(templates_first_line).format(descr_claim_first_line[0]).capitalize()

    # start of second line
    position = [descr_claim_.index(s) for s in descr_claim_ if "comprising" in s]
    # print(position) hier unterschied "comprising" oder "comprise"
    start_second_line = position[0]+1

    # second lines
    descr_claim_second_line = descr_claim_[start_second_line].replace(',', '')
    templates_second_line = ['The method comprises {0}.']
    second_line = random.choice(templates_second_line).format(descr_claim_second_line).capitalize()

    # other lines
    other_lines_all = ''
    for i in range(start_second_line+1, len(descr_claim_)):
        # print(i)
        descr_claim_other_lines = descr_claim_[i].replace(',', '')
        templates_other_lines = ['The method also comprises {0}.', 'Furthermore, the method comprises {0}.']
        other_line = random.choice(templates_other_lines).format(descr_claim_other_lines).capitalize()
        
        # print(other_line)
        other_lines_all += ' '+ other_line
        
    # definitions and examples
    definitions_features = ''
    for new_def in _claim_df["definitions"]:
        templates_definitions = ['By {0} any kind of (placeholder) may be meant.']
        definitions_features += random.choice(templates_definitions).format(new_def).capitalize() + "\a"
        templates_examples = ['{0} may be, for example,', 'For example, {0} may be']
        definitions_features += random.choice(templates_examples).format(new_def).capitalize() + "\a"
        
    return first_line + second_line + other_lines_all + "\a" + definitions_features + "One advantage of" + "\a"

def descr_independent_claim(descr_claim_):
    
    
    if "method" in descr_claim_:
        descr_claim_ = descr_claim_.split('\n')
        # first line
        descr_claim_first_line = descr_claim_[0].split(',')
    
        templates_first_line = ['The present invention also relates to {0}. ']
        first_line = random.choice(templates_first_line).format(descr_claim_first_line[0]).capitalize()
    
        # start of second line
        position = [descr_claim_.index(s) for s in descr_claim_ if "comprising" in s]
        start_second_line = position[0]+1
    
        # second lines
        descr_claim_second_line = descr_claim_[start_second_line].replace(',', '')
        templates_second_line = ['The method comprises {0}.']
        second_line = random.choice(templates_second_line).format(descr_claim_second_line).capitalize()
    
        # other lines
        other_lines_all = ''
        for i in range(start_second_line+1, len(descr_claim_)):
            # print(i)
            descr_claim_other_lines = descr_claim_[i].replace(',', '')
            templates_other_lines = ['The method also comprises {0}.', 'Furthermore, the method comprises {0}.']
            other_line = random.choice(templates_other_lines).format(descr_claim_other_lines).capitalize()
            
            # print(other_line)
            other_lines_all += ' '+ other_line
            
        all_lines = first_line + second_line + other_lines_all 
        
    else:
        templates_first_line = ['The present invention also relates to {0}. ']
        all_lines = random.choice(templates_first_line).format(descr_claim_).capitalize()

        
    return all_lines + "\a" + "One advantage of" + "\a"

def descr_dependent_claim(_claim_df):
    claim_ = ''
    if "the method further comprises" in _claim_df:
       claim_ = _claim_df
       #print(j, claim_)
    
    else:
        descr_claim_ = _claim_df.split('\n')
        print(descr_claim_)
        if len(descr_claim_)>1:
            claim_features = descr_claim_[1].replace(',', '')
            templates_other_lines = ['In one aspect, {0}.']
            claim_f_0 = random.choice(templates_other_lines).format(claim_features).capitalize()
            
            claim_f_0 = claim_f_0.replace('comprises', 'may comprise')
            claim_f_0 = claim_f_0.replace(' is ', ' may be ')
            claim_f_0 = claim_f_0.replace(' are ', ' may be ')
            claim_f_0 = claim_f_0.replace(' has ', ' may have ')
            claim_f_0 = claim_f_0.replace(' have ', ' may have ')
            claim_ += claim_f_0 
            
            for i in range(2, len(descr_claim_)):
                # print(i)
                claim_features = descr_claim_[i].replace(',', '')
                templates_other_lines = ['Furthermore, {0}.']
                claim_f = random.choice(templates_other_lines).format(claim_features).capitalize()
                
                claim_f = claim_f.replace('comprises', 'may comprise')
                claim_f = claim_f.replace(' is ', ' may be ')
                claim_f = claim_f.replace(' are ', ' may be ')
                claim_f = claim_f.replace(' has ', ' may have ')
                claim_f = claim_f.replace(' have ', ' may have ')
                claim_ += ' ' + claim_f
        else:
            claim_ = descr_claim_[0]
        #print(j, claim_)
    
    return claim_ + "\a" + "One advantage of" + "\a"

def build_application(claims_input):
    # Loading template

    template = DocxTemplate('template_patentapplication.docx')
    
    # Loading claims
    #my_file = open("/root/Desktop/claims_clean.txt", "r")
    #claim_data = my_file.read()
    claim_data = claims_input
    
    
    ##################################################
    ##################################################
    # Claim processing
    
    # Claim for template
    claim_data_for_templ = re.sub(r'\n\n\d. ', '\a', claim_data)
    claim_data_for_templ = re.sub(r'\n\n\d\d. ', '\a', claim_data_for_templ)
    claim_data_for_templ = claim_data_for_templ.replace('1. ', '')
    
    claim_data_proc = re.sub(r'\n\n\d. ', '', claim_data)
    claim_data_proc = re.sub(r'\n\n\d\d. ', '', claim_data_proc)
    claim_data_proc = claim_data_proc.replace('1. ', '')
    
    data_into_list = claim_data_proc.split('.')
    data_into_list = list(filter(None, data_into_list))
    
    
    claim_df = pd.DataFrame({"claims":data_into_list})
    #claim_df = claim_df[claim_df['claims']!=""]
    
    # claim number
    claim_df["claim_number"] = list(range(1,len(claim_df["claims"])+1))
    
    
    # dependency
    dependency_claims = []
    for txt in data_into_list:
        txt = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', txt)
        #print(txt)
        if "preceding claims" in txt:
            dependency_claims.append(["all preceding"])
        elif "preceding claim" in txt:
            dependency_claims.append(["previous claim"])
        else:
            a = [int(s) for s in txt.split() if s.isdigit()]
            if a == []:
                dependency_claims.append(["independent"])
            else:
                dependency_claims.append(a)
        
    claim_df["dependency"] = dependency_claims
    
    
    # dependency numbers
    dependency_claims_numbers = []
    cur_num = 1
    for dep in claim_df["dependency"]:
        if dep == ["all preceding"]:
            dependency_claims_numbers.append(list(range(1, cur_num)))
        elif dep == ["previous claim"]:
            dependency_claims_numbers.append([cur_num-1])
        else:
            dependency_claims_numbers.append(dep)
        cur_num += 1
            
    claim_df["dependency_num"] = dependency_claims_numbers
        
    
    ### nouns and definitions of claim
    nouns_claims = []
    definitions_claims = []
    
    #definitions_det = ["a ", "an "]
    for i in range(0, len(claim_df["claims"])):
        cl = claim_df["claims"][i]
        doc = nlp(cl)
        chunks_list = []
        definition_list = []
        # list(doc.noun_chunks)
        for noun_chunk in doc.noun_chunks:
            chunks_list.append(noun_chunk.text)
            if "a" == noun_chunk.text[0]:
                definition_list.append(noun_chunk.text)
            elif "an" == noun_chunk.text[:1]:
                definition_list.append(noun_chunk.text)
            else:
                pass
                
        nouns_claims.append(chunks_list)
        definitions_claims.append(definition_list)
        
    claim_df["nouns"] = nouns_claims
    claim_df["definitions"] = definitions_claims
    
    
    ##################################################
    ##################################################
    # Description processing
    
    ##################################################
    # claim 1
    summary = descr_independent_claim_1(claim_df.iloc[0])
    # summary = ""
    
    # hier jetzt df
    
    ##################################################
    #claim 2 and others
    for j in range(1, len(claim_df)):    
        #if "a system" in data_into_list[j].lower():
            #print(j, data_into_list[j])
        if claim_df["dependency"].iloc[j]== ["independent"]:
            summary += descr_independent_claim(claim_df["claims"].iloc[j])
            #print(data_into_list[j])
        else:
            summary += descr_dependent_claim(claim_df["claims"].iloc[j])
    
    
    
    ##################################################
    ##################################################
    # Data
    
    _docket_number = "XXX EP"
    _title = "A method of obtaining a system"
    
    _background = "background"
    
    _summary = summary
    
    _claims = claim_data_for_templ
    
    # _claims_trans = GoogleTranslator(source='auto', target='fr').translate(claim_data_for_templ)
    # _claims += '\f' + _claims_trans
    
    _abstract = "abstract"
    
    ##################################################
    ##################################################
    
    #Declare template variables
    context = {
        'docketnumber': _docket_number,
        'title':        _title,
        'background':   _background,
        'summary':      _summary,
        'claims':       _claims,
        'abstract':     _abstract,
        # 'fig':          imagen
        }
    
    
    # Rendering
    template.render(context)
    
    # Saving
    template.save('patent_application.docx')
    #template.save('/root/Desktop/patent_application.docx')
    #template.write_xml('/root/Desktop/patent_application.xml')
    #xml2pdf.genpdf('/root/Desktop/patent_application.xml', '/root/Desktop/patent_application.pdf')





