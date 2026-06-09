TOPICS = {
    "quantum mechanics": {
        "title": "Quantum Mechanics",
        "hook": "Tiny particles do not follow the rules we see in everyday life.",
        "definition": "Quantum mechanics explains how matter and energy behave at atomic and subatomic scales.",
        "simple": "Imagine an electron is not a tiny ball sitting in one fixed place. It behaves more like a cloud of possibilities until we measure it.",
        "concepts": ["particle", "wave", "superposition", "uncertainty", "measurement", "quantum state"],
        "misconceptions": [
            "Quantum mechanics is not magic; it is a mathematical theory.",
            "Superposition does not mean everyday objects literally do everything at once.",
            "Uncertainty is not only bad measurement; it is built into quantum systems."
        ],
        "applications": ["semiconductors", "lasers", "MRI", "quantum computing", "chemical bonding"],
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
        "concepts": ["data", "features", "model", "training", "prediction", "evaluation"],
        "misconceptions": [
            "Machine learning is not the same as human learning.",
            "More data does not always mean better results.",
            "A model can perform well in training but fail on new data."
        ],
        "applications": ["recommendation systems", "medical diagnosis", "fraud detection", "translation", "image recognition"],
        "facts": [
            "Recommendation systems use machine learning to predict what users may like.",
            "Evaluation is needed because a model can memorize instead of generalize.",
            "Features are useful pieces of information given to a model."
        ]
    },
    "data structures": {
        "title": "Data Structures",
        "hook": "The way data is organized can make a program fast, clean, and scalable.",
        "definition": "Data structures are ways to organize and store data so programs can use it efficiently.",
        "simple": "It is like choosing the right box for toys. Some boxes help you find things fast, some help you stack things, and some help you connect things.",
        "concepts": ["array", "stack", "queue", "tree", "graph", "hash table"],
        "misconceptions": [
            "Data structures are not only theory; they affect real program speed.",
            "One data structure is not best for every problem.",
            "Efficiency depends on how data is accessed and changed."
        ],
        "applications": ["databases", "maps", "search engines", "compilers", "social networks"],
        "facts": [
            "Hash tables can make lookup very fast.",
            "Graphs are useful for networks, maps, and relationships.",
            "Stacks are used in undo systems and function calls."
        ]
    },
    "artificial intelligence": {
        "title": "Artificial Intelligence",
        "hook": "AI helps machines perform tasks that normally require human intelligence.",
        "definition": "Artificial intelligence is the field of building systems that can learn, reason, understand language, perceive, or make decisions.",
        "simple": "AI is like making a computer helpful in a smart task, such as answering questions, recognizing images, or recommending videos.",
        "concepts": ["learning", "reasoning", "perception", "language", "decision-making", "automation"],
        "misconceptions": [
            "AI is not always conscious or human-like.",
            "AI does not automatically understand truth.",
            "AI quality depends on data, design, and evaluation."
        ],
        "applications": ["chatbots", "robotics", "healthcare", "search engines", "education"],
        "facts": [
            "AI systems often depend on data and models.",
            "Chatbots are one visible example of AI in daily life.",
            "AI can support education through feedback and personalization."
        ]
    },
    "python programming": {
        "title": "Python Programming",
        "hook": "Python helps students build real programs with simple, readable syntax.",
        "definition": "Python programming means writing instructions in the Python language to solve problems or build applications.",
        "simple": "Python is like giving clear step-by-step instructions to a computer in a language that is easier for humans to read.",
        "concepts": ["variables", "data types", "conditionals", "loops", "functions", "modules"],
        "misconceptions": [
            "Python is easy to start, but good programming still needs logic and practice.",
            "Copying code is not the same as understanding it.",
            "Errors are not failure; they are part of debugging."
        ],
        "applications": ["automation", "data analysis", "web apps", "machine learning", "scripting"],
        "facts": [
            "Python is widely used in AI, data science, automation, and education.",
            "Functions help organize code into reusable blocks.",
            "Debugging is a normal part of programming."
        ]
    },
    "object oriented programming": {
        "title": "Object Oriented Programming",
        "hook": "OOP helps programmers organize code around objects, behavior, and relationships.",
        "definition": "Object oriented programming is a programming style that uses classes and objects to structure software.",
        "simple": "Think of a class like a blueprint and an object like a real thing made from that blueprint.",
        "concepts": ["class", "object", "inheritance", "encapsulation", "polymorphism", "method"],
        "misconceptions": [
            "OOP is not only about writing classes; it is about organizing responsibilities.",
            "Inheritance is useful but should not be overused.",
            "Objects combine data and behavior."
        ],
        "applications": ["software design", "game development", "GUI apps", "large systems", "simulation"],
        "facts": [
            "A class is a blueprint for creating objects.",
            "Encapsulation helps protect and organize data.",
            "Polymorphism allows different objects to respond in different ways to the same action."
        ]
    },
    "neural networks": {
        "title": "Neural Networks",
        "hook": "Neural networks learn patterns through layers of connected units.",
        "definition": "Neural networks are machine learning models made of connected nodes that learn from data by adjusting weights.",
        "simple": "Imagine many tiny decision makers passing signals to each other until the system learns a pattern.",
        "concepts": ["neuron", "weight", "activation", "layer", "loss", "training"],
        "misconceptions": [
            "Neural networks are not the same as the human brain.",
            "More layers do not always mean better results.",
            "Training requires data, loss, and optimization."
        ],
        "applications": ["image recognition", "speech recognition", "translation", "chatbots", "generative AI"],
        "facts": [
            "Weights are adjusted during training.",
            "Activation functions help networks model non-linear patterns.",
            "Loss measures how wrong the model is."
        ]
    },
    "linear regression": {
        "title": "Linear Regression",
        "hook": "Linear regression predicts a value by fitting a straight-line relationship.",
        "definition": "Linear regression is a statistical and machine learning method used to model the relationship between input variables and a continuous output.",
        "simple": "Imagine drawing the best straight line through points so you can guess a future value.",
        "concepts": ["dependent variable", "independent variable", "slope", "intercept", "error", "prediction"],
        "misconceptions": [
            "Linear regression does not prove causation by itself.",
            "A straight line is not suitable for every pattern.",
            "Outliers can strongly affect the model."
        ],
        "applications": ["price prediction", "trend analysis", "risk estimation", "forecasting", "research analysis"],
        "facts": [
            "The model tries to reduce prediction error.",
            "Slope shows how the output changes when an input changes.",
            "Residuals show the difference between actual and predicted values."
        ]
    },
    "database systems": {
        "title": "Database Systems",
        "hook": "Databases organize information so it can be stored, searched, updated, and protected.",
        "definition": "A database system is software and structure used to store, manage, and retrieve organized data.",
        "simple": "A database is like a smart digital cabinet where information can be found quickly.",
        "concepts": ["table", "record", "query", "primary key", "relationship", "SQL"],
        "misconceptions": [
            "A database is not just a spreadsheet.",
            "Good database design prevents confusion and duplication.",
            "Queries must be written carefully to get correct results."
        ],
        "applications": ["banking", "student records", "e-commerce", "hospital systems", "inventory"],
        "facts": [
            "SQL is used to query relational databases.",
            "Primary keys uniquely identify records.",
            "Relationships connect data across tables."
        ]
    },
    "climate change": {
        "title": "Climate Change",
        "hook": "Climate change affects weather patterns, ecosystems, economies, and human life.",
        "definition": "Climate change means long-term changes in temperature, rainfall, extreme weather, and global climate systems.",
        "simple": "The Earth is like a home with a blanket. Some gases make the blanket thicker, so the Earth gets warmer over time.",
        "concepts": ["greenhouse gases", "global warming", "sea level rise", "fossil fuels", "extreme weather", "sustainability"],
        "misconceptions": [
            "Weather and climate are not the same.",
            "A cold day does not disprove climate change.",
            "Climate change affects health, food, water, and ecosystems."
        ],
        "applications": ["disaster planning", "coastal protection", "energy policy", "agriculture", "water management"],
        "facts": [
            "Greenhouse gases trap heat in the atmosphere.",
            "Sea level rise can threaten coastal communities.",
            "Climate adaptation helps societies reduce damage."
        ]
    }
}
