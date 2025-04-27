# Question bank and progress record code
## Question Bank

Naming convention for a question: `[paper_code]-que-[date]-[question_number]-[part]`
Naming convention for a mark scheme: `[paper_code]-rms-[date]-[question_number]-[part]`

To add new questions and mark schemes to the question bank, follow these steps:
1. Create a list of all the files in the directory where the questions and mark schemes are stored. This is done using the Python `os` module.
2. Create a DataFrame with the columns specified in the `columns_template` variable.
3. Using the `add_questions` function, iterate through the list of files and check if the file is a question or a mark scheme. If it is a question, add it to the DataFrame. If it is a mark scheme, add it to the corresponding question in the DataFrame.
4. Using the `add_mark_schemes` function, iterate through the DataFrame and check if the file is a mark scheme. If it is, add it to the corresponding question in the DataFrame.
5. Save the DataFrame to a CSV file.

The dictionaries are used by the functions to map the paper and topic codes to their respective names.

```python
def add_questions(dir: list, qb: pd.DataFrame):
    for i in range(len(dir)):
        current = dir[i]
        if current[8:11] == "que":
            if current[:23] + "-01" not in list(qb.index.values): # New question
                if current[0] == "8": # AS level
                    qb.loc[current[:-4]] = {
                        "additional_question_paths": [],
                        "mark_scheme_paths": [],
                        "examiners_report": None,
                        "model_answer_link": model_answer_links[current[:8] + current[12:16]],
                        "qualification": "AS level",
                        "subject": "Further Maths",
                        "exam_board": ["Edexcel"],
                        "paper": as_papers[current[5:7]],
                        "year": current[12:16],
                        "topic": None,
                        "marks_available": None,
                    }
                else: # A level
                    qb.loc[current[:-4]] = {
                        "additional_question_paths": [],
                        "mark_scheme_paths": [],
                        "examiners_report": None,
                        "model_answer_link": model_answer_links[current[:8] + current[12:16]],
                        "qualification": "A level",
                        "subject": "Further Maths",
                        "exam_board": ["Edexcel"],
                        "paper": a_papers[current[5:7]],
                        "year": current[12:16],
                        "topic": None,
                        "marks_available": None,
                    }
            else: qb.at[current[:23] + "-01", "additional_question_paths"].append(current)

```

```python
def add_mark_schemes(dir: list, qb: pd.DataFrame):
    for i in range(len(qb)):
        curr_q_path = qb.index.values[i]
        curr_ms_path = curr_q_path[:8] + "rms" + curr_q_path[11:16] + curr_q_path[21:23]
        for j in range(len(dir)):
            if dir[j][:16] + dir[j][21:23] == curr_ms_path:
                qb.at[curr_q_path, "mark_scheme_paths"].append(dir[j])
```

```python

as_core_topics = ["Proof",
             "Complex numbers",
             "Matrices",
             "Further algebra and functions",
             "Further calculus",
             "Further vectors"]
as_stats_topics = ["Descrete probability distributions",
                  "Poisson and binomial distributions",
                  "Chi squared tests"]
as_mech_topics = ["Momentum and impulse",
                "Work, energy and power",
                "Elastic collisions in one dimension"]
as_dec_topics = ["Algorithms and graph theory",
               "Algorithms on graphs",
               "Critical path analysis",
               "Linear programming"]

a_core_topics = {"pro": "Proof",
            "com": "Complex numbers",
            "mat": "Matrices",
            "alg": "Further algebra and functions",
            "cal": "Further calculus",
            "vec": "Further vectors",
            "pol": "Polar coordinates",
            "hyp": "Hyperbolic functions",
            "dif": "Differential equations"}
a_stats_topics = {"des": "Discrete probability distributions",
                  "poi": "Poisson and binomial distributions",
                  "geo": "Geometric and negative binomial distributions",
                  "ht": "Hypothesis testing",
                  "clm": "Central limit theorem",
                  "chi": "Chi squared tests",
                  "pgf": "Probability generating functions",
                  "qua": "Quality of tests"}
a_mech_topics = {"mom": "Momentum and impulse",
                "wor": "Work, energy and power",
                "ela": "Elastic strings and springs and elastic energy",
                "col1": "Elastic collisions in one dimension",
                "col2": "Elastic collisions in two dimensions"}
a_dec_topics = {"alga": "Algorithms and graph theory",
               "algo": "Algorithms on graphs",
               "cri": "Critical path analysis",
               "lin": "Linear programming"}

all_topics = {**a_core_topics, **a_stats_topics, **a_mech_topics, **a_dec_topics}
```

```python
as_papers = {"01": "Core Pure 1",
          "21": "Further Pure 1",
          "22": "Further Pure 2",
          "23": "Further Statistics 1",
          "24": "Further Statistics 2",
          "25": "Further Mechanics 1",
          "26": "Further Mechanics 2",
          "27": "Decision 1",
          "28": "Decision 2"}
a_papers = {"01": "Core Pure 1",
          "02": "Core Pure 2",
          "3a": "Further Pure 1",
          "4a": "Further Pure 2",
          "3b": "Further Statistics 1",
          "4b": "Further Statistics 2",
          "3c": "Further Mechanics 1",
          "4c": "Further Mechanics 2",
          "3d": "Decision 1",
          "4d": "Decision 2"}
```

Executed code:
```python
res_list = os.listdir("/Users/ivxnw/PycharmProjects/nea_v1/res")

question_bank = pd.DataFrame(columns=columns_template)
question_bank.set_index("question_path", inplace=True)
add_questions(res_list, question_bank)
add_mark_schemes(res_list, question_bank)

question_bank.to_csv("question_bank.csv")
```

## Progress record

```python
progress_record = pd.DataFrame(data={"topic": [], "qualification": [], "paper": [],
                                     "marks_available": [], "q_available": [], "marks_scored": [], "q_attempted": [],
                                     "n": [], "ef": [], "interval": []})

initial_n = 0
initial_ef = 2.5
initial_interval = 1

topics = question_bank.loc[:, "topic"].unique()
for topic in topics:
    topic_bank = question_bank.loc[question_bank["topic"]  == topic]
    
    progress_record = pd.concat([progress_record,
        pd.DataFrame(data={"topic": [topic],
            "qualification": ["AS level" if "AS level" in topic_bank["qualification"].unique() else "A level"],
            "paper": [topic_bank.loc[:, "paper"].unique()[0]],
            "marks_available": [topic_bank.loc[:, "marks_available"].sum()],
            "q_available": [topic_bank.loc[:, "marks_available"].count()],
            "marks_scored": [0],
            "q_attempted": [0],
            "n": [initial_n],
            "ef": [initial_ef],
            "interval": [initial_interval]
            })],
        ignore_index=True)


progress_record.to_csv("progress_record.csv")
```