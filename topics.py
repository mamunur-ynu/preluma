import re

ALIASES = {
    "quantum": "quantum mechanics", "qm": "quantum mechanics",
    "ml": "machine learning", "ai": "artificial intelligence",
    "python": "python programming", "ds": "data structures",
    "cnn": "convolutional neural network", "nlp": "natural language processing",
    "stats": "statistics", "urban water": "urban water management",
    "oop": "object oriented programming", "os": "operating systems",
    "dbms": "database management systems", "db": "database management systems",
    "algo": "algorithms", "dsa": "data structures and algorithms",
    "cv": "computer vision", "dl": "deep learning", "nn": "neural networks",
    "calculus": "calculus", "linear algebra": "linear algebra",
    "physics": "physics", "chemistry": "chemistry", "biology": "biology",
    "economics": "economics", "sociology": "sociology",
    "psychology": "psychology", "history": "history",
}

TOPICS = {
    "quantum mechanics": {
        "title": "Quantum Mechanics",
        "hook": "Tiny particles do not always behave like everyday objects, so we need a special rulebook.",
        "definition": "Quantum mechanics is the branch of physics that explains how very small things such as electrons, photons, and atoms behave.",
        "simple": "Think of a quantum particle like a tiny object that can be described by possibilities before we measure it.",
        "facts": [
            "Quantum mechanics studies matter and energy at very small scales.",
            "Particles can show both particle-like and wave-like behavior.",
            "Probability is used because outcomes are not always fixed before measurement."
        ],
        "concepts": {
            "superposition": {
                "definition": "Superposition means a quantum system can be described as a combination of possible states before measurement.",
                "kid": "It is like a spinning coin before it lands. We cannot call it only heads or only tails yet.",
                "example": "An electron can be described as having different possible states until we measure it.",
                "mistake": "It does not mean big everyday objects literally become many magical copies.",
                "exam": "Mention possible states, measurement, and probability."
            },
            "uncertainty principle": {
                "definition": "The uncertainty principle states that some pairs of properties cannot both be known perfectly at the same time.",
                "kid": "If you know one thing very clearly, another related thing becomes less clear at the same time.",
                "example": "Knowing a tiny particle's exact position makes its speed less certain, and the other way around.",
                "mistake": "It is not only because our instruments are bad. It is a basic limit in nature.",
                "exam": "Explain that uncertainty is a fundamental quantum limit, not a measurement problem."
            },
            "wave particle duality": {
                "definition": "Wave-particle duality means tiny things can show both wave-like and particle-like behavior depending on how we observe them.",
                "kid": "Sometimes it acts like a small ball, and sometimes it spreads like a wave on water.",
                "example": "Light behaves like waves in interference experiments and like particles in the photoelectric effect.",
                "mistake": "It is not switching randomly. The behavior depends on how we set up the observation.",
                "exam": "Use light or electron examples and mention both behaviors clearly."
            },
            "quantum entanglement": {
                "definition": "Quantum entanglement is when two particles become linked so that measuring one instantly affects the other, no matter how far apart they are.",
                "kid": "Imagine two magic dice that always show matching numbers when rolled, even if they are in different cities.",
                "example": "Two entangled photons will show correlated polarization when measured, even across great distances.",
                "mistake": "Entanglement does not allow faster-than-light communication.",
                "exam": "Mention correlation, measurement, and that it does not break the speed of light rule."
            }
        },
        "applications": {
            "quantum computing": "Uses quantum states to process information much faster for certain problems.",
            "semiconductors": "Modern electronics like phones and computers depend on quantum behavior of electrons.",
            "lasers": "Laser technology depends on quantum transitions between energy levels.",
            "MRI machines": "Magnetic resonance imaging uses quantum spin properties of hydrogen atoms."
        },
        "misconceptions": [
            "Quantum mechanics is not just normal physics applied to smaller objects.",
            "Superposition does not mean everything is magically everywhere at once in daily life.",
            "Uncertainty is not only a measurement error. It is a basic limit of nature."
        ],
        "class_questions": [
            "Why do quantum systems need probability instead of exact values?",
            "What exactly changes when a quantum measurement happens?",
            "How is superposition used in quantum computing?",
            "Why does light behave like both a wave and a particle?",
            "Can the uncertainty principle ever be overcome with better instruments?"
        ]
    },
    "machine learning": {
        "title": "Machine Learning",
        "hook": "Instead of writing every rule by hand, we let computers learn patterns from examples.",
        "definition": "Machine learning is a field of AI where computers learn patterns from data and use them to make predictions or decisions without being explicitly programmed.",
        "simple": "It is like teaching a child by showing many examples instead of only giving written rules. The child learns the pattern and applies it to new situations.",
        "facts": [
            "Machine learning uses data to train models that can make predictions.",
            "A model learns relationships between input features and expected outputs.",
            "Good testing on unseen data is needed to check if the model actually works."
        ],
        "concepts": {
            "model": {
                "definition": "A model is the learned pattern or mathematical function created from training data that can make predictions on new inputs.",
                "kid": "It is the computer's learned recipe for making a guess based on what it has seen before.",
                "example": "A house price model learns that bigger size and better location usually mean higher price.",
                "mistake": "A model is not automatically intelligent or always correct. It depends on data quality.",
                "exam": "Mention training, pattern learning, prediction, and evaluation."
            },
            "training data": {
                "definition": "Training data is the set of labeled examples used to teach a model the patterns it needs to learn.",
                "kid": "It is the practice book for the computer. The more good examples, the better the learning.",
                "example": "Thousands of images labeled as cat or dog can train an image classifier.",
                "mistake": "More data is not always better if the data is noisy, biased, or incorrectly labeled.",
                "exam": "Explain features, labels, and the relationship the model is learning."
            },
            "overfitting": {
                "definition": "Overfitting happens when a model memorizes training data too closely and performs poorly on new unseen data.",
                "kid": "It is like memorizing exact answers to one test but failing when questions are worded differently.",
                "example": "A model gets 99 percent accuracy on training data but only 60 percent on test data.",
                "mistake": "High training accuracy alone does not prove a good model. Test performance matters more.",
                "exam": "Mention generalization, training vs test performance, and overfitting prevention."
            },
            "supervised learning": {
                "definition": "Supervised learning trains a model on labeled data where both inputs and correct outputs are provided.",
                "kid": "It is like a teacher giving you practice problems with answer keys.",
                "example": "Email spam detection is trained on emails labeled as spam or not spam.",
                "mistake": "Supervised learning requires labeled data, which can be expensive or time-consuming to collect.",
                "exam": "Mention labeled data, input-output pairs, and classification or regression tasks."
            }
        },
        "applications": {
            "medical prediction": "Models can help predict disease risk from patient data.",
            "recommendation systems": "Apps recommend videos, songs, or products based on past behavior.",
            "fraud detection": "Banks detect unusual transactions by learning normal spending patterns.",
            "image recognition": "Self-driving cars and face recognition systems use trained vision models."
        },
        "misconceptions": [
            "Machine learning is not magic. It depends entirely on data quality and quantity.",
            "High training accuracy does not guarantee real-world performance.",
            "A model can be biased and unfair if the training data is biased."
        ],
        "class_questions": [
            "What is the difference between training data and test data?",
            "Why can overfitting be dangerous in real applications?",
            "How do the features chosen affect model performance?",
            "Why do we need evaluation metrics beyond accuracy?",
            "How can bias enter a machine learning system and cause harm?"
        ]
    },
    "python programming": {
        "title": "Python Programming",
        "hook": "Python helps us write instructions for computers in a clear and readable way without complex symbols.",
        "definition": "Python is a high-level interpreted programming language used for web apps, data analysis, AI, automation, and education due to its clean and readable syntax.",
        "simple": "Python is like writing a clear recipe that a computer can follow step by step. The instructions are close to plain English.",
        "facts": [
            "Python uses indentation instead of curly braces to define code blocks.",
            "Variables in Python do not need a declared type because Python figures it out automatically.",
            "Python has thousands of libraries that extend what it can do."
        ],
        "concepts": {
            "variable": {
                "definition": "A variable is a named location in memory that stores a value which can be used and changed throughout the program.",
                "kid": "It is like a labeled box where we keep something. We can look inside or replace what is in it.",
                "example": "age = 20 stores the number 20 with the name age. Later we can use age in calculations.",
                "mistake": "The variable name is not the same as the value. Changing the name does not change the value.",
                "exam": "Mention name, assigned value, memory, and that values can change."
            },
            "function": {
                "definition": "A function is a reusable named block of code that performs a specific task and can accept inputs and return outputs.",
                "kid": "It is like a small machine: you put something in, it does a job, and gives something back.",
                "example": "A function called calculate_average takes a list of marks, adds them, divides by count, and returns the result.",
                "mistake": "Defining a function does not run it. You must call the function by name to execute it.",
                "exam": "Mention input parameters, the process inside, return value, and reusability."
            },
            "loop": {
                "definition": "A loop is a control structure that repeats a block of code a certain number of times or while a condition is true.",
                "kid": "It tells the computer to do the same action again and again until a condition says to stop.",
                "example": "A for loop can go through every name in a student list and print each one.",
                "mistake": "A loop without a correct stopping condition can run forever and freeze the program.",
                "exam": "Mention repetition, the condition that controls it, and for vs while loops."
            },
            "class": {
                "definition": "A class is a blueprint that defines the properties and behaviors shared by a group of similar objects.",
                "kid": "It is like a cookie cutter. The class is the shape, and each object made from it is one cookie.",
                "example": "A Student class can have name and grade as properties and a method to calculate average.",
                "mistake": "A class is a template, not an object. You must create an instance from the class to use it.",
                "exam": "Mention blueprint, instance, attributes, and methods."
            }
        },
        "applications": {
            "artificial intelligence": "Python is the most widely used language in machine learning and AI research.",
            "automation": "Python can automate repetitive computer tasks like file renaming or email sending.",
            "data analysis": "Python with pandas and matplotlib can clean, analyze, and visualize data.",
            "web development": "Python frameworks like Django and Flask power many websites and APIs."
        },
        "misconceptions": [
            "Python being easy to read does not mean logic is automatically correct.",
            "If code runs once without error, it may still produce wrong results for other inputs.",
            "Copying code without understanding it does not build real programming skill."
        ],
        "class_questions": [
            "Why are functions considered one of the most important ideas in programming?",
            "How does a loop reduce repeated work and make code shorter?",
            "What happens in memory when a variable value is reassigned?",
            "Why is Python particularly popular in AI and data science?",
            "How can we design code to avoid errors before running it?"
        ]
    },
    "data structures": {
        "title": "Data Structures",
        "hook": "Programs become faster and cleaner when data is stored and organized in the right way for the task.",
        "definition": "Data structures are ways of organizing, storing, and managing data in a computer so that operations like searching, inserting, and deleting can be done efficiently.",
        "simple": "It is like choosing the right container for different things: a shelf for books, a queue for waiting people, a tree for a company hierarchy.",
        "facts": [
            "Lists and arrays store items in a sequence with an index.",
            "Stacks follow last-in first-out order, like a pile of plates.",
            "Queues follow first-in first-out order, like a line at a ticket counter."
        ],
        "concepts": {
            "stack": {
                "definition": "A stack is a linear data structure where the last item added is always the first one to be removed.",
                "kid": "It is like a pile of plates. You always add to the top and remove from the top.",
                "example": "The undo function in a text editor uses a stack. The most recent action is undone first.",
                "mistake": "A stack is not the same as a queue. Their order of removal is opposite.",
                "exam": "Mention LIFO which means last in first out, push to add, and pop to remove."
            },
            "queue": {
                "definition": "A queue is a linear data structure where the first item added is always the first one to be removed.",
                "kid": "It is like waiting in line at a shop. The first person in line gets served first.",
                "example": "A printer queue handles jobs in the order they were sent. First sent means first printed.",
                "mistake": "Queue order follows arrival time. It is not random and not like a stack.",
                "exam": "Mention FIFO which means first in first out, enqueue to add, dequeue to remove."
            },
            "tree": {
                "definition": "A tree is a hierarchical data structure made of nodes where each node has a parent and zero or more children, except the root which has no parent.",
                "kid": "It is like a family tree. There is one root at the top and branches going down to children and grandchildren.",
                "example": "A computer file system uses a tree. The root drive has folders, and folders contain more folders and files.",
                "mistake": "A tree data structure is not the same as a graph or a chart. It has a strict parent-child hierarchy.",
                "exam": "Mention root, parent, child, leaf nodes, and hierarchy."
            },
            "hash table": {
                "definition": "A hash table stores key-value pairs and uses a hash function to map keys to positions for very fast lookup.",
                "kid": "It is like a phone book where you look up a name and find the number instantly using a smart index.",
                "example": "Python dictionaries use hash tables internally so that looking up a key takes almost the same time regardless of size.",
                "mistake": "Hash tables can have collisions when two keys map to the same position, which needs to be handled.",
                "exam": "Mention key, value, hash function, and fast lookup time."
            }
        },
        "applications": {
            "search engines": "Trees and hash tables help find and index web pages quickly.",
            "operating systems": "Queues and trees are used in process scheduling and file systems.",
            "databases": "Indexes in databases use tree structures like B-trees for fast data retrieval.",
            "navigation": "GPS and maps use graph structures to find shortest paths."
        },
        "misconceptions": [
            "There is no single best data structure for every problem. The right choice depends on the task.",
            "Stack and queue are different. Their removal order is opposite and should not be confused.",
            "A graph data structure is not the same as a chart or plot used in data visualization."
        ],
        "class_questions": [
            "When should we choose a stack over a queue for a given problem?",
            "Why is a hash table faster for lookup than a simple list?",
            "How does a tree organize hierarchical information better than a flat list?",
            "How do data structures affect the speed and memory use of a program?",
            "Why does choosing the wrong data structure make a program slower?"
        ]
    },
    "artificial intelligence": {
        "title": "Artificial Intelligence",
        "hook": "AI gives machines the ability to perform tasks that normally require human intelligence.",
        "definition": "Artificial intelligence is the field of computer science that focuses on building systems capable of performing tasks that require human-like reasoning, learning, and decision-making.",
        "simple": "AI is like teaching a computer to think and solve problems the way a smart person would, by learning from experience and examples.",
        "facts": [
            "AI includes rule-based systems, machine learning, and deep learning.",
            "Modern AI systems learn from large amounts of data rather than following hand-written rules.",
            "AI is used in healthcare, transportation, finance, and many other fields."
        ],
        "concepts": {
            "agent": {
                "definition": "An AI agent is a system that perceives its environment, makes decisions, and takes actions to achieve a goal.",
                "kid": "It is like a robot that looks around, decides what to do, and acts to reach a target.",
                "example": "A self-driving car is an agent. It sees the road, decides when to turn or brake, and drives toward the destination.",
                "mistake": "An AI agent is not always a physical robot. It can be software making decisions in a digital environment.",
                "exam": "Mention perception, decision-making, action, and goal."
            },
            "search algorithm": {
                "definition": "A search algorithm is a method an AI uses to explore possible solutions and find the best path to a goal.",
                "kid": "It is like finding the best route on a map by trying different paths and choosing the shortest one.",
                "example": "A chess AI uses search to explore many possible moves ahead and pick the best one.",
                "mistake": "Searching all possibilities is not always possible. Smart algorithms prune bad paths early.",
                "exam": "Mention state space, exploration, and finding an optimal or acceptable solution."
            },
            "knowledge representation": {
                "definition": "Knowledge representation is the method of storing facts and rules about the world so an AI system can use them to reason.",
                "kid": "It is like writing down everything a smart assistant needs to know so it can answer questions correctly.",
                "example": "An AI medical system stores rules like high fever plus cough may indicate infection.",
                "mistake": "Storing more knowledge is not enough if the AI cannot reason about it correctly.",
                "exam": "Mention facts, rules, inference, and structured knowledge bases."
            }
        },
        "applications": {
            "healthcare": "AI helps detect diseases in medical images and predict patient outcomes.",
            "transportation": "Self-driving cars and traffic optimization systems use AI.",
            "customer service": "Chatbots handle customer questions and complaints automatically.",
            "finance": "AI detects fraud and recommends investment strategies."
        },
        "misconceptions": [
            "AI is not the same as human consciousness. Current AI does not understand meaning the way humans do.",
            "AI systems are not always objective. They reflect the biases in their training data.",
            "Strong AI that can do everything a human can does not exist yet."
        ],
        "class_questions": [
            "What makes a system intelligent according to AI researchers?",
            "How is machine learning different from traditional rule-based AI?",
            "Why is the quality of training data so important in AI?",
            "What are the ethical concerns of using AI in decision-making?",
            "What is the difference between narrow AI and general AI?"
        ]
    },
    "object oriented programming": {
        "title": "Object Oriented Programming",
        "hook": "Instead of writing one long list of instructions, OOP organizes code around real-world objects.",
        "definition": "Object oriented programming is a programming approach that organizes software around objects, which are instances of classes that combine data and behavior.",
        "simple": "OOP is like building with LEGO. Each LEGO piece is an object with a specific shape and function. You combine them to build something bigger.",
        "facts": [
            "OOP uses classes as blueprints for creating objects.",
            "Encapsulation bundles data and methods together inside a class.",
            "Inheritance allows a new class to reuse and extend an existing class."
        ],
        "concepts": {
            "class and object": {
                "definition": "A class is a blueprint that defines attributes and methods. An object is a specific instance created from that blueprint.",
                "kid": "The class is like the design of a car on paper. Each real car built from that design is one object.",
                "example": "A Dog class defines name and breed. Each specific dog like Rex or Bella is one object created from that class.",
                "mistake": "A class is not an object. You must instantiate the class to create a real object you can use.",
                "exam": "Mention class as blueprint, object as instance, and how to create one using the constructor."
            },
            "encapsulation": {
                "definition": "Encapsulation means keeping the internal data of an object private and only allowing access through defined methods.",
                "kid": "It is like a TV remote. You press the button but you do not need to know the circuit inside to use it.",
                "example": "A BankAccount class hides the balance and only allows changes through deposit and withdraw methods.",
                "mistake": "Encapsulation is not just about privacy. It is also about controlling how data is accessed and changed.",
                "exam": "Mention private attributes, public methods, and controlled access."
            },
            "inheritance": {
                "definition": "Inheritance allows a child class to receive and reuse the attributes and methods of a parent class while also adding its own.",
                "kid": "It is like a child who has their parent's traits but also has their own unique personality.",
                "example": "An ElectricCar class inherits from a Car class and adds battery and charge method.",
                "mistake": "Inheritance should model a true is-a relationship. Use it only when the child class truly is a type of the parent.",
                "exam": "Mention parent class, child class, reuse, and extension."
            },
            "polymorphism": {
                "definition": "Polymorphism allows different objects to be treated as the same type and respond to the same method in their own specific way.",
                "kid": "It is like asking different animals to speak. A dog barks, a cat meows, but you used the same speak command.",
                "example": "A draw method called on a Circle object draws a circle, but the same call on a Rectangle object draws a rectangle.",
                "mistake": "Polymorphism does not mean all objects behave identically. Each one responds in its own appropriate way.",
                "exam": "Mention same method name, different behavior, and method overriding."
            }
        },
        "applications": {
            "software engineering": "Large systems use OOP to organize code into manageable independent components.",
            "game development": "Game characters, items, and environments are objects with their own properties and behaviors.",
            "GUI applications": "User interface elements like buttons and windows are designed as objects.",
            "simulation": "Real-world systems like traffic or biology are modeled using interacting objects."
        },
        "misconceptions": [
            "OOP is not always the best approach for every program. Small scripts may not benefit from it.",
            "Inheritance should not be overused. Composition is often a better design choice.",
            "More classes does not always mean better code. Unnecessary classes add complexity."
        ],
        "class_questions": [
            "When should we use inheritance and when should we use composition instead?",
            "How does encapsulation protect data integrity in a program?",
            "What is the difference between method overriding and method overloading?",
            "Why is polymorphism useful when working with collections of different object types?",
            "How does OOP make large software projects easier to maintain and extend?"
        ]
    },
    "neural networks": {
        "title": "Neural Networks",
        "hook": "Neural networks learn to recognize patterns by adjusting thousands of connections, similar to how the brain learns.",
        "definition": "A neural network is a machine learning model made of layers of interconnected nodes that learn to map inputs to outputs by adjusting the strength of connections during training.",
        "simple": "Think of it like a network of simple decision-makers. Each one looks at inputs, does a small calculation, and passes a result forward until a final answer comes out the other end.",
        "facts": [
            "Neural networks are inspired by how biological neurons in the brain connect and communicate.",
            "Training adjusts the weights of connections to minimize prediction error.",
            "Deep neural networks have many hidden layers that learn increasingly abstract features."
        ],
        "concepts": {
            "neuron and weight": {
                "definition": "A neuron is a single computing unit in a network that takes inputs, multiplies each by a weight, sums them, and passes the result through an activation function.",
                "kid": "Each tiny worker in the network looks at a few numbers, decides how important each one is, adds them up, and passes a signal forward.",
                "example": "A neuron for cat detection might learn to weigh pointy ear features highly and round nose features lowly.",
                "mistake": "Artificial neurons are very simple math operations. They are not anything like biological neurons in complexity.",
                "exam": "Mention inputs, weights, sum, activation function, and output."
            },
            "backpropagation": {
                "definition": "Backpropagation is the algorithm that calculates how much each weight contributed to the error and adjusts all weights to reduce future errors.",
                "kid": "It is like checking your homework, seeing which steps went wrong, and going back to fix your thinking for next time.",
                "example": "If a network wrongly classifies a cat as a dog, backpropagation traces the error and adjusts the weights that caused it.",
                "mistake": "Backpropagation does not guarantee finding the perfect weights. It finds a good enough solution.",
                "exam": "Mention error, gradient, weight update, and learning rate."
            },
            "activation function": {
                "definition": "An activation function is a mathematical function applied to a neuron's output to introduce non-linearity, allowing the network to learn complex patterns.",
                "kid": "It is like a decision gate that decides how strongly a signal should pass through based on the input.",
                "example": "The ReLU function outputs zero for negative inputs and keeps positive values unchanged, helping networks learn faster.",
                "mistake": "Without an activation function, no matter how many layers there are, the network can only learn linear relationships.",
                "exam": "Mention non-linearity, ReLU or sigmoid examples, and why it is needed."
            }
        },
        "applications": {
            "image recognition": "Neural networks identify objects, faces, and scenes in photos with high accuracy.",
            "speech recognition": "Voice assistants convert spoken words to text using trained neural networks.",
            "translation": "Language translation services use neural networks to convert between languages.",
            "medical imaging": "Neural networks detect tumors and abnormalities in X-rays and MRI scans."
        },
        "misconceptions": [
            "More layers do not always improve performance. Too many layers can make training unstable.",
            "Neural networks do not understand meaning. They find statistical patterns in data.",
            "A neural network is not a black box that cannot be studied. Methods exist to understand what it learned."
        ],
        "class_questions": [
            "Why do neural networks need non-linear activation functions?",
            "How does increasing the number of layers affect what a network can learn?",
            "What is the role of the learning rate in training a neural network?",
            "Why do very deep networks sometimes fail to train effectively?",
            "How is a convolutional neural network different from a fully connected network?"
        ]
    },
    "natural language processing": {
        "title": "Natural Language Processing",
        "hook": "NLP teaches computers to read, understand, and generate human language, bridging the gap between humans and machines.",
        "definition": "Natural language processing is a branch of AI that focuses on enabling computers to understand, interpret, and generate human language in a useful way.",
        "simple": "NLP is like giving a computer the ability to read a book, understand what it says, and then write a summary or answer questions about it.",
        "facts": [
            "NLP combines linguistics, computer science, and machine learning.",
            "Text must be converted into numbers before a computer can process it.",
            "Modern NLP systems like GPT and BERT are trained on enormous amounts of text."
        ],
        "concepts": {
            "tokenization": {
                "definition": "Tokenization is the process of breaking text into smaller units called tokens, which are usually words or subword pieces.",
                "kid": "It is like cutting a sentence into individual words and giving each word a label so the computer can process them one at a time.",
                "example": "The sentence I love Python becomes three tokens: I, love, Python.",
                "mistake": "Tokenization is not just splitting by spaces. Punctuation, special characters, and compound words need special handling.",
                "exam": "Mention breaking text into units, tokens, and preprocessing."
            },
            "word embeddings": {
                "definition": "Word embeddings are numerical vector representations of words that capture their meaning and relationships to other words.",
                "kid": "Each word gets a list of numbers that places it in a space where similar words are close together.",
                "example": "King minus Man plus Woman gives a result close to Queen in embedding space, showing the model learned relationships.",
                "mistake": "Word embeddings capture statistical patterns, not true understanding of meaning the way humans understand.",
                "exam": "Mention vector, similarity, and that similar words have similar vectors."
            },
            "sentiment analysis": {
                "definition": "Sentiment analysis is the task of classifying text as positive, negative, or neutral based on the emotions or opinions expressed.",
                "kid": "It is like asking the computer to read a review and tell you whether the person liked it or did not.",
                "example": "This movie was absolutely fantastic is classified as positive. The service was terrible and slow is negative.",
                "mistake": "Sentiment is not always obvious. Sarcasm and cultural context can confuse even advanced models.",
                "exam": "Mention classification, positive or negative labels, and real-world uses like product reviews."
            }
        },
        "applications": {
            "chatbots": "Customer service bots understand questions and give relevant answers.",
            "machine translation": "Google Translate uses NLP to convert text between languages.",
            "search engines": "Search engines understand the meaning of queries, not just matching keywords.",
            "text summarization": "News apps automatically summarize long articles into short versions."
        },
        "misconceptions": [
            "Computers do not understand language the way humans do. They find statistical patterns.",
            "A high accuracy score on a benchmark does not mean a model understands meaning.",
            "Translation by NLP can be fluent but still contain errors in meaning or context."
        ],
        "class_questions": [
            "Why must text be converted to numbers before a computer can process it?",
            "How do word embeddings capture the meaning and relationships between words?",
            "Why is sarcasm difficult for sentiment analysis models?",
            "What makes transformer models like BERT better than earlier NLP approaches?",
            "How does named entity recognition work and where is it used?"
        ]
    },
    "statistics": {
        "title": "Statistics",
        "hook": "Statistics helps us make sense of data, find patterns, and make informed decisions from numbers.",
        "definition": "Statistics is the science of collecting, organizing, analyzing, and interpreting numerical data to draw conclusions and make predictions.",
        "simple": "Statistics is like being a data detective. You look at numbers, find patterns, and use them to answer questions about the world.",
        "facts": [
            "Descriptive statistics summarizes data using mean, median, mode, and standard deviation.",
            "Inferential statistics uses samples to make conclusions about larger populations.",
            "Probability is the foundation that connects data to predictions."
        ],
        "concepts": {
            "mean median mode": {
                "definition": "Mean is the arithmetic average. Median is the middle value when sorted. Mode is the most frequently occurring value.",
                "kid": "Mean is what you get if everyone shares equally. Median is the person standing exactly in the middle of a sorted line. Mode is the most popular choice.",
                "example": "In the dataset 3, 5, 5, 7, 10: the mean is 6, the median is 5, and the mode is 5.",
                "mistake": "The mean is sensitive to extreme values called outliers. The median is more reliable when outliers exist.",
                "exam": "Know how to calculate each one and when to use median over mean."
            },
            "standard deviation": {
                "definition": "Standard deviation measures how spread out values are from the mean. A high value means data is widely spread. A low value means data is clustered close to the mean.",
                "kid": "If everyone in a class scored nearly the same marks, standard deviation is low. If scores vary a lot, it is high.",
                "example": "Test scores of 80, 81, 79, 80 have low standard deviation. Scores of 40, 60, 90, 100 have high standard deviation.",
                "mistake": "Standard deviation alone does not tell you if results are good or bad. Context matters.",
                "exam": "Explain it as a measure of spread and mention variance as the squared version."
            },
            "hypothesis testing": {
                "definition": "Hypothesis testing is a method to decide whether data provides enough evidence to reject a default assumption called the null hypothesis.",
                "kid": "It is like a trial. We assume innocence until the evidence is strong enough to prove guilt beyond a reasonable doubt.",
                "example": "A company claims a new drug reduces headaches. A hypothesis test checks whether the data supports that claim statistically.",
                "mistake": "Failing to reject the null hypothesis does not prove it is true. It only means evidence was not strong enough.",
                "exam": "Mention null hypothesis, alternative hypothesis, p-value, and significance level."
            }
        },
        "applications": {
            "medicine": "Clinical trials use statistics to determine whether a new treatment is effective.",
            "business": "Companies analyze sales data to identify trends and make decisions.",
            "science": "Researchers use statistics to validate experimental findings.",
            "sports": "Player and team performance is analyzed statistically to improve strategy."
        },
        "misconceptions": [
            "Correlation between two variables does not prove that one causes the other.",
            "A larger sample size does not guarantee correct conclusions if the sample is biased.",
            "Statistical significance does not always mean practical importance in the real world."
        ],
        "class_questions": [
            "Why is the median more reliable than the mean when data has extreme outliers?",
            "What is the difference between descriptive and inferential statistics?",
            "Why does correlation not imply causation?",
            "What does a p-value actually tell us in hypothesis testing?",
            "How does sample size affect the reliability of statistical conclusions?"
        ]
    },
    "algorithms": {
        "title": "Algorithms",
        "hook": "An algorithm is a precise set of steps that solves any instance of a problem reliably and efficiently.",
        "definition": "An algorithm is a finite, ordered sequence of well-defined instructions that takes an input, processes it, and produces a correct output for a given problem.",
        "simple": "An algorithm is like a detailed recipe. Follow the steps exactly and you always get the expected result, no matter who follows it.",
        "facts": [
            "Algorithms are evaluated by time complexity and space complexity.",
            "Sorting algorithms like quicksort and mergesort organize data in a defined order.",
            "Search algorithms like binary search find items efficiently in sorted data."
        ],
        "concepts": {
            "time complexity": {
                "definition": "Time complexity describes how the number of operations an algorithm performs grows as the input size increases, expressed in Big O notation.",
                "kid": "It is a measure of how much longer an algorithm takes when you give it more work. O(n) means double the input means double the time.",
                "example": "Linear search is O(n) because checking each item takes one step per item. Binary search is O(log n) because it halves the search space each step.",
                "mistake": "Big O notation describes growth rate in the worst case, not the exact number of operations.",
                "exam": "Know O(1), O(n), O(n squared), and O(log n) with examples of each."
            },
            "sorting": {
                "definition": "Sorting algorithms arrange elements in a defined order such as ascending or descending.",
                "kid": "It is like organizing a messy bookshelf alphabetically by title so you can find any book faster.",
                "example": "Bubble sort repeatedly swaps adjacent out-of-order elements. Merge sort divides the list in half and merges sorted halves.",
                "mistake": "No single sorting algorithm is best for every situation. Choice depends on data size and initial order.",
                "exam": "Compare bubble sort O(n squared) with merge sort O(n log n) and explain why the difference matters."
            },
            "recursion": {
                "definition": "Recursion is a technique where a function calls itself with a smaller version of the same problem until a simple base case is reached.",
                "kid": "It is like looking up a word in a dictionary and finding the definition uses another word you must look up too, until you reach a word you already know.",
                "example": "Factorial of 5 is 5 times factorial of 4, which is 4 times factorial of 3, and so on until factorial of 1 which is just 1.",
                "mistake": "Every recursive function must have a base case. Without it the function calls itself forever and crashes.",
                "exam": "Identify base case, recursive case, and how each call reduces the problem size."
            }
        },
        "applications": {
            "search engines": "Ranking algorithms decide which web pages appear at the top of search results.",
            "navigation": "Shortest path algorithms like Dijkstra find the best route on maps.",
            "compression": "Algorithms like Huffman coding reduce file size without losing important data.",
            "encryption": "Cryptographic algorithms protect sensitive data and communications."
        },
        "misconceptions": [
            "A working algorithm is not always an efficient one. Correctness and efficiency are separate qualities.",
            "The fastest algorithm for large input is not always fastest for small input.",
            "Recursion is not always better than iteration. Sometimes a simple loop is clearer and faster."
        ],
        "class_questions": [
            "Why do we use Big O notation instead of measuring actual time in seconds?",
            "When is merge sort preferred over bubble sort in practice?",
            "How does binary search require data to be sorted to work?",
            "What makes a greedy algorithm different from a dynamic programming algorithm?",
            "Why must every recursive function have a base case?"
        ]
    },
    "deep learning": {
        "title": "Deep Learning",
        "hook": "Deep learning gives machines the ability to learn complex patterns from raw data like images, sound, and text without hand-crafted rules.",
        "definition": "Deep learning is a subfield of machine learning that uses neural networks with many layers to automatically learn hierarchical features from large datasets.",
        "simple": "Deep learning is like teaching a baby to recognize faces by showing thousands of photos. The brain builds up from simple edges to complex faces layer by layer.",
        "facts": [
            "Deep learning requires large amounts of labeled data and significant computing power.",
            "Each layer in a deep network learns more abstract features than the one before it.",
            "GPUs accelerate deep learning training because they process many calculations in parallel."
        ],
        "concepts": {
            "layers": {
                "definition": "A deep network is made of an input layer, multiple hidden layers, and an output layer. Each hidden layer transforms the data into more abstract representations.",
                "kid": "The first layer sees raw pixels. The next sees edges. The next sees shapes. The final layer sees whole objects.",
                "example": "In face recognition, early layers detect edges, middle layers detect eyes and nose shapes, and deep layers detect full faces.",
                "mistake": "Adding more layers does not always improve accuracy. Too many layers without enough data causes overfitting.",
                "exam": "Describe the role of each layer type and what kinds of features they learn."
            },
            "convolutional layer": {
                "definition": "A convolutional layer applies learned filters across an image to detect local patterns like edges, textures, and shapes.",
                "kid": "It is like using a magnifying glass to scan an image piece by piece and note down what patterns appear in each piece.",
                "example": "A filter trained on cat images learns to detect pointy ear shapes wherever they appear in the image.",
                "mistake": "A convolutional layer does not look at the whole image at once. It scans small patches systematically.",
                "exam": "Mention filter, feature map, local pattern detection, and parameter sharing."
            },
            "dropout": {
                "definition": "Dropout is a regularization technique where random neurons are temporarily ignored during training to prevent overfitting.",
                "kid": "During practice, some team members sit out randomly so the remaining players learn to work without depending on any one person.",
                "example": "With dropout of 0.5, each neuron has a 50 percent chance of being turned off during each training step.",
                "mistake": "Dropout is only applied during training. During testing all neurons are active to make the best prediction.",
                "exam": "Mention overfitting prevention, random deactivation during training, and that it is not used at test time."
            }
        },
        "applications": {
            "computer vision": "Deep learning powers object detection, face recognition, and medical image analysis.",
            "speech processing": "Voice assistants use deep networks to recognize and generate speech.",
            "autonomous vehicles": "Self-driving cars use deep learning to perceive and navigate their environment.",
            "drug discovery": "Deep learning models predict how molecules will interact with proteins."
        },
        "misconceptions": [
            "Deep learning does not understand images or language. It finds statistical patterns.",
            "A deeper network is not always better. Architecture and data quality matter more.",
            "Deep learning is not the only or always best approach. Classical methods often work better on small datasets."
        ],
        "class_questions": [
            "Why do deeper networks learn more complex features than shallow ones?",
            "What problem does dropout solve during neural network training?",
            "Why do convolutional networks work better for images than fully connected networks?",
            "What role does the amount of training data play in deep learning performance?",
            "How is transfer learning used to apply a pre-trained model to a new task?"
        ]
    },
    "database management systems": {
        "title": "Database Management Systems",
        "hook": "Databases store, organize, and retrieve data efficiently so applications can find exactly what they need in milliseconds.",
        "definition": "A database management system is software that stores, manages, organizes, and retrieves structured data for applications in a controlled, consistent, and secure way.",
        "simple": "A DBMS is like a very organized filing cabinet with a smart assistant. You tell it what you want and it finds the right file instantly.",
        "facts": [
            "Relational databases store data in tables with rows and columns.",
            "SQL is the standard language used to query and manage relational databases.",
            "Indexes speed up data retrieval by creating shortcuts to frequently accessed data."
        ],
        "concepts": {
            "relational model": {
                "definition": "The relational model organizes data into tables where each row is a record and each column is an attribute, and tables are linked by shared key values.",
                "kid": "It is like spreadsheets that are connected. One sheet has student names and IDs, another has grades linked by the same ID.",
                "example": "A Students table and a Grades table are linked by student ID. A query can join them to show each student with their marks.",
                "mistake": "Relational tables are not the same as Excel sheets. They enforce rules about data types and relationships.",
                "exam": "Mention tables, rows, columns, primary key, foreign key, and joins."
            },
            "SQL": {
                "definition": "SQL is the structured query language used to create, read, update, and delete data in relational databases.",
                "kid": "SQL is like giving very precise instructions to a librarian. SELECT means find this, WHERE means only if this condition is true.",
                "example": "SELECT name FROM students WHERE grade > 80 finds all students with grades above 80.",
                "mistake": "SQL is not case sensitive for keywords, but database and table names may be case sensitive depending on the system.",
                "exam": "Know SELECT, FROM, WHERE, JOIN, GROUP BY, and ORDER BY with simple examples."
            },
            "normalization": {
                "definition": "Normalization is the process of organizing a database to reduce data redundancy and improve data integrity by dividing data into well-structured related tables.",
                "kid": "It is like not repeating the same information in multiple places. If an address changes, you only need to update it once.",
                "example": "Instead of storing a city name in every row of a customers table, store a city ID and have a separate cities table.",
                "mistake": "Over-normalization can make queries slow because too many tables must be joined to get the needed data.",
                "exam": "Explain redundancy, the first three normal forms, and why normalization matters for data integrity."
            }
        },
        "applications": {
            "banking": "Banks store account information, transactions, and customer data in databases.",
            "e-commerce": "Online shops manage product catalogs, orders, and customer accounts.",
            "healthcare": "Hospitals store patient records, prescriptions, and test results.",
            "social media": "Platforms store user profiles, posts, and connections."
        },
        "misconceptions": [
            "A database is not the same as a spreadsheet. Databases enforce rules and handle concurrent access.",
            "SQL is not a programming language in the traditional sense. It is a query language for structured data.",
            "NoSQL databases do not replace relational databases. Each type suits different use cases."
        ],
        "class_questions": [
            "Why is normalization important and what problems does it prevent?",
            "What is the difference between a primary key and a foreign key?",
            "When would you choose a NoSQL database over a relational database?",
            "How do indexes improve query performance in a large database?",
            "What does a JOIN operation do and when is it needed?"
        ]
    },
    "operating systems": {
        "title": "Operating Systems",
        "hook": "The operating system is the invisible manager that lets all programs and hardware work together smoothly.",
        "definition": "An operating system is system software that manages hardware resources, provides services for programs, and creates a consistent environment for applications to run.",
        "simple": "An OS is like the manager of a busy office. It assigns desks to workers, controls the printer queue, and makes sure everyone gets a fair turn.",
        "facts": [
            "The OS manages CPU scheduling, memory, storage, and input-output devices.",
            "Processes are programs in execution and the OS controls how they share the CPU.",
            "File systems organize how data is stored and retrieved from storage devices."
        ],
        "concepts": {
            "process management": {
                "definition": "Process management is the OS function that creates, schedules, and terminates processes while ensuring the CPU is shared fairly and efficiently.",
                "kid": "It is like a teacher managing students taking turns to use one computer. Everyone gets time but no one waits forever.",
                "example": "When you open a browser and a music player at the same time, the OS rapidly switches CPU time between both processes.",
                "mistake": "Processes do not actually run simultaneously on a single CPU. The OS switches between them so fast it appears simultaneous.",
                "exam": "Mention process states such as running, ready, and waiting, and CPU scheduling policies."
            },
            "memory management": {
                "definition": "Memory management is the OS function that allocates RAM to processes, tracks which memory is in use, and reclaims it when processes finish.",
                "kid": "It is like assigning seats in a classroom. When a student leaves, the seat becomes available for the next student.",
                "example": "When you open a large application, the OS allocates a block of RAM to it and frees that RAM when you close the app.",
                "mistake": "A program cannot directly access RAM. It must request memory from the OS and use the address given.",
                "exam": "Mention allocation, deallocation, virtual memory, and paging."
            },
            "deadlock": {
                "definition": "A deadlock occurs when two or more processes each hold a resource the other needs and neither can proceed, causing both to wait forever.",
                "kid": "It is like two people in a narrow hallway both waiting for the other to move first. Nobody moves and nothing gets done.",
                "example": "Process A holds a printer and needs a scanner. Process B holds a scanner and needs a printer. Both wait forever.",
                "mistake": "Deadlock does not always crash the system immediately. It may cause programs to freeze silently.",
                "exam": "State the four conditions for deadlock: mutual exclusion, hold and wait, no preemption, and circular wait."
            }
        },
        "applications": {
            "mobile devices": "Android and iOS are operating systems managing apps, calls, and sensors on phones.",
            "servers": "Linux manages web servers, databases, and cloud infrastructure.",
            "embedded systems": "Small OS versions run in cars, TVs, and industrial machines.",
            "desktops": "Windows and macOS provide user interfaces and resource management for personal computers."
        },
        "misconceptions": [
            "The OS does not run programs. It creates an environment where programs can run using hardware.",
            "More RAM does not always solve performance problems if the bottleneck is the CPU or storage.",
            "Multitasking on a single CPU core is an illusion created by very fast process switching."
        ],
        "class_questions": [
            "How does the OS decide which process gets the CPU next?",
            "What is virtual memory and why is it useful when RAM is full?",
            "What are the four necessary conditions for a deadlock to occur?",
            "How does an OS protect one process from accessing another process's memory?",
            "What is the difference between a process and a thread?"
        ]
    },
    "economics": {
        "title": "Economics",
        "hook": "Economics explains how people, businesses, and governments make decisions when resources are limited.",
        "definition": "Economics is the social science that studies how individuals, organizations, and governments allocate scarce resources to satisfy unlimited wants and needs.",
        "simple": "Economics is about making choices. Because we cannot have everything, we must decide what to prioritize and what to give up.",
        "facts": [
            "Microeconomics focuses on individual and business decisions.",
            "Macroeconomics studies the overall economy including GDP, inflation, and unemployment.",
            "Supply and demand are the core forces that determine prices in markets."
        ],
        "concepts": {
            "supply and demand": {
                "definition": "Supply is the amount producers are willing to offer at various prices. Demand is the amount consumers want to buy. Price adjusts until they balance at equilibrium.",
                "kid": "When everyone wants the same toy before a holiday, the price goes up because demand is high and supply is limited.",
                "example": "When a new phone model is released in limited quantities, high demand and low supply push the price up.",
                "mistake": "Demand does not only go down as price rises. There are exceptions called Giffen goods and luxury goods.",
                "exam": "Draw or describe the supply and demand curves and explain how equilibrium price is reached."
            },
            "opportunity cost": {
                "definition": "Opportunity cost is the value of the next best alternative you give up when you choose one option over another.",
                "kid": "If you spend Saturday studying instead of going to the movies, the opportunity cost is the enjoyment of the movie you missed.",
                "example": "A student who goes to university gives up four years of full-time work salary as the opportunity cost.",
                "mistake": "Opportunity cost is not the same as a financial cost. It includes any valuable alternative given up.",
                "exam": "Show you understand that every choice has a hidden cost of what was not chosen."
            },
            "GDP": {
                "definition": "Gross domestic product is the total monetary value of all goods and services produced within a country in a given period.",
                "kid": "GDP is like adding up the price tag on everything a country makes and sells in one year.",
                "example": "A country with high GDP produces a lot of goods and services, suggesting a strong and productive economy.",
                "mistake": "High GDP does not mean everyone is wealthy. It does not measure income distribution or quality of life.",
                "exam": "Know what GDP measures, how it relates to economic growth, and its limitations."
            }
        },
        "applications": {
            "government policy": "Governments use economic analysis to set tax rates, spending, and interest rates.",
            "business strategy": "Companies use supply and demand analysis to set prices and plan production.",
            "international trade": "Trade agreements are shaped by economic theories about comparative advantage.",
            "personal finance": "Understanding opportunity cost helps individuals make better financial decisions."
        },
        "misconceptions": [
            "Economics is not only about money. It applies to any situation involving scarce resources and choice.",
            "A trade deficit does not automatically mean an economy is weak or failing.",
            "Free markets do not always produce the best outcomes for society without any regulation."
        ],
        "class_questions": [
            "Why does scarcity force every individual and society to make trade-offs?",
            "How does the price mechanism signal information to producers and consumers?",
            "What is the difference between macroeconomics and microeconomics?",
            "Why do economists use models that make simplifying assumptions?",
            "What is inflation and how does it affect purchasing power over time?"
        ]
    },
    "psychology": {
        "title": "Psychology",
        "hook": "Psychology explores why we think, feel, and behave the way we do by studying the mind and behavior scientifically.",
        "definition": "Psychology is the scientific study of the mind, behavior, and mental processes including perception, memory, emotion, personality, and motivation.",
        "simple": "Psychology is like being a detective of the human mind. It uses careful observation and experiments to explain why people act the way they do.",
        "facts": [
            "Psychology uses scientific methods including experiments, surveys, and observations.",
            "The brain and nervous system are central to understanding behavior.",
            "Cognitive psychology studies thinking, memory, and problem solving."
        ],
        "concepts": {
            "classical conditioning": {
                "definition": "Classical conditioning is a learning process where a neutral stimulus becomes associated with a natural stimulus to produce the same response.",
                "kid": "It is like how dogs learn to salivate when they hear a bell if the bell was rung every time food was given.",
                "example": "Pavlov rang a bell before feeding dogs. Eventually the dogs salivated at the sound of the bell alone, before any food appeared.",
                "mistake": "Classical conditioning does not require conscious thought. It works even when the subject is unaware of the association.",
                "exam": "Identify the unconditioned stimulus, unconditioned response, conditioned stimulus, and conditioned response."
            },
            "cognitive dissonance": {
                "definition": "Cognitive dissonance is the mental discomfort experienced when a person holds two contradictory beliefs or when their actions contradict their beliefs.",
                "kid": "It is the uncomfortable feeling you get when you say you are on a diet but then eat a whole cake.",
                "example": "A smoker who knows smoking causes cancer experiences dissonance between the behavior and the knowledge.",
                "mistake": "People resolve dissonance by changing beliefs or behavior, not always by choosing the rational option.",
                "exam": "Define the conflict between beliefs or beliefs and behavior and explain how it is typically resolved."
            },
            "memory": {
                "definition": "Memory is the mental process of encoding, storing, and retrieving information from past experiences.",
                "kid": "Memory is like saving a file on a computer, storing it, and then opening it later when you need it.",
                "example": "Studying with spaced repetition improves long-term memory by reviewing information at increasing intervals.",
                "mistake": "Memory is not like a recording device. It is reconstructive and can be altered or distorted by later experiences.",
                "exam": "Describe encoding, storage, retrieval, and the three types of memory: sensory, short-term, and long-term."
            }
        },
        "applications": {
            "therapy": "Psychologists use behavior and cognitive techniques to treat mental health conditions.",
            "education": "Understanding how memory and motivation work improves teaching methods.",
            "advertising": "Marketers use psychological principles to influence purchasing decisions.",
            "workplace": "Organizational psychology improves team performance and employee wellbeing."
        },
        "misconceptions": [
            "Psychology is not just common sense. Many intuitive beliefs about behavior are wrong.",
            "Mental health conditions are not a sign of weakness. They have biological and environmental causes.",
            "Sigmund Freud's theories are not the foundation of modern psychology. The field has evolved significantly."
        ],
        "class_questions": [
            "What distinguishes psychology from philosophy in how it studies the mind?",
            "How does classical conditioning differ from operant conditioning?",
            "Why is memory considered reconstructive rather than reproductive?",
            "How do biological factors interact with environment to shape personality?",
            "What ethical guidelines must psychologists follow in research?"
        ]
    }
}


def canonical_key(topic: str) -> str:
    key = " ".join(str(topic).strip().lower().split())
    return ALIASES.get(key, key)


def validate_topics():
    errors = []
    required = ["title", "hook", "definition", "simple", "concepts",
                 "applications", "misconceptions", "class_questions"]
    for key, topic in TOPICS.items():
        for field in required:
            if field not in topic or not topic[field]:
                errors.append(f"{key}: missing {field}")
        for cname, concept in topic.get("concepts", {}).items():
            for field in ["definition", "kid", "example", "mistake", "exam"]:
                if field not in concept or not concept[field]:
                    errors.append(f"{key}.{cname}: missing {field}")
    return errors
