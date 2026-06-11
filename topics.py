ALIASES = {
    "qm": "quantum mechanics",
    "quantum": "quantum mechanics",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "python": "python programming",
    "cnn": "convolutional neural network",
    "nlp": "natural language processing",
    "dbms": "database management system",
    "os": "operating system",
    "network": "computer network",
}

def concept(definition, kid, example, mistake, exam):
    return {
        "definition": definition,
        "kid": kid,
        "example": example,
        "mistake": mistake,
        "exam": exam,
    }

def make_topic(title, definition, simple, concepts, applications=None, misconceptions=None, questions=None):
    return {
        "title": title,
        "hook": f"{title} becomes easier when students understand the big idea before class.",
        "definition": definition,
        "simple": simple,
        "facts": [
            definition,
            simple,
            f"{title} can be understood better with examples and class questions.",
        ],
        "concepts": concepts,
        "applications": applications or {"class learning": f"{title} helps students prepare for lectures."},
        "misconceptions": misconceptions or [
            f"{title} is not only memorization.",
            "Students should connect the definition with examples.",
            "Online preparation should be checked with teacher notes.",
        ],
        "class_questions": questions or [
            f"What is the simplest definition of {title}?",
            f"Can you give one real example of {title}?",
            f"What is the most important concept in {title}?",
            f"What is a common mistake about {title}?",
            f"How is {title} related to our course?",
        ],
    }

TOPICS = {
    "quantum mechanics": make_topic(
        "Quantum Mechanics",
        "Quantum mechanics is the branch of physics that explains how very small things such as electrons, photons, and atoms behave.",
        "In simple words, tiny particles follow special rules that are different from everyday objects.",
        {
            "superposition": concept(
                "Superposition means a quantum system can be described as a combination of possible states before measurement.",
                "It is like a spinning coin before it lands.",
                "An electron can have different possible states until we measure it.",
                "It does not mean big daily objects become magical copies.",
                "Mention possible states, measurement, and probability.",
            ),
            "uncertainty": concept(
                "Uncertainty means some pairs of properties cannot both be known perfectly at the same time.",
                "If one thing becomes very clear, another related thing becomes less clear.",
                "Knowing a particle position very accurately makes momentum less certain.",
                "It is not only because instruments are weak.",
                "Mention the fundamental limit of measurement.",
            ),
        },
        {"quantum computing": "Uses quantum states to process information.", "semiconductors": "Modern electronics depend on quantum behavior."},
    ),
    "machine learning": make_topic(
        "Machine Learning",
        "Machine learning is a field of AI where computers learn patterns from data and use them to make predictions or decisions.",
        "It is like teaching a computer through examples instead of writing every rule by hand.",
        {
            "model": concept(
                "A model is the learned pattern created from training data.",
                "It is the computer's learned recipe for making a guess.",
                "A house-price model may learn from size and location.",
                "A model is not automatically always correct.",
                "Mention training, prediction, and evaluation.",
            ),
            "overfitting": concept(
                "Overfitting happens when a model memorizes training data too much and performs poorly on new data.",
                "It is like memorizing one test but failing when questions change.",
                "A model has high training accuracy but low test accuracy.",
                "High training accuracy alone is not enough.",
                "Mention generalization and test performance.",
            ),
        },
        {"medical prediction": "Predict disease risk.", "recommendation": "Suggest videos, songs, or products."},
    ),
    "python programming": make_topic(
        "Python Programming",
        "Python is a high-level programming language used for data, AI, automation, and web apps.",
        "Python is like writing a clear recipe that a computer can follow step by step.",
        {
            "function": concept(
                "A function is a reusable block of code that performs a task.",
                "It is like a small machine: give input and get output.",
                "A function can calculate average marks.",
                "Code inside a function runs only when called.",
                "Mention input, process, output, and reuse.",
            ),
            "loop": concept(
                "A loop repeats a block of code.",
                "It tells the computer to do the same action again and again.",
                "A loop can print all names in a list.",
                "A loop without stopping condition can run forever.",
                "Mention repetition and control condition.",
            ),
        },
        {"AI": "Python is widely used in machine learning.", "automation": "Python can automate repetitive tasks."},
    ),
    "data structures": make_topic(
        "Data Structures",
        "Data structures are ways of storing and organizing data so it can be used efficiently.",
        "It is like choosing the right container for different kinds of information.",
        {
            "stack": concept(
                "A stack follows last-in, first-out order.",
                "It is like a pile of plates.",
                "Undo operations often use a stack.",
                "A stack is not the same as a queue.",
                "Mention LIFO.",
            ),
            "queue": concept(
                "A queue follows first-in, first-out order.",
                "It is like waiting in line.",
                "Printer jobs can use a queue.",
                "Queue order is not random.",
                "Mention FIFO.",
            ),
        },
        {"search": "Data structures help find information quickly.", "databases": "Indexes use tree-like structures."},
    ),
    "artificial intelligence": make_topic(
        "Artificial Intelligence",
        "Artificial intelligence is the field of building systems that can learn, reason, perceive, or make decisions.",
        "AI is like a smart helper that can make useful guesses but still needs human checking.",
        {"bias": concept("Bias happens when a system gives unfair or distorted results.", "The computer learns a wrong habit from unfair examples.", "A model trained on limited data may fail for other groups.", "AI results are not always neutral.", "Mention data quality and fairness.")},
    ),
    "convolutional neural network": make_topic(
        "Convolutional Neural Network",
        "A convolutional neural network is a deep learning model mainly used for image and visual pattern recognition.",
        "A CNN first notices small patterns like edges, then combines them into bigger objects.",
        {"filter": concept("A filter is a small matrix that scans an image to detect a pattern.", "It is a tiny window looking for lines or shapes.", "A filter can detect vertical edges.", "A filter is learned, not always manually written.", "Mention scanning and feature detection.")},
    ),
    "natural language processing": make_topic(
        "Natural Language Processing",
        "Natural language processing is a field of AI that helps computers understand, analyze, and generate human language.",
        "NLP teaches computers to read, listen, and reply more usefully.",
        {"token": concept("A token is a small piece of text used by an NLP system.", "A sentence is broken into small pieces.", "Words or subwords can be tokens.", "A token is not always a full word.", "Mention text splitting.")},
    ),
    "statistics": make_topic(
        "Statistics",
        "Statistics is the study of collecting, summarizing, analyzing, and interpreting data.",
        "Statistics helps us understand the story behind many numbers.",
        {"variance": concept("Variance measures how spread out numbers are.", "It shows how far numbers usually are from the average.", "Two classes can have the same average but different spread.", "Variance is not the same as ANOVA.", "Mention deviation from mean.")},
    ),
    "urban water management": make_topic(
        "Urban Water Management",
        "Urban water management is the planning and control of water supply, wastewater, drainage, and flood risk in cities.",
        "A city needs clean water coming in and dirty or rain water going out safely.",
        {"drainage": concept("Drainage removes excess rainwater from urban areas.", "It is the city's way of carrying rainwater away.", "Storm drains reduce street flooding.", "Drainage is not the same as drinking water supply.", "Mention flood prevention.")},
    ),
    "database management system": make_topic(
        "Database Management System",
        "A database management system is software used to create, manage, and access databases.",
        "It is like a smart digital filing cabinet.",
        {"primary key": concept("A primary key uniquely identifies each row.", "It is like a unique ID card.", "Student ID can be a primary key.", "Primary key should not repeat.", "Mention uniqueness.")},
    ),
    "software engineering": make_topic(
        "Software Engineering",
        "Software engineering is the systematic process of designing, building, testing, and maintaining software.",
        "It is like building a house, but the house is an app or program.",
        {"testing": concept("Testing checks whether software works correctly.", "It is checking homework before submission.", "Unit tests check small parts.", "Testing cannot be skipped.", "Mention quality assurance.")},
    ),
    "cybersecurity": make_topic(
        "Cybersecurity",
        "Cybersecurity is the practice of protecting computers, networks, and data from unauthorized access or damage.",
        "It is like locking doors for your digital life.",
        {"phishing": concept("Phishing tricks users into giving sensitive information.", "A fake message tries to steal your password.", "Fake bank emails are examples.", "Real-looking links can still be dangerous.", "Mention social engineering.")},
    ),
    "operating system": make_topic(
        "Operating System",
        "An operating system is system software that manages computer hardware, software resources, and services for programs.",
        "It is the manager of the computer.",
        {"process": concept("A process is a running program.", "It is a program that is currently working.", "A browser running on your computer is a process.", "A process is not the same as a file.", "Mention execution.")},
    ),
    "computer network": make_topic(
        "Computer Network",
        "A computer network is a group of connected devices that exchange data.",
        "It is like roads connecting computers.",
        {"protocol": concept("A protocol is a set of communication rules.", "It is the language rules computers follow.", "HTTP is used for web communication.", "Devices need common rules.", "Mention communication standard.")},
    ),
    "linear regression": make_topic(
        "Linear Regression",
        "Linear regression is a statistical method that models the relationship between input variables and a continuous output.",
        "It draws a best-fit line to make predictions.",
        {"slope": concept("Slope shows how much output changes when input changes.", "It tells how steep the line is.", "More study hours may increase score.", "Slope does not always prove causation.", "Mention rate of change.")},
    ),
    "logistic regression": make_topic(
        "Logistic Regression",
        "Logistic regression is a classification method used to estimate the probability of a binary outcome.",
        "It predicts the chance of something being yes or no.",
        {"sigmoid": concept("Sigmoid maps any number to a value between 0 and 1.", "It turns a score into a probability.", "It can show disease risk probability.", "Probability is not always certainty.", "Mention 0 to 1 output.")},
    ),
    "decision tree": make_topic(
        "Decision Tree",
        "A decision tree is a machine learning model that splits data using decision rules.",
        "It is like a flowchart of yes/no questions.",
        {"node": concept("A node is a decision point or result in a tree.", "It is one question box.", "Is glucose high? can be a node.", "Not every node is final.", "Mention decision point.")},
    ),
    "neural network": make_topic(
        "Neural Network",
        "A neural network is a machine learning model made of connected layers that transform inputs into outputs.",
        "It is like many small calculators working together to learn patterns.",
        {"weight": concept("A weight controls the strength of a connection.", "It says how important an input is.", "Glucose may have strong weight in diabetes prediction.", "Weights are learned during training.", "Mention learned parameter.")},
    ),
    "cloud computing": make_topic(
        "Cloud Computing",
        "Cloud computing delivers servers, storage, databases, networking, software, and analytics through the internet.",
        "It is like renting computer power online.",
        {"scalability": concept("Scalability means handling more users or work.", "The system can grow when more people come.", "Adding more cloud resources during exams.", "Scaling can increase cost.", "Mention growth capacity.")},
    ),
}

def canonical_key(topic: str) -> str:
    key = " ".join(str(topic).strip().lower().split())
    return ALIASES.get(key, key)

def validate_topics():
    errors = []
    required = ["title", "hook", "definition", "simple", "concepts", "applications", "misconceptions", "class_questions"]
    for key, topic in TOPICS.items():
        for field in required:
            if field not in topic or not topic[field]:
                errors.append(f"{key}: missing {field}")
        for cname, c in topic.get("concepts", {}).items():
            for field in ["definition", "kid", "example", "mistake", "exam"]:
                if field not in c or not c[field]:
                    errors.append(f"{key}.{cname}: missing {field}")
    return errors

def _build_topic_options():
    titles = []
    for item in TOPICS.values():
        if isinstance(item, dict) and item.get("title"):
            titles.append(item["title"])
    return sorted(set(titles)) + ["Custom Topic"]

TOPIC_OPTIONS = _build_topic_options()
