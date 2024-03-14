
import streamlit as st
import re
import json
import openai
import warnings

import requests

warnings.filterwarnings('ignore')

api = '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'

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api,
}
url = "https://api.openai.com/v1/chat/completions"


# Client = openai.OpenAI()

class question_and_answers():
    input_text = ""
    no_correct = 1

    template_1 ='''
    paragraph: India, officially known as the Republic of India, is a diverse and vibrant country located in South Asia. 
    It is the seventh-largest country in the world by land area and the second-most populous, home to over 1.3 billion people 
    representing various cultures, languages, and religions.
    
    India's rich history dates back thousands of years, and it has been a cradle of ancient civilizations and the birthplace of 
    several major religions, including Hinduism, Buddhism, Jainism, and Sikhism. India boasts a mesmerizing tapestry of landscapes, 
    from the snow-capped Himalayas in the north to the lush tropical forests in the south. The country is renowned for its cultural heritage, 
    with magnificent architectural marvels such as the Taj Mahal, an epitome of love, and the historic forts and palaces that narrate stories of its illustrious past. 

    Question 01 : What kind of country is India? 
    a. Diverse 
    b. Non-Vibrant 
    c. Monotonous 
    d. Dull
    Correct Option : a

    Question 02 : Population of India is greater than? 
    a. 1.0 billion 
    b. 1.2 Billion 
    c. 1.3 Billion 
    d. 1.4 Billion 
    Correct Option : c

    Question 03 : What is India called as?  
    a. Cradle of modren world 
    b. Cradle of Ancient civilization 
    c. Cradle of Innovation 
    d. Cradle of Invention 
    Correct Options: b 

    Question 04 : Where in India is Himalayas located? 
    a. South 
    b. West 
    c. North-East 
    d. North 
    Correct Options: d
    '''
    template_2 ='''
    paragraph: India, officially known as the Republic of India, is a diverse and vibrant country located in South Asia. 
    It is the seventh-largest country in the world by land area and the second-most populous, home to over 1.3 billion people 
    representing various cultures, languages, and religions.
    
    India's rich history dates back thousands of years, and it has been a cradle of ancient civilizations and the birthplace of 
    several major religions, including Hinduism, Buddhism, Jainism, and Sikhism. India boasts a mesmerizing tapestry of landscapes, 
    from the snow-capped Himalayas in the north to the lush tropical forests in the south. The country is renowned for its cultural heritage, 
    with magnificent architectural marvels such as the Taj Mahal, an epitome of love, and the historic forts and palaces that narrate stories of its illustrious past. 

    Question 01 : What kind of country is India? 
    a. Diverse 
    b. Vibrant 
    c. Monotonous 
    d. Dull
    Correct Options :(a) & (b)

    Question 02 : Population of India is greater than? 
    a. 1.0 billion 
    b. 1.2 Billion 
    c. 1.3 Billion 
    d. 1.4 Billion 
    Correct Options : (b) & (c)

    Question 03 : What is India called as?  
    a. Cradle of modren world 
    b. Cradle of Ancient civilization 
    c. Cradle of Innovation 
    d. Cradle of Invention 
    Correct Options: (b) & (c) 

    Question 04 : Where in India is Himalayas located? 
    a. South 
    b. West 
    c. North-East 
    d. North 
    Correct Options: (c) & (d)
    '''
    template_3 ='''
    paragraph: India, officially known as the Republic of India, is a diverse and vibrant country located in South Asia. 
    It is the seventh-largest country in the world by land area and the second-most populous, home to over 1.3 billion people 
    representing various cultures, languages, and religions.
    
    India's rich history dates back thousands of years, and it has been a cradle of ancient civilizations and the birthplace of 
    several major religions, including Hinduism, Buddhism, Jainism, and Sikhism. India boasts a mesmerizing tapestry of landscapes, 
    from the snow-capped Himalayas in the north to the lush tropical forests in the south. The country is renowned for its cultural heritage, 
    with magnificent architectural marvels such as the Taj Mahal, an epitome of love, and the historic forts and palaces that narrate stories of its illustrious past. 

    Question 01 : What kind of country is India? 
    a. Diverse 
    b. Vibrant 
    c. Monotonous 
    d. Dull

    Question 02 : Population of India is greater than? 
    a. 1.0 billion 
    b. 1.2 Billion 
    c. 1.3 Billion 
    d. 1.4 Billion 

    Question 03 : What is India called as?  
    a. Cradle of modren world 
    b. Cradle of Ancient civilization 
    c. Cradle of Innovation 
    d. Cradle of Invention 
    

    Question 04 : Where in India is Himalayas located? 
    a. South 
    b. West 
    c. North-East 
    d. North 
    
    '''

    query = f'''Please stick to the following instructions while generating the response \
    - Generate only 10 questions 
    - With 1 correct answer for each and every question 
    - Please return the question and answers in the same format as specified in the template that is passed as reference for response generation. 
    - Please mandatorily add a question mark at the end of every question. 
    - Please compulsorily generate only specified number of options as answers, dont generate 4 options everytime as default'''

    payload = None
    input1 = None
    input2 = None
    input3 = None

    def __init__(self, input_text) -> None:
        self.input_text = input_text
        # self.no_correct = no_correct

        input1 = input_text.split('\n')
        input1 = [para for para in input1 if para.strip()]
        merged_paras = " ".join(input1)
        self.input2 = 'Paragraph' + merged_paras
        # if no_correct == 1:
        self.input3 = self.template_1 + self.query + self.input2
        # else :
        # self.input3 = self.template_2 + self.query + self.input2
            

    def getResponse(self):
        self.payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": self.input3},
            ],
        }
        response = requests.post(url, headers=headers, json=self.payload)

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"Error: {response.status_code}, {response.text}")
    
    # items = getResponse().split('\n')
    # for i in items:
    #     st.write(i)

    
  
if __name__ == "__main__":
    
    st.set_page_config(layout="wide")
    col004, col005, col006 = st.columns([100,300,100])
    with col005:
        st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                    .custom-text-01 { font-family: 'Agdasima', sans-serif; font-size: 70px;color:cyan }
                    </style>
                    <h2 class="custom-text-01">Module 1</h2>
                    """, unsafe_allow_html=True)
    st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                    .custom-text-02 { font-family: 'Perpetua', sans-serif; font-size: 30px;color:  #f9e79f   }
                    </style>
                    <p class="custom-text-02"> Tamil Language and Literature </p>
                    """, unsafe_allow_html=True)
    st.write('')
    st.markdown('<div style="text-align: justify"> Tamil literature boasts a rich heritage spanning over two millennia, showcasing a diverse array of literary works from various periods. Originating from the Tamil people in South India, including Tamil Nadu, Kerala, Sri Lankan Eelam Tamils, and the Tamil diaspora, it reflects the region\'s social, cultural, and political evolution. The early Sangam literature predating 300 BCE comprises anthologies covering love, war, social values, and religion. Subsequent periods saw the emergence of devotional poems by Alvars and Nayanmars, marking the Bhakti movement, and the patronage of literary classics by imperial Chola and Pandya empires.  </div>', unsafe_allow_html=True)
    st.write('')
    st.markdown('<div style="text-align: justify"> From the late 19th century, a literary revival occurred, characterized by works accessible to the masses. Influential figures like Subramania Bharathi spearheaded the modern Tamil literary movement, leading to the proliferation of prose, short stories, and novels. Sangam literature, although some lost, provides insights into ancient Tamil civilization, its governance, trade, and societal norms. Tolkappiyam, a foundational text, not only addresses grammar but also classifies habitats, animals, and human behavior, reflecting the organized evolution of the Tamil language and society.  </div>', unsafe_allow_html=True)
    st.write('')
    st.markdown('<div style="text-align: justify"> The Sangam age, considered Tamil\'s golden era, witnessed a flourishing of literature under the Chera, Pandya, and Chola dynasties. Poets enjoyed considerable freedom in their relationship with rulers, often critiquing them. The division of literature into \'subjective\' and \'objective\' topics facilitated nuanced discussions on love, governance, and societal norms within prescribed conventions. The classification of land into genres like forests, mountains, and seashores provided rich imagery for poetic expression.  </div>', unsafe_allow_html=True)
    st.write('')
    st.markdown('<div style="text-align: justify"> Religion played a significant role in Tamil literature, with Vaishnavism and Kaumaram being prominent. Mayon (Vishnu) and Cēyōṉ (Murugan) were revered deities, with Sangam literature extolling their attributes. The Paripādal anthology, focusing on love, glorified Perumal (Vishnu) as the supreme deity, while Murugan was celebrated as the youthful god. Shiva and Brahma were seen as forms of Maha Vishnu, highlighting Vishnu\'s supremacy in Tamil religious beliefs.</div>', unsafe_allow_html=True)
    st.write('')
    st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                    .custom-text-02 { font-family: 'Baskerville', sans-serif; font-size: 30px;color:  #f7dc6f}
                    </style>
                    <p class="custom-text-02"> Attempt the following MCQs </p>
                    """, unsafe_allow_html=True)
    

    
    input_text = '''Tamil literature boasts a rich heritage spanning over two millennia, showcasing a diverse array of literary works from various
    periods. Originating from the Tamil people in South India, including Tamil Nadu, Kerala, Sri Lankan Eelam Tamils, and the Tamil diaspora, it 
    reflects the regions social, cultural, and political evolution. The early Sangam literature predating 300 BCE comprises anthologies covering
    love, war, social values, and religion. Subsequent periods saw the emergence of devotional poems by Alvars and Nayanmars, marking the Bhakti 
    movement, and the patronage of literary classics by imperial Chola and Pandya empires. From the late 19th century, a literary revival occurred,
    characterized by works accessible to the masses. Influential figures like Subramania Bharathi spearheaded the modern Tamil literary movement, 
    leading to the proliferation of prose, short stories, and novels. Sangam literature, although some lost, provides insights into ancient Tamil 
    civilization, its governance, trade, and societal norms. Tolkappiyam, a foundational text, not only addresses grammar but also classifies 
    habitats, animals, and human behavior, reflecting the organized evolution of the Tamil language and society. The Sangam age, considered Tamils 
    golden era, witnessed a flourishing of literature under the Chera, Pandya, and Chola dynasties. Poets enjoyed considerable freedom in their relationship 
    with rulers, often critiquing them. The division of literature into \'subjective\' and \'objective\' topics facilitated nuanced discussions on 
    love, governance, and societal norms within prescribed conventions. The classification of land into genres like forests, mountains, and 
    seashores provided rich imagery for poetic expression. Religion played a significant role in Tamil literature, with Vaishnavism and Kaumaram 
    being prominent. Mayon (Vishnu) and Cēyōṉ (Murugan) were revered deities, with Sangam literature extolling their attributes. The Paripādal 
    anthology, focusing on love, glorified Perumal (Vishnu) as the supreme deity, while Murugan was celebrated as the youthful god. Shiva and Brahma were 
    seen as forms of Maha Vishnu, highlighting Vishnu\'s supremacy in Tamil religious beliefs.'''

    

    obj = question_and_answers(input_text)

    result = obj.getResponse().split('\n')

    for i in result:
        st.write(i)


        
