ALIASES = {
    "quantum": "quantum mechanics", "qm": "quantum mechanics",
    "ml": "machine learning", "ai": "artificial intelligence",
    "python": "python programming", "ds": "data structures",
    "cnn": "convolutional neural network", "nlp": "natural language processing",
    "stats": "statistics", "urban water": "urban water management",
}

TOPICS = {
    "quantum mechanics": {
        "title":"Quantum Mechanics",
        "hook":"Tiny particles do not always behave like everyday objects, so we need a special rulebook.",
        "definition":"Quantum mechanics is the branch of physics that explains how very small things such as electrons, photons, and atoms behave.",
        "simple":"Think of a quantum particle like a tiny object that can be described by possibilities before we measure it.",
        "facts":["Quantum mechanics studies matter and energy at very small scales.","Particles can show both particle-like and wave-like behavior.","Probability is used because outcomes are not always fixed before measurement."],
        "concepts":{
            "superposition":{"definition":"Superposition means a quantum system can be described as a combination of possible states before measurement.","kid":"It is like a spinning coin before it lands. We cannot call it only heads or only tails yet.","example":"An electron can be described as having different possible states until we measure it.","mistake":"It does not mean big everyday objects literally become many magical copies.","exam":"Mention possible states, measurement, and probability."},
            "uncertainty":{"definition":"Uncertainty means some pairs of properties cannot both be known perfectly at the same time.","kid":"If you know one thing very clearly, another related thing becomes less clear.","example":"Knowing a tiny particle's position very accurately makes momentum less certain.","mistake":"It is not only because our instruments are bad.","exam":"Explain that uncertainty is a fundamental quantum limit."},
            "wave particle duality":{"definition":"Wave-particle duality means tiny things can show both wave-like and particle-like behavior.","kid":"Sometimes it acts like a small ball, and sometimes it spreads like a wave.","example":"Light can behave like waves in interference and like particles in the photoelectric effect.","mistake":"It is not switching randomly like a human choosing clothes.","exam":"Use light or electron examples."}
        },
        "applications":{"quantum computing":"Uses quantum states to process information.","semiconductors":"Modern electronics depend on quantum behavior.","lasers":"Laser technology depends on quantum transitions."},
        "misconceptions":["Quantum mechanics is not just normal physics with smaller objects.","Superposition does not mean everything is magically everywhere in daily life.","Uncertainty is not only a measurement error; it is a basic limit."],
        "class_questions":["Why do quantum systems need probability?","What exactly changes when measurement happens?","How is superposition used in quantum computing?","Why does light behave like both a wave and a particle?","Can uncertainty ever be removed completely?"]
    },
    "machine learning": {
        "title":"Machine Learning",
        "hook":"Instead of writing every rule by hand, we let computers learn patterns from examples.",
        "definition":"Machine learning is a field of AI where computers learn patterns from data and use them to make predictions or decisions.",
        "simple":"It is like teaching a child by showing many examples instead of only giving written rules.",
        "facts":["Machine learning uses data to train models.","A model learns relationships between features and outcomes.","Good testing is needed to check if the model works on new data."],
        "concepts":{
            "model":{"definition":"A model is the learned pattern or rule created from training data.","kid":"It is the computer's learned recipe for making a guess.","example":"A house price model may learn that size and location affect price.","mistake":"A model is not automatically intelligent or always correct.","exam":"Mention training, prediction, and evaluation."},
            "training data":{"definition":"Training data is the set of examples used to teach a model.","kid":"It is the practice book for the computer.","example":"Images of cats and dogs can train a classifier.","mistake":"More data is not always better if the data is noisy or biased.","exam":"Explain examples, features, and labels."},
            "overfitting":{"definition":"Overfitting happens when a model memorizes training data too much and performs poorly on new data.","kid":"It is like memorizing answers from one test but failing when questions change.","example":"A model gets 99% on training data but low accuracy on test data.","mistake":"High training accuracy alone does not prove a good model.","exam":"Mention generalization and test performance."}
        },
        "applications":{"medical prediction":"Models can help predict disease risk.","recommendation systems":"Apps recommend videos, songs, or products.","fraud detection":"Banks can detect unusual transactions."},
        "misconceptions":["Machine learning is not magic; it depends on data quality.","High training accuracy does not guarantee real-world performance.","A model can be biased if the data is biased."],
        "class_questions":["What is the difference between training and testing?","Why can overfitting be dangerous?","How do features affect model performance?","Why do we need evaluation metrics?","How can bias enter a machine learning system?"]
    },
    "python programming": {
        "title":"Python Programming","hook":"Python helps us write instructions for computers in a clear and readable way.","definition":"Python is a high-level programming language used for web apps, data analysis, AI, automation, and education.","simple":"Python is like writing a clear recipe that a computer can follow step by step.","facts":["Python uses readable syntax.","Variables store values.","Functions help reuse code."],
        "concepts":{"variable":{"definition":"A variable is a name that stores a value.","kid":"It is like a labeled box where we keep something.","example":"age = 20 stores the number 20 in the name age.","mistake":"The variable name is not the same as the value inside it.","exam":"Mention name, value, and memory."},"function":{"definition":"A function is a reusable block of code that performs a task.","kid":"It is like a small machine: give input, get output.","example":"A function can calculate average marks.","mistake":"Writing code once inside a function does not run it until you call it.","exam":"Mention input, process, output, and reuse."},"loop":{"definition":"A loop repeats a block of code.","kid":"It tells the computer to do the same action again and again.","example":"Printing all names in a list uses a loop.","mistake":"A loop without a stopping condition can run forever.","exam":"Mention repetition and control condition."}},
        "applications":{"AI":"Python is widely used in machine learning.","automation":"Python can automate repetitive tasks.","data analysis":"Python can clean and analyze data."},
        "misconceptions":["Python being easy to read does not mean logic is automatic.","If code runs once, it may still fail for other inputs.","Copying code without understanding does not build programming skill."],
        "class_questions":["Why are functions useful?","How does a loop reduce repeated work?","What happens when a variable value changes?","Why is Python popular in AI?","How can we avoid errors in Python?"]
    },
    "data structures": {
        "title":"Data Structures","hook":"Programs become faster and cleaner when data is organized in the right way.","definition":"Data structures are ways of storing and organizing data so it can be used efficiently.","simple":"It is like choosing the right container: a shelf, a queue line, or a box.","facts":["Lists store ordered items.","Stacks follow last-in, first-out.","Queues follow first-in, first-out."],
        "concepts":{"stack":{"definition":"A stack is a data structure where the last item added is removed first.","kid":"It is like a pile of plates: you take the top plate first.","example":"Undo operations often use a stack.","mistake":"A stack is not the same as a queue.","exam":"Mention LIFO: last in, first out."},"queue":{"definition":"A queue is a data structure where the first item added is removed first.","kid":"It is like waiting in line at a shop.","example":"Printer tasks can be handled using a queue.","mistake":"Queue order is not random.","exam":"Mention FIFO: first in, first out."},"tree":{"definition":"A tree is a hierarchical data structure with nodes and branches.","kid":"It is like a family tree with parents and children.","example":"Folders in a computer can be represented as a tree.","mistake":"A tree is not just a drawing; it stores relationships.","exam":"Mention root, nodes, children, and hierarchy."}},
        "applications":{"search":"Data structures help find information quickly.","operating systems":"Queues and trees are used in system tasks.","databases":"Indexes use tree-like structures."},
        "misconceptions":["There is no single best data structure for every problem.","Stack and queue order are not interchangeable.","A graph data structure is not the same as a chart."],
        "class_questions":["When should we use a stack?","Why is a queue useful?","How does a tree organize hierarchy?","How do data structures affect speed?","Why does choosing the right structure matter?"]
    },
}

def canonical_key(topic: str) -> str:
    key = " ".join(str(topic).strip().lower().split())
    return ALIASES.get(key, key)

def validate_topics():
    errors=[]
    required=["title","hook","definition","simple","concepts","applications","misconceptions","class_questions"]
    for key, topic in TOPICS.items():
        for field in required:
            if field not in topic or not topic[field]: errors.append(f"{key}: missing {field}")
        for cname, concept in topic.get("concepts", {}).items():
            for field in ["definition","kid","example","mistake","exam"]:
                if field not in concept or not concept[field]: errors.append(f"{key}.{cname}: missing {field}")
    return errors

EXTRA_MASSIVE_TOPICS = {
    "database management system": {
        "title": "Database Management System",
        "hook": "A DBMS helps store, organize, and retrieve data safely.",
        "definition": "A database management system is software used to create, manage, and access databases.",
        "simple": "It is like a smart digital filing cabinet.",
        "facts": ["DBMS stores structured data.", "SQL is often used to query data.", "DBMS improves data security and consistency."],
        "concepts": {
            "table": {"definition": "A table stores data in rows and columns.", "kid": "It is like a spreadsheet.", "example": "A student table stores name, ID, and marks.", "mistake": "A table is not the whole database.", "exam": "Mention rows, columns, and records."},
            "primary key": {"definition": "A primary key uniquely identifies each row.", "kid": "It is like a unique ID card.", "example": "Student ID can be a primary key.", "mistake": "Primary key should not repeat.", "exam": "Mention uniqueness."},
            "query": {"definition": "A query asks the database for specific data.", "kid": "It is a question to the database.", "example": "SELECT name FROM students.", "mistake": "A query is not only for deleting data.", "exam": "Mention retrieving or manipulating data."}
        },
        "applications": {"banking": "Stores account records.", "university": "Stores student information.", "e-commerce": "Stores orders and products."},
        "misconceptions": ["A DBMS is not just an Excel file.", "Data security matters.", "Good database design reduces errors."],
        "class_questions": ["Why do we need DBMS?", "What is a primary key?", "How does SQL work?", "What is normalization?", "How does DBMS protect data?"]
    },
    "software engineering": {
        "title": "Software Engineering",
        "hook": "Good software needs planning, design, testing, and maintenance.",
        "definition": "Software engineering is the systematic process of designing, building, testing, and maintaining software.",
        "simple": "It is like building a house, but the house is an app or program.",
        "facts": ["Requirements guide development.", "Testing reduces bugs.", "Maintenance keeps software useful."],
        "concepts": {
            "requirement": {"definition": "A requirement describes what the software should do.", "kid": "It is the wish list for the app.", "example": "A login feature is a requirement.", "mistake": "Unclear requirements cause wrong products.", "exam": "Mention user needs."},
            "testing": {"definition": "Testing checks whether software works correctly.", "kid": "It is checking homework before submission.", "example": "Unit tests check small parts.", "mistake": "Testing cannot be skipped.", "exam": "Mention quality assurance."},
            "maintenance": {"definition": "Maintenance updates and fixes software after release.", "kid": "It is taking care of the app after making it.", "example": "Fixing bugs after deployment.", "mistake": "Software work does not end after release.", "exam": "Mention bug fixes and updates."}
        },
        "applications": {"app development": "Build reliable apps.", "project management": "Plan team work.", "quality assurance": "Reduce software failure."},
        "misconceptions": ["Coding is only one part.", "Testing is not optional.", "Documentation matters."],
        "class_questions": ["What is software engineering?", "Why are requirements important?", "Why test software?", "What is maintenance?", "How do teams build software?"]
    },
    "cybersecurity": {
        "title": "Cybersecurity",
        "hook": "Cybersecurity protects systems, networks, and data from digital attacks.",
        "definition": "Cybersecurity is the practice of protecting computers, networks, and data from unauthorized access or damage.",
        "simple": "It is like locking doors for your digital life.",
        "facts": ["Strong passwords help security.", "Phishing is a common attack.", "Encryption protects data."],
        "concepts": {
            "phishing": {"definition": "Phishing tricks users into giving sensitive information.", "kid": "A fake message tries to steal your password.", "example": "Fake bank emails.", "mistake": "Real-looking links can still be dangerous.", "exam": "Mention social engineering."},
            "encryption": {"definition": "Encryption changes readable data into protected code.", "kid": "It turns a message into secret writing.", "example": "HTTPS uses encryption.", "mistake": "Encryption is not the same as deletion.", "exam": "Mention confidentiality."},
            "malware": {"definition": "Malware is harmful software.", "kid": "It is a bad program that can damage or steal.", "example": "Viruses and ransomware.", "mistake": "Malware can come from unknown downloads.", "exam": "Mention malicious software."}
        },
        "applications": {"banking": "Protect financial data.", "healthcare": "Protect patient data.", "personal security": "Protect accounts."},
        "misconceptions": ["Cybersecurity is not only antivirus.", "Humans can be weak points.", "No system is perfectly safe."],
        "class_questions": ["What is phishing?", "Why use encryption?", "How does malware spread?", "How can users stay safe?", "Why is cybersecurity important?"]
    },
    "operating system": {
        "title": "Operating System",
        "hook": "An operating system manages hardware and software resources.",
        "definition": "An operating system is system software that manages computer hardware, software resources, and services for programs.",
        "simple": "It is the manager of the computer.",
        "facts": ["OS manages memory.", "OS schedules processes.", "OS handles files and devices."],
        "concepts": {
            "process": {"definition": "A process is a running program.", "kid": "It is a program that is currently working.", "example": "A browser running on your computer.", "mistake": "A process is not the same as a file.", "exam": "Mention execution."},
            "memory management": {"definition": "Memory management controls how programs use RAM.", "kid": "It gives working space to programs.", "example": "Allocating memory to apps.", "mistake": "RAM is limited.", "exam": "Mention allocation and protection."},
            "file system": {"definition": "A file system organizes files on storage.", "kid": "It is the computer's folder system.", "example": "NTFS or ext4.", "mistake": "Files are not stored randomly.", "exam": "Mention organization and access."}
        },
        "applications": {"computers": "Run applications.", "phones": "Manage mobile apps.", "servers": "Control services."},
        "misconceptions": ["OS is not only the desktop screen.", "Hardware needs OS control.", "Processes use resources."],
        "class_questions": ["What does an OS do?", "What is a process?", "Why manage memory?", "How are files organized?", "What is scheduling?"]
    },
    "computer network": {
        "title": "Computer Network",
        "hook": "Networks allow computers to communicate and share resources.",
        "definition": "A computer network is a group of connected devices that exchange data.",
        "simple": "It is like roads connecting computers.",
        "facts": ["Networks use protocols.", "IP addresses identify devices.", "Routers forward data."],
        "concepts": {
            "protocol": {"definition": "A protocol is a set of communication rules.", "kid": "It is the language rules computers follow.", "example": "HTTP is used for web communication.", "mistake": "Devices need common rules.", "exam": "Mention communication standard."},
            "ip address": {"definition": "An IP address identifies a device on a network.", "kid": "It is like a house address for a computer.", "example": "192.168.1.1.", "mistake": "IP is not the same as website name.", "exam": "Mention identification."},
            "router": {"definition": "A router forwards data between networks.", "kid": "It directs traffic.", "example": "Home Wi-Fi router.", "mistake": "Router is not just Wi-Fi.", "exam": "Mention packet forwarding."}
        },
        "applications": {"internet": "Connects global devices.", "office": "Shares files and printers.", "cloud": "Connects users to services."},
        "misconceptions": ["Internet and network are related but not identical.", "Wi-Fi is not the whole network.", "Protocols are essential."],
        "class_questions": ["What is a protocol?", "Why need IP addresses?", "What does a router do?", "How does data travel?", "What is LAN vs WAN?"]
    },
    "linear regression": {
        "title": "Linear Regression",
        "hook": "Linear regression predicts a value using a straight-line relationship.",
        "definition": "Linear regression is a statistical method that models the relationship between input variables and a continuous output.",
        "simple": "It draws a best-fit line to make predictions.",
        "facts": ["It predicts continuous values.", "It uses slope and intercept.", "Error measures show fit quality."],
        "concepts": {
            "slope": {"definition": "Slope shows how much output changes when input changes.", "kid": "It tells how steep the line is.", "example": "More study hours may increase score.", "mistake": "Slope does not always prove causation.", "exam": "Mention rate of change."},
            "intercept": {"definition": "Intercept is the predicted output when input is zero.", "kid": "Where the line starts.", "example": "Base score when study hours are zero.", "mistake": "Intercept may not always be meaningful.", "exam": "Mention y-axis crossing."},
            "error": {"definition": "Error is the difference between actual and predicted values.", "kid": "How far the guess is from truth.", "example": "Predicted 80, actual 75.", "mistake": "Low error is good but not everything.", "exam": "Mention residual."}
        },
        "applications": {"price prediction": "Predict house prices.", "sales": "Forecast revenue.", "education": "Study score prediction."},
        "misconceptions": ["Correlation is not causation.", "A straight line may not fit all data.", "Outliers can affect regression."],
        "class_questions": ["What is slope?", "What is intercept?", "How is error measured?", "When is linear regression useful?", "What are limitations?"]
    },
    "logistic regression": {
        "title": "Logistic Regression",
        "hook": "Logistic regression predicts categories like yes/no or 0/1.",
        "definition": "Logistic regression is a classification method used to estimate the probability of a binary outcome.",
        "simple": "It predicts the chance of something being yes or no.",
        "facts": ["It outputs probability.", "It is used for classification.", "Sigmoid function maps values between 0 and 1."],
        "concepts": {
            "sigmoid": {"definition": "Sigmoid maps any number to a value between 0 and 1.", "kid": "It turns a score into a probability.", "example": "Diabetes risk probability.", "mistake": "Probability is not always certainty.", "exam": "Mention 0 to 1 output."},
            "classification": {"definition": "Classification predicts a category.", "kid": "It chooses a label.", "example": "Spam or not spam.", "mistake": "Classification is not predicting continuous price.", "exam": "Mention labels."},
            "threshold": {"definition": "A threshold converts probability into class label.", "kid": "Above this line means yes.", "example": "If probability > 0.5, classify as 1.", "mistake": "Threshold can be adjusted.", "exam": "Mention decision boundary."}
        },
        "applications": {"medicine": "Disease risk prediction.", "email": "Spam detection.", "finance": "Fraud risk."},
        "misconceptions": ["It is classification, not ordinary linear regression.", "Probability needs threshold.", "Model results need evaluation."],
        "class_questions": ["Why use sigmoid?", "What is a threshold?", "What is binary classification?", "How evaluate the model?", "Where is it used?"]
    },
    "decision tree": {
        "title": "Decision Tree",
        "hook": "A decision tree makes decisions using a tree of questions.",
        "definition": "A decision tree is a machine learning model that splits data using decision rules.",
        "simple": "It is like a flowchart of yes/no questions.",
        "facts": ["It can be used for classification and regression.", "Splits are based on features.", "Trees can overfit."],
        "concepts": {
            "node": {"definition": "A node is a decision point or result in a tree.", "kid": "It is one question box.", "example": "Is glucose high?", "mistake": "Not every node is final.", "exam": "Mention decision point."},
            "leaf": {"definition": "A leaf is a final output node.", "kid": "It is the final answer box.", "example": "Diabetes: yes/no.", "mistake": "Leaf has no further split.", "exam": "Mention final prediction."},
            "split": {"definition": "A split divides data based on a feature.", "kid": "It separates examples into groups.", "example": "Age > 40.", "mistake": "Bad splits reduce performance.", "exam": "Mention feature condition."}
        },
        "applications": {"medical screening": "Risk decision rules.", "banking": "Loan approval.", "education": "Student performance prediction."},
        "misconceptions": ["Easy to read does not mean always accurate.", "Deep trees can overfit.", "Feature choice matters."],
        "class_questions": ["What is a node?", "What is a leaf?", "How does a split work?", "Why can trees overfit?", "Where are decision trees used?"]
    },
    "neural network": {
        "title": "Neural Network",
        "hook": "Neural networks learn patterns using layers of connected units.",
        "definition": "A neural network is a machine learning model made of connected layers that transform inputs into outputs.",
        "simple": "It is like many small calculators working together to learn patterns.",
        "facts": ["Neural networks use weights.", "Activation functions add non-linearity.", "Training adjusts weights."],
        "concepts": {
            "weight": {"definition": "A weight controls the strength of a connection.", "kid": "It says how important an input is.", "example": "Glucose may have strong weight in diabetes prediction.", "mistake": "Weights are learned, not guessed randomly forever.", "exam": "Mention learned parameter."},
            "activation": {"definition": "An activation function decides how a neuron passes information.", "kid": "It helps the network choose what signal to send.", "example": "ReLU activation.", "mistake": "Without activation, deep layers lose power.", "exam": "Mention non-linearity."},
            "training": {"definition": "Training adjusts weights using data.", "kid": "Practice makes the model better.", "example": "Using patient data to train a model.", "mistake": "Training too much can overfit.", "exam": "Mention loss and optimization."}
        },
        "applications": {"vision": "Image recognition.", "language": "Text models.", "medicine": "Risk prediction."},
        "misconceptions": ["Neural networks are not human brains.", "More layers are not always better.", "They need data and evaluation."],
        "class_questions": ["What are weights?", "Why use activation?", "How does training work?", "What is overfitting?", "Where are neural networks used?"]
    },
    "cloud computing": {
        "title": "Cloud Computing",
        "hook": "Cloud computing provides computing services over the internet.",
        "definition": "Cloud computing delivers servers, storage, databases, networking, software, and analytics through the internet.",
        "simple": "It is like renting computer power online.",
        "facts": ["Cloud can reduce local hardware needs.", "Services can scale up or down.", "Security and cost must be managed."],
        "concepts": {
            "server": {"definition": "A server provides services or data to users.", "kid": "It is a computer that serves others.", "example": "A web server hosts a website.", "mistake": "Server does not mean only a big physical box.", "exam": "Mention service provider."},
            "scalability": {"definition": "Scalability means handling more users or work.", "kid": "The system can grow when more people come.", "example": "Adding more cloud resources during exams.", "mistake": "Scaling can increase cost.", "exam": "Mention growth capacity."},
            "storage": {"definition": "Cloud storage keeps data online.", "kid": "Files are saved on internet servers.", "example": "Google Drive.", "mistake": "Cloud storage still needs security.", "exam": "Mention remote data storage."}
        },
        "applications": {"web apps": "Host apps online.", "backup": "Store backup files.", "AI": "Train and deploy models."},
        "misconceptions": ["Cloud is not magic; it uses real servers.", "Cloud can have security risks.", "Cost must be controlled."],
        "class_questions": ["What is cloud computing?", "Why use cloud?", "What is scalability?", "What are risks?", "Where is it used?"]
    },
}
TOPICS.update(EXTRA_MASSIVE_TOPICS)

# ── Additional topics added in V17 ──────────────────────────────────────────

EXTRA_V17_TOPICS = {
    "artificial intelligence": {
        "title": "Artificial Intelligence",
        "hook": "AI is about building systems that can reason, learn, and act in ways that seem intelligent.",
        "definition": "Artificial intelligence is the field of computer science that focuses on building machines capable of performing tasks that normally require human intelligence.",
        "simple": "Think of AI as teaching computers to think and learn instead of just following fixed instructions.",
        "facts": [
            "AI includes machine learning, natural language processing, and computer vision.",
            "AI systems learn from data and improve with experience.",
            "AI is used in medicine, finance, transportation, and education.",
        ],
        "concepts": {
            "machine intelligence": {
                "definition": "Machine intelligence refers to the ability of a computer system to perform tasks that would normally require human reasoning.",
                "kid": "It means the computer can think a little bit like a person for specific tasks.",
                "example": "A spam filter that learns which emails are junk is using machine intelligence.",
                "mistake": "AI is not a brain; it is a mathematical system trained on data.",
                "exam": "Mention training, data, and specific task performance.",
            },
            "search and optimization": {
                "definition": "Search algorithms explore possible solutions to find the best answer for a given problem.",
                "kid": "It is like trying many doors to find the one that opens.",
                "example": "GPS navigation finds the shortest route using search algorithms.",
                "mistake": "Brute force search is not always the same as intelligent search.",
                "exam": "Mention goal, possible states, and evaluation.",
            },
            "knowledge representation": {
                "definition": "Knowledge representation is the way information about the world is stored so an AI system can reason about it.",
                "kid": "It is like writing down all rules a computer needs to make decisions.",
                "example": "A medical AI stores facts about symptoms and diseases to help doctors.",
                "mistake": "More stored knowledge does not always mean better decisions.",
                "exam": "Mention facts, rules, inference, and reasoning.",
            },
        },
        "applications": {
            "healthcare": "AI helps diagnose diseases from medical images.",
            "autonomous vehicles": "Self-driving cars use AI for navigation and decision making.",
            "natural language": "Voice assistants like chatbots use AI to understand text.",
        },
        "misconceptions": [
            "AI is not a single technology; it is a collection of methods.",
            "Current AI does not think or feel; it recognizes patterns in data.",
            "AI replacing humans in every job is an exaggerated prediction.",
        ],
        "class_questions": [
            "What separates AI from traditional programming?",
            "How does a machine learn from data?",
            "What is the role of training data in AI?",
            "Where does AI fail and why?",
            "How is AI used in one field you know well?",
        ],
    },
    "natural language processing": {
        "title": "Natural Language Processing",
        "hook": "NLP teaches computers to read, understand, and generate human language.",
        "definition": "Natural language processing is a branch of AI that enables computers to understand, interpret, and produce human language in a meaningful way.",
        "simple": "NLP is what allows a computer to read a sentence and understand what it means, not just match words.",
        "facts": [
            "NLP combines linguistics and machine learning.",
            "Tokenization splits text into words or sentences for processing.",
            "Modern NLP uses transformer models trained on large text datasets.",
        ],
        "concepts": {
            "tokenization": {
                "definition": "Tokenization is the process of splitting text into smaller units such as words, subwords, or characters.",
                "kid": "It is like cutting a sentence into separate word pieces before processing.",
                "example": "The sentence 'I love Python' is tokenized into ['I', 'love', 'Python'].",
                "mistake": "Tokenization is not the same as understanding meaning.",
                "exam": "Mention splitting, units, and the purpose before modeling.",
            },
            "sentiment analysis": {
                "definition": "Sentiment analysis determines whether a text expresses positive, negative, or neutral opinion.",
                "kid": "It reads a review and decides if the person was happy or unhappy.",
                "example": "A company analyzes customer tweets to understand satisfaction levels.",
                "mistake": "Sarcasm and context are difficult for simple sentiment models.",
                "exam": "Mention classification, positive or negative label, and training data.",
            },
            "language model": {
                "definition": "A language model learns the probability of word sequences and can predict the next word in text.",
                "kid": "It is a system that has read so much text it can guess what comes next.",
                "example": "Autocomplete on a phone uses a language model.",
                "mistake": "A language model does not understand meaning the way humans do.",
                "exam": "Mention probability, training corpus, and prediction.",
            },
        },
        "applications": {
            "machine translation": "NLP powers translation apps like Google Translate.",
            "chatbots": "Customer support bots use NLP to answer questions.",
            "search engines": "Search uses NLP to understand user queries better.",
        },
        "misconceptions": [
            "NLP models do not truly understand language; they learn statistical patterns.",
            "Translating word by word without NLP gives poor results.",
            "High accuracy on one language does not mean the model works well for another.",
        ],
        "class_questions": [
            "What is the difference between syntax and semantics in NLP?",
            "How does a language model learn from text?",
            "Why is context important for understanding sentences?",
            "What makes sentiment analysis difficult?",
            "How is NLP used in search engines?",
        ],
    },
    "statistics": {
        "title": "Statistics",
        "hook": "Statistics lets us make sense of data and draw reliable conclusions from uncertain information.",
        "definition": "Statistics is the science of collecting, organizing, analyzing, interpreting, and presenting data to support decision making.",
        "simple": "Statistics is the tool that helps us go from raw numbers to real understanding.",
        "facts": [
            "Descriptive statistics summarize data using measures like mean, median, and variance.",
            "Inferential statistics use samples to draw conclusions about a larger population.",
            "Probability is the foundation of statistical reasoning.",
        ],
        "concepts": {
            "mean and variance": {
                "definition": "The mean is the average value of a dataset. Variance measures how spread out the values are from that average.",
                "kid": "Mean tells you the middle, variance tells you how far apart the numbers are.",
                "example": "Five exam scores: 70, 75, 80, 85, 90 — mean is 80, and variance shows if scores cluster near 80 or spread widely.",
                "mistake": "The mean alone does not describe a dataset fully; variance matters too.",
                "exam": "Know the formula for mean and variance, and explain what each measures.",
            },
            "hypothesis testing": {
                "definition": "Hypothesis testing is a method to decide whether evidence from data supports a specific claim about a population.",
                "kid": "It is like a court trial: we assume innocence first, then check if evidence changes the conclusion.",
                "example": "Testing whether a new drug works better than an old one uses hypothesis testing.",
                "mistake": "Failing to reject the null hypothesis does not prove it is true.",
                "exam": "Mention null hypothesis, p-value, and significance level.",
            },
            "probability distribution": {
                "definition": "A probability distribution describes all possible outcomes and their likelihoods for a random variable.",
                "kid": "It is a map showing how often each possible result happens.",
                "example": "The normal distribution shows that most values fall near the average with fewer at the extremes.",
                "mistake": "Not all real data follow a normal distribution.",
                "exam": "Mention random variable, probability, and shape of the distribution.",
            },
        },
        "applications": {
            "data science": "Statistics is the core of data analysis and machine learning.",
            "public health": "Statistics is used to track disease spread and evaluate treatments.",
            "quality control": "Factories use statistics to detect defects and improve processes.",
        },
        "misconceptions": [
            "Correlation does not imply causation.",
            "A larger sample is not always necessary if the sample is truly random.",
            "Statistical significance is not the same as practical importance.",
        ],
        "class_questions": [
            "What is the difference between descriptive and inferential statistics?",
            "When should we use median instead of mean?",
            "What does a p-value tell us?",
            "How can we tell if two variables are correlated?",
            "Why does sample size affect statistical conclusions?",
        ],
    },
    "convolutional neural network": {
        "title": "Convolutional Neural Network",
        "hook": "CNNs learn to recognize visual patterns by looking at small pieces of an image at a time.",
        "definition": "A convolutional neural network is a type of deep learning model designed to process grid-like data such as images by learning spatial patterns through convolutional filters.",
        "simple": "A CNN scans an image with small filters to find edges, shapes, and then higher-level patterns like faces or objects.",
        "facts": [
            "CNNs use convolutional layers to detect local features like edges.",
            "Pooling layers reduce the size of feature maps to lower computation.",
            "CNNs are the foundation of modern image recognition systems.",
        ],
        "concepts": {
            "convolution": {
                "definition": "Convolution is the operation of sliding a small filter over an input to detect local patterns.",
                "kid": "It is like using a magnifying glass that slides across an image looking for specific shapes.",
                "example": "A filter trained to detect vertical edges will activate strongly on vertical lines in an image.",
                "mistake": "A filter does not understand the whole image at once; it looks at small regions.",
                "exam": "Mention filter, stride, and feature map.",
            },
            "pooling": {
                "definition": "Pooling reduces the spatial dimensions of a feature map while keeping the most important information.",
                "kid": "It shrinks the representation so the network can focus on the big picture.",
                "example": "Max pooling takes the highest value in each small region of the feature map.",
                "mistake": "Pooling reduces size but does not detect new patterns.",
                "exam": "Mention max pooling, spatial reduction, and why it helps generalization.",
            },
            "feature map": {
                "definition": "A feature map is the output produced when a convolutional filter is applied to an input image.",
                "kid": "It is the result image that shows where the filter found its pattern.",
                "example": "An edge-detection filter produces a feature map highlighting edges.",
                "mistake": "Feature maps are not the final classification; they feed into more layers.",
                "exam": "Explain how feature maps from multiple filters are combined in deep CNNs.",
            },
        },
        "applications": {
            "image classification": "CNNs classify images into categories like cats, dogs, or vehicles.",
            "medical imaging": "CNNs detect tumors and abnormalities in X-rays and MRI scans.",
            "face recognition": "Smartphones use CNNs to recognize the owner's face.",
        },
        "misconceptions": [
            "CNNs do not understand images the way humans do; they learn statistical patterns.",
            "More layers do not always mean better performance; depth needs to match the task.",
            "CNNs require large labeled datasets; small datasets often lead to poor results.",
        ],
        "class_questions": [
            "Why are convolutional filters better than fully connected layers for images?",
            "What is the purpose of pooling in a CNN?",
            "How does a CNN learn to detect edges?",
            "What happens to accuracy if training data is too small?",
            "How is a CNN different from a standard neural network?",
        ],
    },
}

# Merge extra V17 topics into the main TOPICS dict
TOPICS.update(EXTRA_V17_TOPICS)
