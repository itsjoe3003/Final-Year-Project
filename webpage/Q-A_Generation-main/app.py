import streamlit as st
import re
import json
import openai
import warnings
warnings.filterwarnings('ignore')
openai.api_key = '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' #'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'
def question_and_answers(input_text,no_correct):
    if isinstance(input_text, str):
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
        query = f'''Please stick to the following instructions while generating the response \
        - Generate only {no_ques} questions 
        - With {no_correct} correct answer for each and every question 
        - Please return the question and answers in the same format as specified in the template that is passed as reference for response generation. 
        - Please mandatorily add a question mark at the end of every question. 
        - Please compulsorily generate only specified number of options as answers, dont generate 4 options everytime as default'''
        input1 = input_text.split('\n')
        input1 = [para for para in input1 if para.strip()]
        merged_paras = " ".join(input1)
        input2 = 'Paragraph' + merged_paras
        if no_correct == 1:
            input3 = template_1 + query + input2
        else :
            input3 = template_2 + query + input2
        response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ],
              temperature=0.4,
              max_tokens=1000,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0
            )
        res1 = json.loads(str(response))
        res = res1.choices[0].message.content
        items = ''  .split('\n')
        
        st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                    .custom-text-02 { font-family: 'Perpetua', sans-serif; font-size: 30px;color:  #f9e79f   }
                    </style>
                    <p class="custom-text-02"> Displaying the generated Q&A </p>
                    """, unsafe_allow_html=True)
        for i in items:
            st.write(i)
    else:
        raise TypeError("Value must be a string data type.")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    col001, col002, col003 = st.columns([10,10,10])
    with col001:
        st.image('1.gif')
    with col002:
        st.image('1.gif')
    with col003:
        st.image('1.gif')
    col004, col005, col006 = st.columns([100,300,100])
    with col005:
        st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                    .custom-text-01 { font-family: 'Agdasima', sans-serif; font-size: 70px;color:cyan }
                    </style>
                    <p class="custom-text-01">Q&A Generation using LLM</p>
                    """, unsafe_allow_html=True)
    st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                    .custom-text-02 { font-family: 'Perpetua', sans-serif; font-size: 30px;color:  #f9e79f   }
                    </style>
                    <p class="custom-text-02"> About the project </p>
                    """, unsafe_allow_html=True)
    st.write('')
    st.markdown('<div style="text-align: justify"> Creating multiple-choice questions based on a given paragraph offers students a multifaceted approach to learning. It not only deepens comprehension by requiring them to distil key concepts and main ideas, but also engages them actively in the material, fostering a stronger grasp of the subject matter. This process encourages critical thinking as students formulate plausible distracters that challenge their own understanding and uncover potential misconceptions. Moreover, the skill of crafting questions cultivates the practical application of acquired knowledge, bridging the gap between theory and real-world scenarios.  </div>', unsafe_allow_html=True)
    st.write('')
    st.markdown('<div style="text-align: justify"> As students compare their questions to model answers, they engage in meaningful self-assessment, identifying areas of strength and those in need of review. This exercise mirrors the format of assessments, thus aiding in effective test preparation. Beyond assessment, the act of generating questions prompts students to organize information logically, strengthening their ability to structure thoughts coherently. Collaborative sharing of questions with peers and educators initiates a valuable feedback loop, refining their understanding and enhancing communication skills.  </div>', unsafe_allow_html=True)
    st.write('')
    st.markdown('<div style="text-align: justify"> This practice also nurtures vocabulary enrichment as students carefully select appropriate terminology. Ultimately, the process empowers students to take charge of their learning journey, cultivating autonomy and honing higher-order thinking skills. The lasting impact of question generation on long-term retention solidifies its role as a holistic tool for comprehensive understanding, effective study strategies, and academic growth.  </div>', unsafe_allow_html=True)
    st.write('')
    st.markdown("""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                    .custom-text-02 { font-family: 'Baskerville', sans-serif; font-size: 30px;color:  #f7dc6f}
                    </style>
                    <p class="custom-text-02"> Lets try generating some Q&A from the paragraph of your choice..... </p>
                    """, unsafe_allow_html=True)
    
    input_text = st.text_input('','Please enter your text here')
    if len(input_text) < 30:
        st.error('Please input a paragpraph with atleast 30 words in it for generating Q&A...', icon="🚨")
    else:
        st.write('')
        col007, col008 = st.columns([10,10])
        with col007:
            no_ques = int(st.radio(label = 'Please choose the number of questions to generate',options = [1,2,3,4]))
        with col008:
            no_correct = int(st.radio('Please choose the number of correct/nearly_correct answers to generate', options = [1,2]))
        st.write('')
        if st.button('Generate the Q&A for the above paragraph', use_container_width=True):
            input_paragraph = input_text
            question_and_answers(input_text,no_correct)


    
            
            
    st.divider()
    col1001, col1002, col1003,col1004, col1005 = st.columns([10,10,10,10,15])
    with col1005:
        st.markdown("""
                                <style>
                                @import url('https://fonts.googleapis.com/css2?family=Agdasima');
                                .custom-text-10 { font-family: 'Agdasima', sans-serif; font-size: 28px;color:cyan }
                                </style>
                                <p class="custom-text-10">An Effort by : SVSR (Team Mates)</p>
                                """, unsafe_allow_html=True)    
        