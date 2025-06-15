from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import pymysql
import re
import json
from sql_pwd import PASS
import cv2
import sys
import threading
from deep_translator import GoogleTranslator


sys.path.insert(0, '/FYP')


# from controller_main import MainClass

session = dict()



app = Flask(__name__)
CORS(app)


app.secret_key = "Secret Key"


mysql_config = {
    'user': 'root',
    'password': PASS,
    'host': 'localhost',
    'database': 'fyp'
}



mysql = pymysql.connect(**mysql_config)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'success':  True, 'msg': 'Connected to the server.'}), 200





@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # msg = ''
    # print('Request == POST: ', request.method)

    if not username or not password:
        return jsonify({'msg': 'Please provide both username and password', 'success': False}), 400

    try:
        with mysql.cursor() as cursor:
            cursor.execute('SELECT * FROM student WHERE username = %s AND password = %s', (username, password))
            account = cursor.fetchone()
            print('Account: ', account)
            if account:
                session['loggedin'] = True
                session['student_id'] = account[0]
                session['student_name'] = account[1]
                session['username'] = account[2]
                print(session)
                
                # cursor.execute('select * from leaderboard where')

                # print('Type of loggedin: ', type(session['loggedin']))
                return jsonify({'msg': '', 'success': True, 'name': account[2]}), 200
            else:
                return jsonify({'msg': 'Incorrect username or password'}), 401
    except pymysql.Error as e:
        return jsonify({'msg': f'Database error: {e}'}), 500




@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('student_id', None)
    session.pop('username', None)
    return jsonify({'success': True})





@app.route('/register', methods=['GET', 'POST'])
def register():
    data = request.json
    student_name = data.get('student_name')
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'msg': 'Please fill out the form', 'success': False}), 400

    try:
        with mysql.cursor() as cursor:
            cursor.execute('SELECT * FROM student WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            else:
                cursor.execute('INSERT INTO student (student_name, username, password) VALUES (%s, %s, %s)', (student_name, username, password))
                mysql.commit()
                msg = 'You have successfully registered!'
                return jsonify({'msg': msg, 'success':True}), 200
    except pymysql.Error as e:
        msg = f'Database error: {e}'
    return jsonify({'msg': msg, 'success': False}), 400
    

    


@app.route('/frontpage', methods=['GET', 'POST'])
def frontpage():
    if request.method == 'POST' or request.method == 'GET':
        # print(request)
        if session.get('loggedin'):
            print('Session stuff: ', session)
            student_id = session['student_id']
            try:
                with mysql.cursor() as cursor:
                    cursor.execute("SELECT s.student_name, l.exp_points, l.marks FROM leaderboard l JOIN student s ON l.student_id = s.student_id ORDER BY l.marks DESC")
                    leaderboard_data = cursor.fetchall()
                    leaderboard_data = [{"student_name": row[0], "exp_points": row[1], "marks":row[2]} for row in leaderboard_data]

                    cursor.execute("SELECT exp_points, progress_percentage FROM leaderboard WHERE student_id = %s", (student_id,))
                    exp_progress_percent = cursor.fetchone()

                    print("\n Exp prog percent: ", exp_progress_percent)

                    print("\n LEADERBOARD: ", leaderboard_data)

                data = {
                    "leaderboard": leaderboard_data,
                    "exp_points": exp_progress_percent[0] if exp_progress_percent else None,
                    "progress_percentage": exp_progress_percent[1] if exp_progress_percent else None
                }
                    
                return jsonify({'leaderboard': data, 'success':True}), 200
            except pymysql.Error as e:
                print('\n Database error in frontpage')
                return jsonify({"error": f'Database error: {e}'})
        else:
            print("you are not logged in")
            print('Session stuff: ', session)
    else:
        return jsonify({'msg': 'Error', 'success':False}), 400







@app.route('/dashboard', methods=[ 'GET','POST'])
def dashboard():

    print("In dashboard, session[loggedin] value is: ", session.get('loggedin'))

    if session.get('loggedin'):
        student_id = session['student_id']
        username = session['username']

        try:
            with mysql.cursor() as cursor:

                cursor.execute('SELECT exp_points FROM leaderboard WHERE student_id=%s', (student_id))
                exp_points = cursor.fetchone()

                if not exp_points:
                    initial_exp_points = 0
                    initial_marks = 0
                    cursor.execute("INSERT INTO leaderboard (student_id, exp_points, progress_percentage, marks) VALUES (%s, %s, %s, %s)", (student_id, initial_exp_points, 0, initial_marks))
                    mysql.commit()
                
                cursor.execute('SELECT exp_points, progress_percentage FROM leaderboard WHERE student_id=%s', (student_id,))
                exp_points = cursor.fetchone()

                print('\n Dashboard-> Exp_points stuff: ', exp_points)

                print('\n Percentage progress (dash): ', round(exp_points[1]))

                return jsonify({"success":True, "username": username, "exp_points": exp_points[0], "progress": exp_points[1]})

        except pymysql.Error as e:
            return jsonify({"error": "Database error connection"})

    else:
        return jsonify({'msg':'Not Logged In'}), 500


    


    

@app.route('/dashboard-data')
def dashboard_data():
    try:
        with mysql.cursor() as cursor:
            cursor.execute("""
                SELECT s.student_name, l.exp_points, l.marks
                FROM leaderboard l
                JOIN student s ON l.student_id = s.student_id
                ORDER BY l.exp_points DESC
            """)
            leaderboard_data = cursor.fetchall()
            leaderboard_data = [{"student_name": row[0], "exp_points": row[1], "marks":row[2]} for row in leaderboard_data]

        student_id = session.get('student_id')
        with mysql.cursor() as cursor:
            cursor.execute("SELECT exp_points, progress_percentage FROM leaderboard WHERE student_id = %s", (student_id,))
            exp_progress_percent = cursor.fetchone()

        data = {
            "leaderboard": leaderboard_data,
            "exp_points": exp_progress_percent[0] if exp_progress_percent else None,
            "progress_percentage": exp_progress_percent[1] if exp_progress_percent else None
        }

        return jsonify(data)
    except pymysql.Error as e:
        return jsonify({"error": f"Database error: {e}"})







@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    data = request.json
    user_input = data.get("text")
    print(user_input)
    if session['loggedin'] == True:
        try:
            to_translate = user_input
            translated = GoogleTranslator(source='auto', target='tamil').translate(to_translate)

            return jsonify(translated)
            
        except:
                print("error")







courses = {
        'LANGUAGE AND LITERATURE': {
            'name': 'LANGUAGE AND LITERATURE',
            'video': 'https://www.youtube.com/embed/kmq_eZon0L8?si=5XI8yfWX5bS6iOoQ',
            'description': ['''1.Language Families in India - Dravidian Languages:
            Tamil belongs to the Dravidian language family, spoken primarily in South India.
            It is distinct from the Indo-European family that includes Hindi and Sanskrit.
            This unique lineage contributes to the richness and diversity of Indian languages.
            Language Families in India - Dravidian Languages:Tamil belongs to the Dravidian language family, spoken primarily in South India.
It is distinct from the Indo-European family that includes Hindi and Sanskrit.
This unique lineage contributes to the richness and diversity of Indian languages.''',
                            
'''2. Tamil as a Classical Language:

Tamil is one of the six classical languages of India, recognized for its ancient origins and rich literary heritage.
Its documented history stretches back over 2,000 years, with a vast collection of classical literature.''',

'''3. Classical Literature in Tamil - Sangam Literature:

Sangam literature refers to works from the Sangam period (3rd century BCE to 3rd century CE).
It encompasses poetry, epics, and didactic works, offering valuable insights into Tamil society, culture, and traditions.
Notably, Sangam literature is considered secular, reflecting diverse viewpoints and a focus on earthly life.''',

'''4. Secular Nature of Sangam Literature:

Unlike some other classical Indian literature heavily influenced by religion, Sangam literature portrays a more secular society.
It celebrates love, nature, war, and social life, highlighting the accomplishments and complexities of human experience.''',

'''5. Distributive Justice in Sangam Literature:

The concept of "aṟam" (righteous conduct) is prominent in Sangam literature.
It emphasizes fair distribution of wealth, just rule, and social responsibility, reflecting a concern for social justice.''',

'''6. Management Principles in Thirukural:

Thirukural is an ancient Tamil text revered for its wisdom on various aspects of life.
It includes sections on ethics, politics, economics, and love, offering valuable management principles still relevant today.''',

'''7. Tamil Epics and Impact of Buddhism & Jainism:

Tamil epics like Silappadhikaram and Manimekalai showcase the influence of Buddhism and Jainism on Tamil culture.
These religions enriched Tamil literature with philosophical themes and ethical values.''',

'''8. Bhakti Literature - Azhwars and Nayanmars:

The Bhakti movement in Tamil Nadu (6th-9th centuries CE) gave rise to devotional poetry by Alwars (Vaishnavism) and Nayanmars (Saivism).
Their works express intense love and devotion for their deities, influencing Tamil literature and religious practices.''',

'''9. Forms of Minor Poetry:

Tamil literature boasts a rich tradition of minor poetry forms like "ahappattu" (love poems) and " purappattu" (war poems).
These diverse forms offer a nuanced view of emotions, social interactions, and historical events.''',

'''10. Development of Modern Literature in Tamil:

Modern Tamil literature emerged in the 19th century, influenced by Western literary trends and social reform movements.
Writers like Subramanya Bharathiyar and Bharathidasan addressed issues like social justice, nationalism, and women's rights.''',

'''11. Contribution of Bharathiyar and Bharathidhasan:

Subramanya Bharathiyar, a revolutionary poet, infused Tamil literature with patriotism, social awareness, and a call for freedom.
Bharathidasan championed social reforms, women's empowerment, and the eradication of caste discrimination through his powerful writings.'''],
        
        
        'topic_id': 1,
        
        },
        'HERITAGE - ROCK ART PAINTINGS TO MODERN ART - SCULPTURE': {
            'name': 'HERITAGE - ROCK ART PAINTINGS TO MODERN ART - SCULPTURE',
            'video': 'https://www.youtube.com/embed/7GvS0lSOMYk?si=Kh0OQBbtpu-oZ0TR',
            'description': ['''1. Hero Stones to Modern Sculpture:

Hero Stones (Virkkagal): These ancient megaliths, dating back centuries, commemorate fallen warriors or individuals. They depict scenes of battle, hunting, or daily life, offering a glimpse into Tamil social structures and artistic styles.
Modern Sculpture: Tamil artists continue the tradition of storytelling through sculpture. Modern works range from abstract and contemporary pieces to figurative representations, reflecting the evolution of Tamil artistic expression.''',

'''2. Bronze Icons:

A Legacy in Metal: Tamil Nadu boasts a rich tradition of bronze iconography. Exquisitely crafted deities, saints, and mythical creatures showcase the mastery of Tamil metalworkers. These icons are not just artistic marvels but serve as devotional objects in temples.''',

'''3. Tribes and their Handicrafts:

A Tapestry of Skill: Tamil Nadu's diverse tribal communities possess unique handicraft traditions. From intricate beadwork and woven textiles to woodcarving and pottery, these crafts reflect the cultural identity and artistic ingenuity of each tribe.''',

'''4. The Art of Temple Car Making (Ther):

Colossal Devises of Faith: Temple cars (Ther) are monumental chariots used in temple festivals. These elaborately decorated wooden structures showcase carpentry skills, metalwork, and painting. They are not simply vehicles but mobile representations of deities, signifying the vibrant link between art and religious practice in Tamil culture.''',

'''5. Massive Terracotta Sculptures:

Earthen Grandeur: Tamil Nadu has a history of crafting colossal terracotta sculptures, particularly during the Chola dynasty. These impressive figures, often depicting deities or mythological characters, demonstrate the scale and skill of Tamil artists in working with clay.''',

'''6. Village Deities:

Protectors of the Community: Shrines dedicated to village deities are a common sight in Tamil Nadu. These deities, often represented by simple stone sculptures or painted murals, represent the local beliefs and traditions, reflecting the deep connection between art and community life.''',

'''7. Thiruvalluvar Statue at Kanyakumari:

A Monument to Wisdom: The towering statue of Thiruvalluvar, a revered Tamil poet and author of the ethical treatise 'Thirukural,' stands at the southernmost tip of India. This iconic landmark embodies the importance of Tamil literature and its enduring influence.''',

'''8. Making of Musical Instruments - Mridangam, Parai, Veenai, Yazh and Nadhaswaram:

A Symphony of Craftsmanship: The creation of traditional Tamil musical instruments involves meticulous craftsmanship. Instruments like the Mridangam (drum), Parai (frame drum), Veenai (string instrument), Yazh (harp), and Nadhaswaram (shehnai) are not just instruments but works of art in themselves. Their construction showcases the intricate knowledge of wood, metal, and skin, passed down through generations.''',

'''9. Role of Temples in Social and Economic Life of Tamils:

Centers of Art, Culture, and Community: Temples have played a central role in Tamil society for centuries. They are not just places of worship, but also hubs of art, culture, and social interaction. Temple architecture, sculpture, paintings, and music festivals all contribute to the rich artistic heritage of Tamils. Temples also served as economic centers, employing artisans, musicians, and dancers, and supporting local communities.'''],
       
       'topic_id': 2,
       
        },


        'FOLK AND MARTIAL ARTS': {
            'name': 'FOLK AND MARTIAL ARTS',
            'video': 'https://www.youtube.com/embed/gA1dmzWd2mE?si=YX9245VfFQfwq2qV',
            'description': ['''Therukoothu:

Street Theater: Therukoothu is a vibrant form of street theater with a long history in Tamil Nadu. It combines music, dance, drama, and storytelling to entertain and educate audiences. Performers enact stories from mythology, folklore, and contemporary life, using colorful costumes, masks, and props. Therukoothu plays an important role in preserving and transmitting Tamil culture and traditions.''',

'''Karagattam:

Pot Dance: Karagattam is a graceful folk dance performed primarily by women in Tamil Nadu. It involves balancing a decorated pot (karagam) on the head while dancing to rhythmic beats. The dance is often performed during festivals and celebrations, and showcases the skill, poise, and artistry of the dancers.''',

'''Villu Pattu:

Bow Song: Villu Pattu is a traditional form of storytelling and music from Tamil Nadu. It involves singing ballads accompanied by a bow-shaped instrument called the villu. The stories often focus on historical events, mythological characters, and social issues. Villu Pattu is a popular form of entertainment and education in rural areas, and helps preserve Tamil folklore and oral traditions.''',

'''Kaniyan Koothu:

Puppet Theater: Kaniyan Koothu is a traditional form of puppet theater in Tamil Nadu. It uses shadow puppets made of leather to enact stories from mythology, folklore, and contemporary life. The puppets are manipulated by skilled puppeteers behind a screen, and the performance is accompanied by music and narration. Kaniyan Koothu is a popular form of entertainment for all ages, and helps promote moral values and social messages.''',

'''Oyillattam:

Beauty Dance: Oyillattam is a graceful folk dance performed by men in Tamil Nadu. It involves rhythmic movements and steps performed to the accompaniment of music. The dance is often performed during festivals and celebrations, and showcases the strength, agility, and artistry of the dancers.''',

'''Leather Puppetry:

Shadow Play: Leather puppetry is a traditional form of puppet theater in Tamil Nadu. It uses puppets made of leather to enact stories from mythology, folklore, and contemporary life. The puppets are manipulated by skilled puppeteers behind a screen, and the performance is accompanied by music and narration. Leather puppetry is a popular form of entertainment for all ages, and helps promote moral values and social messages.''',

'''Silambattam:

Stick Martial Art: Silambattam is a traditional martial art from Tamil Nadu that uses a pair of sticks (silambam) for combat and display. It involves intricate footwork, hand movements, and strikes, and requires skill, discipline, and physical fitness. Silambattam is not just a martial art but also a performing art, with demonstrations and competitions held during festivals and events.''',

'''Valari:

Sword Dance: Valari is a traditional sword dance performed by men in Tamil Nadu. It involves intricate movements and steps performed with a sword, often to the accompaniment of music. The dance is often performed during festivals and celebrations, and showcases the strength, agility, and artistry of the dancers.''',

'''Tiger Dance:

A Fierce Performance: Tiger dance is a traditional folk dance performed in Tamil Nadu, particularly during festivals. It involves dancers wearing tiger costumes and enacting the movements and roars of the animal. The dance is accompanied by music and drumming, and creates a lively and exciting atmosphere.'''],
        
        
        'topic_id': 3,
        
        },


        'THINAI CONCEPT OF TAMILS': {
            'name': 'THINAI CONCEPT OF TAMILS',
            'video': 'https://www.youtube.com/embed/PknBNA8K-mo?si=mPEpHhquIV-9f5Up',
            'description': ['''1. Flora and Fauna of Tamils:

Sangam literature provides a wealth of information about the flora and fauna of ancient Tamil Nadu. Poets frequently reference plants and animals, offering insights into the natural environment and its significance in Tamil life. From majestic elephants and fierce tigers to fragrant sandalwood trees and vibrant flowering plants, the literature paints a picture of a diverse and thriving ecosystem.''',

'''2. Aham and Puram Concept from Tholkappiyam and Sangam Literature:

Tholkappiyam, the ancient Tamil grammar, establishes two core themes in poetry - Aham (inner life) and Puram (outer world). Aham poetry explores themes of love, separation, and domestic life, while Puram poetry focuses on war, heroism, kingship, and social order. These contrasting themes provide a well-rounded view of Tamil society and values. Sangam literature is rich with poems reflecting both Aham and Puram traditions.''',

'''3. Aram Concept of Tamils:

Aram translates to "righteous conduct" and is a central concept in Tamil ethics. It encompasses principles of justice, fairness, compassion, and fulfilling one's duties. Sangam literature emphasizes the importance of aram, depicting it as the foundation of a prosperous and harmonious society.''',

'''4. Education and Literacy during Sangam Age:

Despite the lack of formal educational institutions, evidence suggests a high level of literacy during the Sangam period. Education was often informal, passed down through families and communities. Bards, scholars, and poets played a crucial role in transmitting knowledge and skills. The emphasis on literature and poetry suggests a society that valued intellectual pursuits and communication.''',

'''5. Ancient Cities and Ports of Sangam Age:

Sangam literature mentions several prominent cities and ports that served as centers of trade, culture, and political power. Some notable examples include Madurai, Kanchipuram, Kaveripattinam (Puhar), and Korkai. These cities facilitated trade with other parts of India and beyond, playing a significant role in the development of Tamil civilization.''',

'''6. Export and Import during Sangam Age:

The Sangam period witnessed thriving trade networks connecting Tamil Nadu with other regions. Exports included textiles, spices like pepper and cardamom, pearls, and ivory products. Imports consisted of horses, cattle, metals, and luxury goods like wine and silk. This maritime trade contributed significantly to the economic prosperity and cultural exchange of the Tamils.''',

'''7. Overseas Conquest of Cholas:

While the Cholas are primarily known for their later imperial period, the dynasty's roots go back to the Sangam Age. Evidence suggests early Cholas engaged in some overseas conquests, particularly in Southeast Asia. These conquests may have established cultural and trade links between South India and Southeast Asia, laying the groundwork for the Cholas' later maritime dominance.'''],

       
       'topic_id': 4,
       
        },


        'CONTRIBUTION OF TAMILS TO INDIAN NATIONAL MOVEMENT AND INDIAN CULTURE': {
            'name': 'CONTRIBUTION OF TAMILS TO INDIAN NATIONAL MOVEMENT AND INDIAN CULTURE',
            'video': 'https://www.youtube.com/embed/NDmpMa_zASY?si=AuLYcB05XxRC3gxM',
            'description': ['''1. Contribution of Tamils to Indian Freedom Struggle:

Tamils played a significant role in India's fight for independence. Leaders like V. O. Chidambaram Pillai, Subramanya Bharathiyar, and VOC Priya advocated for self-rule and inspired generations with their activism and revolutionary writings. Tamils actively participated in non-violent protests, civil disobedience movements, and boycotts throughout the struggle.''',

'''2. The Cultural Influence of Tamils over the Other Parts of India:

Tamil culture has left a lasting influence on other parts of India. Trade, literature, and religious exchange have played a vital role in this. Tamil literary works like the Ramayana and Mahabharata translations influenced regional languages and storytelling traditions. Temple architecture styles, music, and dance forms from Tamil Nadu have also found resonance across India.''',

'''3. Self-Respect Movement:

The Self-Respect Movement, led by Periyar E. V. Ramasamy, emerged in the early 20th century. It challenged the caste system, advocated for social justice and women's rights, and promoted self-respect for all individuals, regardless of caste. This movement had a lasting impact on Tamil society and continues to influence social reforms in India.''',

'''4. Role of Siddha Medicine in Indigenous Systems of Medicine:

Siddha medicine is one of the traditional Indian medical systems originating in Tamil Nadu. It emphasizes preventive care, uses herbal remedies, and focuses on maintaining balance between the five elements in the body. While facing challenges in the modern world, Siddha medicine still plays a crucial role in healthcare, particularly in rural areas, offering a unique approach to health and well-being.''',

'''5. Inscriptions & Manuscripts:

Tamil Nadu boasts a rich history of inscriptions on temple walls, caves, and copper plates. These inscriptions, dating back centuries, provide valuable information about Tamil language evolution, social structures, political systems, and religious practices. Additionally, palm-leaf manuscripts preserved in libraries and private collections offer insights into Tamil literature, philosophy, and history.''',

'''6. Print History of Tamil Books:

Tamil holds the distinction of being one of the oldest continuously living languages with a rich printing history. The first Tamil book printed with movable type appeared in the 16th century. Printing presses established by missionaries and local patrons facilitated the dissemination of knowledge and literature, contributing to the growth of Tamil scholarship and cultural exchange.'''],
        
        'topic_id': 5,
        
        },


        'WEAVING AND CERAMIC TECHNOLOGY': {
            'name': 'WEAVING AND CERAMIC TECHNOLOGY',
            'video': 'https://www.youtube.com/embed/S_Y-gLn_1ck?si=yQg_pXAkDU1vm3ML',
            'description': ['''Weaving Industry during Sangam Age:

The Sangam period witnessed a flourishing weaving industry in Tamil Nadu. References in Sangam literature depict skilled weavers crafting exquisite fabrics using cotton, silk, and wool. These textiles were renowned for their quality, intricate designs, and vibrant colors. The industry played a significant role in the Tamil economy, providing employment and contributing to trade with other regions.''',

'''Ceramic technology:

Tamils of the Sangam Age possessed advanced skills in ceramic technology. Archaeological excavations reveal a wide variety of pottery types, including utilitarian vessels for everyday use and decorative pieces. The use of various firing techniques and surface treatments indicates a deep understanding of clay properties and manipulation.''',

'''Black and Red Ware Potteries (BRW):

Black and Red Ware (BRW) is a distinctive type of pottery widely found in archaeological sites across Tamil Nadu and other parts of India. Characterized by a black interior and a red or black exterior, BRW pottery served various domestic purposes. Its presence helps archaeologists understand settlement patterns and technological advancements during the Sangam era.''',

'''Graffiti on Potteries:

An intriguing aspect of Tamil ceramics is the presence of graffiti on some pottery pieces. These markings, often simple symbols or geometric patterns, could represent ownership marks, religious symbols, or even messages. Studying these markings offers archaeologists valuable insights into communication practices and social customs of the period.''',

'''The Synergy of Art and Utility:

The Sangam Age pottery tradition highlights the skillful blending of art and utility. While pottery served practical purposes, the use of various techniques and decorative elements demonstrates an artistic sensibility. This synergy reflects the cultural values and aesthetics of the Tamils during this vibrant period.'''],
       
       'topic_id': 6,
       
        },


        'DESIGN AND CONSTRUCTION TECHNOLOGY': {
            'name': 'DESIGN AND CONSTRUCTION TECHNOLOGY',
            'video': 'https://www.youtube.com/embed/dHkg5FNE_8g?si=API9qvxpWRYJppbQ',
            'description': ['''1. Designing and Structural Construction - Houses and Household Materials (Sangam Age):

Sangam literature offers glimpses into house designs and materials of the era. Dwellings likely varied depending on social status. Wealthier individuals might have resided in brick or mudbrick houses with thatched roofs and wooden pillars. Commoners might have lived in simpler structures using materials like bamboo, palm leaves, and mud.''',

'''2. Building Materials and Hero Stones (Sangam Age):

Sangam literature and archaeological evidence reveal the use of various building materials. Bricks, mudbricks, wood, and terracotta were common. Hero stones, megalithic monuments commemorating heroes or significant events, were often made of granite or laterite. These stones provide valuable insights into burial practices and artistic styles of the Sangam period.''',

'''3. Stage Constructions in Silappathikaram:

The epic poem Silappathikaram describes elaborate stage constructions used for performances. These stages could be temporary or permanent, and incorporated features like raised platforms, decorated backdrops, and intricate props. The descriptions offer valuable information about performance traditions and theatrical practices of the time.''',

'''4. Sculptures and Temples of Mamallapuram:

Mamallapuram (Mahabalipuram) boasts a collection of rock-cut sculptures and temples from the Pallava dynasty. These structures showcase the artistry and technical prowess of Pallava sculptors. The Shore Temple, Pancha Rathas (Five Chariots), and Descent of the Ganges are some of the most renowned examples, depicting religious themes and mythological narratives.''',

'''5. Great Temples of Cholas and Other Worship Places:

The Chola dynasty is renowned for its grand temples, characterized by towering gopurams (gateway towers), intricate sculptures, and vast courtyards. Brihadisvara Temple (Thanjavur), Gangaikondacholapuram Temple, and Airavatheeswarar Temple (Kanchipuram) are some of the architectural marvels showcasing Chola artistry. These temples were not just places of worship, but also centers of learning, administration, and social interaction.''',

'''6. Temples of Nayaka Period:

The Nayaka dynasty's temples are known for their distinctive style, featuring elongated vimana towers (shrine sanctum) and elaborately carved halls. Meenakshi Temple (Madurai), with its colorful gopurams and sculpted pillars, is a prime example. These temples represent the artistic evolution of Tamil architecture, incorporating influences from other parts of India.''',

'''7. Type Study: Madurai Meenakshi Temple:

A detailed study of the Madurai Meenakshi Temple reveals the architectural principles and symbolic significance of Nayaka temple design. The temple complex includes multiple halls, shrines, and corridors, each intricately decorated with sculptures and paintings. The towering gopurams serve as gateways and landmarks, while the Hall of Thousand Pillars showcases the exquisite craftsmanship of the Nayaka era.''',

'''8. Thirumalai Nayakar Mahal:

This grand palace in Madurai, built by the Nayaka king Thirumalai Nayakar, exemplifies the architectural grandeur of the dynasty. The palace complex incorporates Indo-Islamic influences, featuring arched doorways, courtyards, and ornamental gardens. It serves as a testament to the artistic exchange and fusion of styles during the Nayaka period.''',

'''9. Chettinad Houses:

Chettinad, a region in Tamil Nadu, is famous for its unique architectural style evident in its houses. These large mansions, constructed using brick and mortar, are known for their intricately carved doorways, spacious rooms, and distinctive tiled floors. Chettinad houses reflect the prosperity and architectural heritage of the Chettiar community.''',

'''10. Indo-Saracenic Architecture at Madras During British Period:

Madras (Chennai) during the British Raj witnessed a blend of European and Indian architectural styles known as Indo-Saracenic. Public buildings like the Madras High Court and the Egmore Museum reflect this style, incorporating elements like domes, minarets, and Mughal arches. This architecture represents the cultural exchange and adaptation that occurred during the colonial period.'''],
        
        'topic_id': 7,
        
        },


        'MANUFACTURING TECHNOLOGY': 
        {
            'name': 'MANUFACTURING TECHNOLOGY',
            'video': 'https://www.youtube.com/embed/KTl3Rj-gTA0?si=cTfSTSJfWDP0aeeY',
            'description': ['''1. Art of Ship Building:

Sangam literature and archaeological evidence point to a well-developed shipbuilding industry in ancient Tamil Nadu. Skilled craftsmen built sturdy ships capable of navigating vast distances, facilitating trade and exploration. These ships played a crucial role in establishing the Tamils as a prominent maritime power.''',

'''2. Metallurgical Studies:

The Tamils possessed advanced knowledge of metallurgy, evident in their ability to extract and refine metals like iron, copper, and gold. This knowledge facilitated the development of tools, weapons, ornaments, and coinage, impacting various aspects of Tamil life.''',

'''3. Iron Industry - Iron Smelting, Steel:

The mastery of iron smelting allowed the Tamils to produce tools and weapons crucial for agriculture, construction, and warfare. Their ability to develop steel further enhanced the strength and versatility of these objects.''',

'''4. Copper and Gold Coins as a Source of History:

The use of copper and gold coins during the Sangam period provides valuable insights into the Tamil economy and trade practices. These coins, often depicting rulers or symbols, serve as historical artifacts and shed light on the economic and political structures of the time.''',

'''5. Minting of Coins:

The minting of coins facilitated trade by offering a standardized medium of exchange. The process of minting itself reveals the technological advancements and artistic skills of the Tamils. The designs and inscriptions on coins can provide valuable information about the issuing authority and prevailing artistic styles.''',

'''6. Bead Making Industries:

Bead making was a flourishing industry in ancient Tamil Nadu.  Craftspeople created beautiful and intricate beads using various materials like:,

Stone beads: Carved from precious and semi-precious stones, these beads symbolized wealth and status.
Glass beads: The use of glassmaking techniques allowed for vibrant colored beads, adding a decorative element to clothing and jewelry.
Terracotta beads: Made from baked clay, these beads were readily available and affordable, reflecting a wider range of artistic styles.
Shell beads/bone beads: Natural materials like shells and bones were also used to create beads, showcasing resourcefulness and artistic expression.''',

'''7. Archaeological Evidences:

Archaeological excavations have unearthed numerous artifacts related to these crafts, including tools, molds, and finished products. These discoveries provide tangible evidence of the skill and ingenuity of Tamil artisans.''',

'''8. Gemstone Types Described in Silappadhikaram:

The epic poem Silappathikaram details various types of gemstones and their properties. This information suggests a deep appreciation for precious stones and their use in jewelry, trade, and even medicinal practices. The descriptions offer valuable insights into the Tamil understanding of the natural world and its resources.'''],
        
        'topic_id': 8,
        
        },


        'AGRICULTURE AND IRRIGATION TECHNOLOGY': {
            'name': 'AGRICULTURE AND IRRIGATION TECHNOLOGY',
            'video': 'https://www.youtube.com/embed/UpADXLBPT8U?si=x6APmpHC_3NerMo4',
            'description': ['''1. Dams, Tanks, Ponds, and Sluices:

Tamils have a long history of water management techniques. They constructed dams across rivers to store rainwater, creating artificial lakes or tanks. Smaller ponds were built to collect local runoff. Sluices were ingenious mechanisms used to regulate water flow for irrigation purposes. These advancements ensured a consistent water supply for agriculture, a vital aspect of Tamil society.''',

'''2. Significance of Kumizhi Thoompu (Granaries) of the Chola Period:

The Cholas excelled in resource management. Kumizhi Thoompu refers to a network of granaries built throughout their empire. These structures stored surplus grain during harvest seasons, ensuring food security during droughts or times of scarcity. The foresight and planning behind these granaries demonstrate the Cholas' commitment to the well-being of their people.''',

'''3. Animal Husbandry and Cattle Wells:

Animal husbandry played a significant role in the Tamil economy. Tamils raised livestock for milk, meat, and agricultural labor. Wells specifically designed for cattle ensured a reliable source of water for these valuable animals. This emphasis on animal care highlights the Tamils' understanding of the importance of a healthy livestock population.''',

'''4. Agriculture and Agro-Processing:

Agriculture was the backbone of the Tamil economy. Tamils cultivated a variety of crops, including rice, millet, sugarcane, and cotton. Agro-processing techniques like milling and weaving further enhanced the value of agricultural products. The development of these practices demonstrates the Tamils' resourcefulness and adaptability to their environment.''',

'''5. Knowledge of the Sea:

From ancient times, Tamils displayed a deep understanding of the sea. Their expertise in navigation and shipbuilding allowed them to establish a flourishing maritime trade network. This knowledge of the ocean currents, winds, and constellations played a crucial role in their maritime success.''',

'''6. Fisheries and Pearl Diving:

The seas surrounding Tamil Nadu provided a rich source of food and resources. Fisheries were a significant industry, with Tamils employing various techniques for catching fish. Pearl diving, a dangerous but lucrative occupation, yielded precious pearls used in jewelry and ornamentation. These maritime activities showcased the Tamils' courage, resourcefulness, and understanding of the marine environment.''',

'''7. Ancient Knowledge of the Ocean:

Tamil texts reveal a sophisticated understanding of the ocean and its forces. They mention different types of waves, marine life, and even the concept of tides. This knowledge likely stemmed from centuries of observation and practical experience at sea, demonstrating the Tamils' keen awareness of the natural world.''',

'''8. Knowledge Specific Society:

Tamil society was organized around specialized skills and professions. From farmers and artisans to merchants and sailors, each group possessed unique knowledge and skills passed down through generations. This knowledge-specific society contributed to the overall prosperity and technological advancements of the Tamils.'''],
        
        'topic_id': 9,
        
        },


        
        'SCIENTIFIC TAMIL & TAMIL COMPUTING': {
            'name': 'SCIENTIFIC TAMIL & TAMIL COMPUTING',
            'video': 'https://www.youtube.com/embed/HXDE5RxkPkw?si=rOW5lVgyFJrZ9-Ql',
            'description': ['''1. Development of Scientific Tamil:

Scientific Tamil aims to create a rich vocabulary for expressing scientific concepts in Tamil. This involves translating existing scientific terminology, developing new terms for emerging fields, and ensuring accurate and clear communication of scientific ideas.''',

'''2. Tamil Computing:

Tamil computing focuses on the use of computers and technology for processing, storing, and disseminating information in Tamil. This includes developing Tamil fonts, spell checkers, optical character recognition (OCR) software for converting scanned text to digital format, and natural language processing (NLP) tools for analyzing and understanding Tamil text.''',

'''3. Digitalization of Tamil Books:

Preserving and making accessible Tamil literary heritage is crucial. Digitalization of Tamil books involves converting physical books into digital formats like PDFs or e-books. This allows wider access to rare and valuable texts, facilitating research, education, and cultural preservation.''',

'''4. Development of Tamil Software:

With the increasing use of computers and smartphones, creating user-friendly software in Tamil is essential. This includes developing operating systems, productivity applications, educational software, and entertainment software in Tamil, promoting its usage in all aspects of digital life.''',

'''5. Tamil Virtual Academy (TVA):

The Tamil Virtual Academy is a government initiative dedicated to promoting Tamil language and culture globally. It offers online courses, resources, and digital libraries in Tamil, fostering learning and appreciation for the language.''',

'''6. Tamil Digital Library:

The Tamil Digital Library is a repository of digital resources related to Tamil language, literature, and culture. It provides a centralized platform for accessing digitized books, manuscripts, journals, and other materials, promoting research and scholarly engagement.''',

'''7. Online Tamil Dictionaries:

Online Tamil dictionaries provide convenient access to word definitions, translations, and usage examples. These resources help users understand the nuances of the Tamil language and promote accurate communication.''',

'''8. Sorkuvai Project:

The Sorkuvai Project focuses on documenting and preserving the endangered tribal languages of Tamil Nadu. It involves recording spoken languages, creating dictionaries and grammars, and promoting awareness to revitalize these valuable linguistic traditions.'''],
        
        'topic_id': 10,
        
        }
    }




@app.route('/topic/<course_name>', methods=['GET', 'POST'])
def get_topic(course_name):

    if request.method == "POST" or request.method == 'GET':

        print('Course name i got: ', course_name)
        # print('Type of course_name is: ', type(course_name))
        course_data = courses.get(course_name)
        # print(course_data)
        if course_data:
            return jsonify(course_data)
        else:
            return jsonify({'error': 'Course not found'}), 404
    else:
        return jsonify({"some error": "encountered an error"}), 405




@app.route('/assignment/MCQ/<course_name>')
def assignment_mcq(course_name):
    print('MCQ assignment loaded')


@app.route('/topicname', methods=['GET', 'POST'])
def topic_name():
    data = request.json
    if request.method=='POST' or request.method=='GET':
        
        topic_name = data.get('topic_name')
        if session.get('loggedin') == True:
            # try:
            #     with mysql.cursor() as cursor:
            #         cursor.execute('select topic_id from topics where ')
            print(f'\nTopic Name is {topic_name}\n')

            return jsonify({'topic_name': topic_name})
        else:
            return jsonify({'topic_name': 'Not logged in it seems'})



# @app.route('/dashboard-data')
# def getDashData():
#     if session.get('loggedin'):

#         student_id = session['student_id']

#         try:
#             with mysql.cursor as cursor:
#                 cursor.execute("SELECT exp_points, progress_percentage from leaderboard where student_id=%s", (student_id))
#                 dashdata = cursor.fetchone()


        
#         except pymysql.Error as e:
#             print("error in dash data")


    




@app.route('/check-assignment', methods=['GET', 'POST'])
def check_assignment():
    data = request.get_json()
    # student_id = data.get('student_id')
    student_id = session['student_id']
    # assignment_number = data.get('assignment_number')
    topic_name = data.get('courseName')
    assignment_name = data.get('assgn_type')

    try:
        with mysql.cursor() as cursor:
            cursor.execute('select topic_id from topics where topic_name like %s',(topic_name))
            topic_id = cursor.fetchone()

            cursor.execute('select assignment_id from assignments where assignment_name like %s and topic_id=%s', (assignment_name, topic_id))
            assignment_id = cursor.fetchone()

            cursor.execute("SELECT * FROM completed_assgn WHERE student_id = %s AND assignment_id = %s AND topic_id = %s", (student_id, assignment_id, topic_id))
            completed_assignment = cursor.fetchone()

        if completed_assignment:
            return jsonify({"completed": True})
        else:
            return jsonify({"completed": False})
    except pymysql.Error as e:
        return jsonify({"error": f"Database error: {e}"})
    


@app.route('/complete-assignment', methods=['GET','POST'])
def complete_assignment():
    data = request.get_json()
    student_id = session['student_id']
    # assignment_number = data.get('assignment_number')
    assignment_name = data.get('assignment_name')
    topic_name = data.get('topic_name')
    marks = data.get('marks')

    print("In complete_assignment()", end='\n')
    # print("Student_ID: ", student_id)
    print("Assignment Name: ", assignment_name)
    print("Topic Name: ", topic_name)
    print("Total marks: ", marks)

    exp_points_awarded = 10

    try:
        with mysql.cursor() as cursor:

            cursor.execute('select topic_id from topics where topic_name like %s', (topic_name))
            topic_id = cursor.fetchone()
            
            cursor.execute("SELECT assignment_id FROM assignments WHERE assignment_name = %s AND topic_id = %s", (assignment_name,topic_id))
            assignment_row = cursor.fetchone()

            print("Assignment Row: ", assignment_row)

            if assignment_row:
                assignment_id = assignment_row


                cursor.execute("SELECT * FROM completed_assgn WHERE student_id = %s AND assignment_id = %s AND topic_id = %s", (student_id, assignment_id, topic_id))
                if cursor.fetchone():
                    return jsonify({"error": "Assignment already completed"})

                cursor.execute("INSERT INTO completed_assgn (student_id, assignment_id, topic_id, marks) VALUES (%s, %s, %s, %s)", (student_id, assignment_id, topic_id, marks))
                mysql.commit()

                cursor.execute("UPDATE leaderboard SET exp_points = exp_points + %s, marks = marks + %s WHERE student_id = %s", (exp_points_awarded, marks, student_id))

                cursor.execute("SELECT COUNT(*) FROM assignments")
                total_assignments = cursor.fetchone()[0]

                # cursor.execute("SELECT COUNT(*) FROM completed_assgn WHERE student_id = %s AND assignment_id IN (SELECT assignment_id FROM assignments WHERE topic_id = %s)", (student_id, topic_id))
                cursor.execute("SELECT COUNT(*) FROM completed_assgn where student_id=%s", (student_id))
                completed_assignments = cursor.fetchone()[0]
                progress_percentage = round((completed_assignments / total_assignments)*100)
                print('\n Percentage progress: ', progress_percentage)
                cursor.execute("UPDATE leaderboard SET progress_percentage = %s WHERE student_id = %s", (progress_percentage, student_id))

                cursor.execute('select * from leaderboard')
                board = cursor.fetchone()

                print('\nMarks: ', board[3])
                print('\nExp points: ', board[1])
                # print('\n percent: ', board[2])

                mysql.commit()

                return jsonify({"success": True, "progress_percentage": progress_percentage})
            else:
                return jsonify({"error": "Assignment not found"}) 
    except pymysql.Error as e:
        return jsonify({"error": f"Database error: {e}"})






@app.route('/map')
def map_page():
    if 'loggedin' in session:
        return render_template('map.html')
    else:
        return redirect(url_for('login'))
    


    


# def run_foo():
#     obj = MainClass()
#     while True:
#         obj.foo()


# foo_thread = threading.Thread(target=run_foo)
# foo_thread.start()



if __name__ == '__main__':
    # print(len(courses['LANGUAGE AND LITERATURE']['description']))
    app.run(debug=True)


    
