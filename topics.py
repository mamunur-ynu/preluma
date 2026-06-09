TOPICS = {
    "quantum mechanics": {
        "title": "Quantum Mechanics",
        "hook": "Tiny particles do not follow the rules we see in everyday life.",
        "definition": "Quantum mechanics explains how matter and energy behave at atomic and subatomic scales.",
        "simple": "Very small things such as electrons do not act like tiny balls. They behave more like waves of possibility until we measure them.",
        "concepts": {
            "particle": {
                "definition": "A particle is a tiny unit of matter or energy, such as an electron or photon.",
                "kid": "A particle is like a tiny dot, but in quantum physics it can also behave in strange wave-like ways.",
                "example": "An electron can be treated as a particle when it hits a detector.",
                "mistake": "Students often think particles always behave like small solid balls.",
                "exam": "Define particle and explain how quantum particles can also show wave behavior."
            },
            "wave": {
                "definition": "A wave is a spreading pattern that can carry energy and show interference.",
                "kid": "A wave is like ripples on water spreading out.",
                "example": "Electron diffraction shows that electrons can behave like waves.",
                "mistake": "Students often think only water or sound can be waves.",
                "exam": "Explain wave behavior with an example such as interference or diffraction."
            },
            "superposition": {
                "definition": "Superposition means a quantum system can exist in a combination of possible states before measurement.",
                "kid": "Imagine a coin spinning in the air. Before it lands, it is not simply heads or tails. It has possibilities. Superposition is similar, but for tiny quantum systems.",
                "example": "A quantum bit can be in a combination of 0 and 1 before it is measured.",
                "mistake": "Superposition does not mean everyday objects literally do everything at once.",
                "exam": "Define superposition and give one example such as a qubit being in a combination of 0 and 1."
            },
            "uncertainty": {
                "definition": "Uncertainty means some pairs of properties, such as position and momentum, cannot both be known exactly at the same time.",
                "kid": "It is like trying to know exactly where a fast tiny object is and exactly how fast it is moving at the same time. Quantum physics sets a limit.",
                "example": "The more accurately position is known, the less accurately momentum can be known.",
                "mistake": "Uncertainty is not just because instruments are weak; it is a built-in quantum limit.",
                "exam": "Explain uncertainty as a fundamental limit, not only measurement error."
            },
            "measurement": {
                "definition": "Measurement is the act of observing a quantum system, which can affect the state being measured.",
                "kid": "Looking at a tiny quantum system can change what you find.",
                "example": "Measuring a qubit gives one definite result from possible states.",
                "mistake": "Students often think measurement is passive like looking at a normal object.",
                "exam": "Explain why measurement is important in quantum mechanics."
            },
            "quantum state": {
                "definition": "A quantum state describes all the information we can use to predict measurement results of a quantum system.",
                "kid": "It is like a full information card for a tiny quantum object.",
                "example": "The state of a qubit tells us the probabilities of getting 0 or 1.",
                "mistake": "A quantum state is not always a fixed visible property.",
                "exam": "Define quantum state and connect it with probability."
            }
        },
        "applications": {
            "semiconductors": "Quantum mechanics explains electron behavior in semiconductors, which are used in chips and electronics.",
            "lasers": "Lasers work through quantum transitions between energy levels.",
            "MRI": "MRI uses quantum properties of atomic nuclei in magnetic fields.",
            "quantum computing": "Quantum computing uses superposition and measurement to process information differently.",
            "chemical bonding": "Quantum mechanics explains how atoms bond through electron behavior."
        },
        "facts": [
            "Modern electronics depend on quantum behavior inside semiconductors.",
            "Lasers work because of quantum transitions between energy levels.",
            "Quantum computing uses quantum states to process information differently."
        ]
    },
    "machine learning": {
        "title": "Machine Learning",
        "hook": "A computer can learn patterns from examples instead of being manually programmed for every rule.",
        "definition": "Machine learning is a field of artificial intelligence where computers learn patterns from data.",
        "simple": "It is like teaching a child to recognize cats by showing many cat pictures. The child learns the pattern from examples.",
        "concepts": {
            "data": {
                "definition": "Data is the information used to train or test a machine learning model.",
                "kid": "Data is like the examples you show to a student.",
                "example": "House size and price data can train a price prediction model.",
                "mistake": "More data is not always useful if it is noisy or biased.",
                "exam": "Define data and explain why data quality matters."
            },
            "features": {
                "definition": "Features are the input variables used by a model to make predictions.",
                "kid": "Features are clues given to the computer.",
                "example": "For house price prediction, size, location, and number of rooms can be features.",
                "mistake": "Students often confuse raw data with useful features.",
                "exam": "Give examples of features for a prediction task."
            },
            "model": {
                "definition": "A model is the learned pattern or function used to make predictions.",
                "kid": "A model is like the rule the computer learned from examples.",
                "example": "A trained classifier can identify whether an email is spam.",
                "mistake": "A model is not automatically correct; it must be tested.",
                "exam": "Define model and explain training and testing."
            },
            "training": {
                "definition": "Training is the process of helping a model learn patterns from data.",
                "kid": "Training is practice time for the computer.",
                "example": "A model trains on labeled images to recognize cats and dogs.",
                "mistake": "Training accuracy alone does not prove the model is good.",
                "exam": "Explain the difference between training and evaluation."
            },
            "prediction": {
                "definition": "Prediction is the output a model gives for new input data.",
                "kid": "Prediction is the computer's best guess after learning.",
                "example": "A model predicts whether a patient may have diabetes.",
                "mistake": "Prediction is not always certain; it can be wrong.",
                "exam": "Define prediction with one real-world example."
            },
            "evaluation": {
                "definition": "Evaluation measures how well a model performs, usually on data it did not train on.",
                "kid": "Evaluation is like an exam for the model.",
                "example": "Accuracy, precision, recall, and F1-score can evaluate a classifier.",
                "mistake": "Testing on training data can make performance look better than reality.",
                "exam": "Explain why test data is needed."
            }
        },
        "applications": {
            "recommendation systems": "Machine learning predicts what users may like based on past behavior.",
            "medical diagnosis": "Machine learning can support doctors by identifying patterns in medical data.",
            "fraud detection": "Models can detect unusual financial behavior.",
            "translation": "Machine learning helps translate text between languages.",
            "image recognition": "Models can classify objects in images."
        },
        "facts": [
            "Evaluation is needed because a model can memorize instead of generalize.",
            "Features are useful pieces of information given to a model.",
            "Recommendation systems use machine learning to predict what users may like."
        ]
    },
    "python programming": {
        "title": "Python Programming",
        "hook": "Python helps students build real programs with simple, readable syntax.",
        "definition": "Python programming means writing instructions in Python to solve problems or build applications.",
        "simple": "Python is like giving clear step-by-step instructions to a computer in a language humans can read more easily.",
        "concepts": {
            "variables": {
                "definition": "A variable stores a value that can be used later in a program.",
                "kid": "A variable is like a labeled box where you keep something.",
                "example": "age = 20 stores the value 20 in the variable age.",
                "mistake": "Students sometimes think the variable name is the value itself.",
                "exam": "Define variable and give one code example."
            },
            "data types": {
                "definition": "Data types describe what kind of value is stored, such as integer, float, string, or boolean.",
                "kid": "Data types tell what kind of thing is inside the box.",
                "example": "'Hello' is a string, 10 is an integer, and True is a boolean.",
                "mistake": "Students often mix numbers and strings by accident.",
                "exam": "List common Python data types with examples."
            },
            "conditionals": {
                "definition": "Conditionals let a program choose different actions using if, elif, and else.",
                "kid": "It is like saying: if it rains, take an umbrella; otherwise, go normally.",
                "example": "if score >= 50: print('Pass')",
                "mistake": "Indentation errors are common in conditionals.",
                "exam": "Write an if-else example."
            },
            "loops": {
                "definition": "Loops repeat instructions multiple times.",
                "kid": "A loop is like doing the same task again and again until you are done.",
                "example": "for i in range(5): print(i)",
                "mistake": "Infinite loops happen when a loop never stops.",
                "exam": "Explain for loop and while loop."
            },
            "functions": {
                "definition": "Functions are reusable blocks of code designed to perform a specific task.",
                "kid": "A function is like a small machine. You give input, it does work, and it may return output.",
                "example": "def add(a, b): return a + b",
                "mistake": "Students sometimes forget to call the function after defining it.",
                "exam": "Define a function and explain parameters and return value."
            },
            "modules": {
                "definition": "Modules are files or libraries that contain reusable Python code.",
                "kid": "A module is like a toolbox you can use in your program.",
                "example": "import math allows use of math.sqrt().",
                "mistake": "Students may import a module but not know how to use its functions.",
                "exam": "Explain import with one example."
            }
        },
        "applications": {
            "automation": "Python can automate repetitive computer tasks.",
            "data analysis": "Python can clean, analyze, and visualize data.",
            "web apps": "Python can build web applications using frameworks.",
            "machine learning": "Python is widely used in AI and machine learning projects.",
            "scripting": "Python is useful for small scripts and quick tools."
        },
        "facts": [
            "Python is widely used in AI, data science, automation, and education.",
            "Functions help organize code into reusable blocks.",
            "Debugging is a normal part of programming."
        ]
    },
    "data structures": {
        "title": "Data Structures",
        "hook": "The way data is organized can make a program fast, clean, and scalable.",
        "definition": "Data structures are ways to organize and store data so programs can use it efficiently.",
        "simple": "It is like choosing the right box for toys. Some boxes help you find things fast, some help you stack things, and some help you connect things.",
        "concepts": {
            "array": {
                "definition": "An array stores elements in order, usually in contiguous memory.",
                "kid": "An array is like a row of boxes where each box has a position number.",
                "example": "A list of student marks can be stored in an array.",
                "mistake": "Students often forget indexes usually start from 0.",
                "exam": "Explain array indexing and access time."
            },
            "stack": {
                "definition": "A stack is a data structure that follows last-in, first-out order.",
                "kid": "A stack is like plates. The last plate placed on top is taken first.",
                "example": "Undo operations can use a stack.",
                "mistake": "Students confuse stack with queue order.",
                "exam": "Explain push and pop operations."
            },
            "queue": {
                "definition": "A queue follows first-in, first-out order.",
                "kid": "A queue is like a line at a shop. The first person in line goes first.",
                "example": "Printer tasks can be managed using a queue.",
                "mistake": "Students confuse queue with stack.",
                "exam": "Explain enqueue and dequeue operations."
            },
            "tree": {
                "definition": "A tree stores data in a hierarchical structure with nodes and edges.",
                "kid": "A tree is like a family tree with parents and children.",
                "example": "File systems and decision trees use tree structures.",
                "mistake": "Students sometimes think all graphs are trees.",
                "exam": "Define root, parent, child, and leaf."
            },
            "graph": {
                "definition": "A graph stores relationships using vertices and edges.",
                "kid": "A graph is like cities connected by roads.",
                "example": "Social networks and maps can be modeled as graphs.",
                "mistake": "Students confuse graph charts with graph data structures.",
                "exam": "Explain vertex and edge with an example."
            },
            "hash table": {
                "definition": "A hash table stores key-value pairs and uses a hash function for fast lookup.",
                "kid": "A hash table is like a smart locker system where a key tells you where to find the item.",
                "example": "Dictionaries in Python are based on hash table ideas.",
                "mistake": "Students forget collisions can happen.",
                "exam": "Explain key-value storage and collision."
            }
        },
        "applications": {
            "databases": "Data structures help databases store and retrieve data efficiently.",
            "maps": "Graphs can model roads and routes.",
            "search engines": "Indexes and graphs help search engines find information.",
            "compilers": "Stacks and trees are used in parsing and expression evaluation.",
            "social networks": "Graphs represent users and relationships."
        },
        "facts": [
            "Hash tables can make lookup very fast.",
            "Graphs are useful for networks, maps, and relationships.",
            "Stacks are used in undo systems and function calls."
        ]
    },
}

ALIASES = {
    "oop": "object oriented programming",
    "object-oriented programming": "object oriented programming",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "python": "python programming",
}


def add_topic(key, title, definition, concepts, applications):
    TOPICS[key] = {
        "title": title,
        "hook": f"{title} becomes easier when the student sees the key concepts before class.",
        "definition": definition,
        "simple": f"Think of {title} as a map. First learn the main roads, then the details make more sense.",
        "concepts": {c: {
            "definition": f"{c.title()} is an important concept in {title}.",
            "kid": f"{c.title()} is one piece of the {title} puzzle.",
            "example": f"In {title}, {c} helps explain the topic clearly.",
            "mistake": f"Students often memorize {c} without connecting it to examples.",
            "exam": f"Define {c} and explain its role in {title}."
        } for c in concepts},
        "applications": {a: f"{title} is used in {a}." for a in applications},
        "misconceptions": [
            f"{title} is not only memorization.",
            f"{title} needs examples and applications.",
            f"{title} becomes clearer when students ask questions."
        ],
        "facts": [
            f"{title} is easier when connected with examples.",
            f"{title} has practical applications.",
            f"Understanding core concepts improves performance in {title}."
        ]
    }

add_topic("artificial intelligence", "Artificial Intelligence", "Artificial intelligence is the field of building systems that can learn, reason, understand language, perceive, or make decisions.", ["learning", "reasoning", "perception", "language", "decision-making", "automation"], ["chatbots", "robotics", "healthcare", "search engines", "education"])
add_topic("object oriented programming", "Object Oriented Programming", "Object oriented programming is a programming style that uses classes and objects to structure software.", ["class", "object", "inheritance", "encapsulation", "polymorphism", "method"], ["software design", "game development", "GUI apps", "large systems", "simulation"])
add_topic("neural networks", "Neural Networks", "Neural networks are machine learning models made of connected nodes that learn from data by adjusting weights.", ["neuron", "weight", "activation", "layer", "loss", "training"], ["image recognition", "speech recognition", "translation", "chatbots", "generative AI"])
add_topic("linear regression", "Linear Regression", "Linear regression is a method used to model the relationship between input variables and a continuous output.", ["dependent variable", "independent variable", "slope", "intercept", "error", "prediction"], ["price prediction", "trend analysis", "forecasting", "research analysis", "risk estimation"])
add_topic("database systems", "Database Systems", "A database system stores, manages, and retrieves organized data.", ["table", "record", "query", "primary key", "relationship", "SQL"], ["banking", "student records", "e-commerce", "hospital systems", "inventory"])
add_topic("climate change", "Climate Change", "Climate change means long-term changes in temperature, rainfall, extreme weather, and global climate systems.", ["greenhouse gases", "global warming", "sea level rise", "fossil fuels", "extreme weather", "sustainability"], ["disaster planning", "coastal protection", "energy policy", "agriculture", "water management"])
