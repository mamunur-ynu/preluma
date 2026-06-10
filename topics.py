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
