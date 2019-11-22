"""
November 14th 2019
            Author T.Mizumoto
"""
# python 3
# ver.X5.05
# csvGraph.py  -  Create a graph from csv file.
# EXAMPLE: python csvGraph.py DATA.csv time
# EXAMPLE: python csvGraph.py -l DATA.csv time

import csv, sys, re, argparse
import matplotlib.pyplot as plt

class Name:
    def __init__(self):
        self.x_axis = ""
        self.y_axis = ""
        self.graph = ""


class Data:
    def __init__(self):
        self.name = ""
        self.data = []

    def add(self, d):
        self.data.append(d)

    # delete unnecessary strings
    def rename(self):
        new_name = re.sub(r": [a-zA-Z0-9\s_-]+", "", self.name)
        return new_name


# the read to file name
p = argparse.ArgumentParser()
p.add_argument("csv_name", type = str, help = ".csv file name")
p.add_argument("change", type = str, help = "name of axis to change")
# option
p.add_argument("-l", "--log", action = "store_true", help = "logarithmic scale")
p.add_argument("-r", "--range", action = "store_true", help = "axis range")
p.add_argument("-t", "--transparent", action = "store_true", help = "make a transparent graph")
args = p.parse_args()

file_name = args.csv_name
change_ax_name = args.change
print("The read file name: " + file_name)
print("The name of axis to change: " + change_ax_name)

# option: logarithmic scale
log_axis = "Off"
def log_scale():
    print("Which axis should be logarithmic?")
    print("x, y or both? :")
    log_axis = input()
    return log_axis

# option: axis range
option_range = "Off"
def axis_range():
    option_range = "On"
    x_min = input("Enter the X-axis minimun: ")
    x_max = input("Enter the X-axis maximun: ")
    y_min = input("Enter the Y-axis minimun: ")
    y_max = input("Enter the Y-axis maximun: ")
    return option_range, x_min, x_max, y_min, y_max

# option: transparency graph
option_trans = False
def trans():
    option_trans = True
    return option_trans


if args.log:
    log_axis = log_scale()
if args.range:
    option_range, x_min, x_max, y_min, y_max = axis_range()
if args.transparent:
    option_trans = trans()


# read the file
file_open = open(file_name)
file_reader = csv.reader(file_open)


# make data objects
for row in file_reader:
    if file_reader.line_num == 1:
        list_num_ori = range(len(row))
        for i in list_num_ori:
            exec("data{} = Data()".format(i))
            exec("data{}.name = row[{}]".format(i, i))

    else:
        list_num = range(len(row))
        if not list_num == list_num_ori:
            raise Exception("ERROR: the number of columns is different.")
        for i in list_num:
            exec("data{}.add(float(row[{}]))".format(i, i))


# find the axis to change
for i in list_num_ori:
    exec("if change_ax_name == data{}.name:\
        change_ax_num = i".format(i))
    exec('raise Exception("ERROR: the change axis is not found.")')

# print data name
for i in list_num_ori:
    if i == 2:
        exec("print('[{}]' + data{}.rename())".format(i+1, i))
    else:
        exec("print('[{}]' + data{}.rename() + ', ', end = '')".format(i+1, i))

# enter the X and Y axis name'
name = Name()
print("Enter the X axis name: ")
name.x_axis = input()
print("Enter the Y axis name: ")
name.y_axis = input()

# enter the graph name
print("Enter the graph name: ")
name.graph = input()


# draw a graph sans-serif
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1.0	
plt.rcParams['ytick.major.width'] = 1.0
plt.rcParams['font.size'] = 15 
plt.rcParams['axes.linewidth'] = 1.0
colorlist = ["blue", "green", "red", "orange", "magenta", "black"]
markerlist = ['o','^','v','<','>',',','*','d']
stylelist = ['-', '--', '-.', ':']
dashes_point = [0.8, 0.5, 2, 0.5]

plt.figure(figsize = (9.898, 7), dpi = 500)
count = 0
for i in list_num_ori:
    if i == change_ax_num:
        pass
    elif count > 3:
        point = [i * count for i in dashes_point]
        exec("plt.plot(data{}.data, data{}.data, color = colorlist[{}]\
            , label = data{}.rename(), dashes = point)"\
            .format(change_ax_num, i, count, i))
        count += 1
    else:
        exec("plt.plot(data{}.data, data{}.data, color = colorlist[{}]\
            , label = data{}.rename(), ls = stylelist[{}])"\
            .format(change_ax_num, i, count, i, count))
        count += 1
plt.xlabel(name.x_axis)
plt.ylabel(name.y_axis)

# option: logarithmic scale
if log_axis == "x" or log_axis == "X":
    plt.xscale("log")
elif log_axis == "y" or log_axis == "Y":
    plt.yscale("log")
elif log_axis == ("both"):
    plt.xscale("log")
    plt.yscale("log")

# option: axis range
if option_range == "On":
    plt.xlim((float(x_min), float(x_max)))
    plt.ylim((float(y_min), float(y_max)))
else:
    exec("plt.xlim((min(data{}.data), max(data{}.data)))".format(change_ax_num, change_ax_num))

plt.legend()
plt.grid(which = "both")

# option: transparency graph
plt.savefig(name.graph + ".png", transparent = option_trans)