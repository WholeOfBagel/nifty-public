
import markdown
import os
import numpy as np
import re
import pandas as pd
import copy
from dataclasses import dataclass, asdict

@dataclass(frozen=True, order=True)
class Note:
    date: None
    task_mode: None
    vd: 0
    d: 0
    n: 0
    p: 0
    vp: 0
    work_time: 0
    elapsed_time: 0
    breaks: 0
    productivity_pulse: 0

default = {
    "vd": 0,
    "d": 0,
    "n": 0,
    "p": 0,
    "vp": 0,
    "work_time": 0,
    "elapsed_time": 0,
    "breaks": 0,
    "productivity_pulse": 0
} 
date = '2023-10-02'
# These paths will obviously have to match whatever file you are trying to analyze
# path = "../../Accountability/Dailies/Development_Mode/{}.md".format(date)
path = "../../Accountability/Dailies/Learning_Mode/{}.md".format(date)
# path = "../../Accountability/Dailies/Development_Mode/{}.md".format(date)     

def task_splitter(rating_dict, f):
    markdown_string = f.read()
    # print(markdown_string)
    tasks_isolated = markdown_string.split("### Tasks\n")[-1].split("####")[0]
    times = []
    by_words = tasks_by_line(tasks_isolated)
    by_words = remove_sub_tasks(by_words)
    for index in range(0, len(by_words) - 1):
        line = by_words[index]
        next_line = by_words[index + 1]
        time_one = line[0]
        time_two = next_line[0]
        t1 = time_to_int(time_one)
        t2 = time_to_int(time_two)
        # print(t1, t2)
        time_spent = t2 - t1
        # print(time_spent)
        second_word = line[1]
        if second_word.lower() == "break":
            rating_dict["breaks"] = rating_dict["breaks"] + 1
        if second_word.lower() != "break":
            rating = line[-1]
            rating_dict[rating] += time_spent
            rating_dict["work_time"] += time_spent
            # print(rating_dict)
        rating_dict["elapsed_time"] += time_spent
    return rating_dict
                
				
def tasks_by_line(task_list):
    by_words = []
    for line in task_list.strip().split("\n"):
        line = line.replace("- [ ]", '').strip()
        line = line.replace("- [x]", '').strip()
        by_words.append(line.split(" "))
    # print(by_words)
    return by_words

def remove_sub_tasks(by_words):
    only_timed = []
    for index in range(0, len(by_words)):
        word = by_words[index][0]
        pattern = re.compile("\\d{1,2}:\\d{2}") 
        if pattern.match(word):
            only_timed.append(by_words[index])
    return only_timed
    
def time_to_int(time_str):
    h1, m1 = time_str.split(":")
    h1, m1 = int(h1) * 60, int(m1)
    return h1 + m1
	

def calc_productivity_pulse(rating_dict, vd, d, n, p, vp, work_time, **kwargs):
    try:
        pp = (((vd) + (d * 1) + (n * 2) + (p * 3) + (vp * 4)) / (work_time * 4)) * 100
    except:
        print("can't do that")
    else:
        rating_dict["productivity_pulse"] = pp
    return rating_dict.copy()
    # print("PP::", round(pp, 2))
    # print("work_time::", rating_dict["work_time"])
    # print("elapsed_time::", rating_dict["elapsed_time"])
    # print("breaks::", rating_dict["breaks"])
    

    
def task_features(date, task_mode, path):
    rating_dict = copy.deepcopy(default)
    with open(path, 'r') as f:
        task_splitter(rating_dict, f)
    calced = calc_productivity_pulse(rating_dict, **rating_dict)
    result = asdict(Note(date, task_mode, **calced))
    return result.copy()

# this has been relegated to a single file reading tool used for debugging - but is functional
# if __name__ == "__main__":
#     print("starting calculation")
#     df = pd.DataFrame.from_dict([rating_dict])
#     print(df.head())
#     df.plot(kind='line')

# def reset_dict():
#     rating_dict = default.copy()
        
    