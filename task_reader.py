
import markdown
import os
import numpy as np
import re
import pandas as pd

rating_dict = {
    "vd": 0,
    "d": 0,
    "n": 0,
    "p": 0,
    "vp": 0,
    "work_time": 0,
    "elapsed_time": 0,
    "breaks": 0
} 
date = '2023-09-15'
# These paths will obviously have to match whatever file you are trying to analyze
# path = "../../Accountability/Dailies/Development_Mode/{}.md".format(date)
# path = "../../Accountability/Dailies/Learning_Mode/{}.md".format(date)
path = "../../Accountability/Dailies/Development_Mode/{}.md".format(date)
def task_splitter():
    with open(path, 'r') as f:
        markdown_string = f.read()
        print(markdown_string)
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
            print(t1, t2)
            time_spent = t2 - t1
            print(time_spent)
            second_word = line[1]
            if second_word.lower() == "break":
                rating_dict["breaks"] = rating_dict["breaks"] + 1
            if second_word.lower() != "break":
                rating = line[-1]
                rating_dict[rating] = rating_dict[rating] + time_spent
                rating_dict["work_time"] += time_spent
                print(rating_dict)
            rating_dict["elapsed_time"] += time_spent
                
				
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
    print("---------------")
    print(only_timed)
    return only_timed
    
def time_to_int(time_str):
	h1, m1 = time_str.split(":")
	h1, m1 = int(h1) * 60, int(m1)
	return h1 + m1
	

def calc_productivity_pulse(vd, d, n, p, vp, work_time, **kwargs):
    pp = (((vd) + (d * 1) + (n * 2) + (p * 3) + (vp * 4)) / (work_time * 4)) * 100
    print("PP::", round(pp, 2))
    print("work_time::", rating_dict["work_time"])
    print("elapsed_time::", rating_dict["elapsed_time"])
    print("breaks::", rating_dict["breaks"])

if __name__ == "__main__":
    task_splitter()
    print("starting calculation")
    calc_productivity_pulse(**rating_dict)