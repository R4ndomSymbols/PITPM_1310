import tkinter as tk
import math
from turtle import pos

main_color = '#A4A4A4'
border_color_ = '#333333'
background_color = '#FFFFFF'

avalible_funcs = {
    "+": lambda a,b: a+b,
    "-": lambda a,b: a-b,
    "/": lambda a,b: a/b,
    "*": lambda a,b: a*b,
    "^": lambda a,b: math.pow(a,b),
    "root": lambda a,b: math.pow(a, 1/b),
    "log": lambda a,b: math.log(a,b),
    "cos": lambda a: math.cos(a),
    "sin": lambda b: math.sin(b),
    "tan": lambda c: math.tan(c),
    "ctg": lambda d: 1 / math.tan(d)
}

priorities = {
    "+": 1,
    "-": 1,
    "/": 2,
    "*": 2,
    "^": 3,
    "root":3,
    "log": 3,
    "cos": 4,
    "sin": 4,
    "tan": 4,
    "ctg": 4
}

offsets = {
    "+": (-1,1),
    "-": (-1,1),
    "/": (-1,1),
    "*": (-1,1),
    "^": (-1,1),
    "root":(1,2),
    "log": (1,2),
    "cos": (1),
    "sin": (1),
    "tan": (1),
    "ctg": (1)
}

main_window = tk.Tk()
main_window.title("Калькулятор")
main_window.configure(background=background_color)

lbl_result = tk.Label(text="Строка результата", font=("Areal, 20"))
result_string_ent = tk.Entry(font=("Areal, 20"))
lbl_equasion = tk.Label(text="Текущая строка",font=("Areal, 20"))
sv = tk.StringVar()
equasion_string_ent = tk.Entry(main_window, textvariable=sv, font=("Areal, 20"))


def add_button(master, displayed_text, grid_row, grid_colunm , command):
    btn = tk.Button(master)
    btn.configure(background=main_color)
    btn.configure(text=displayed_text, font=("Areal, 20"))
    
    btn.grid(column=grid_colunm, row=grid_row, sticky=tk.NSEW)
    btn['command'] = command

def print_symbol(entry, symbol):
    current_txt = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_txt + symbol)
def erase_one(entry):
    entry.delete(entry.index(tk.END)-1)
def erase_all(entry):
    entry.delete(0,tk.END)

def evaluate_string(*args):
    result_string_ent.delete(0, tk.END)
    if(len(sv.get()) == 0):
        result_string_ent.insert(0, "void_input")
    elif(not validate_brakets(sv.get())):
        result_string_ent.insert(0, "invalid brakets")
    else:
        t = evaluate(sv.get())
        result_string_ent.insert(0, str(t))
    #output.insert(0, "invalid input")
    return True

sv.trace_add('write', evaluate_string)

def validate_brakets(equasion):
    sum = 0
    if(equasion.find(')') == -1 and equasion.find('(') == -1):
        return True
    for i in equasion:
        if(i == ')'):
            sum-=1
        if(i == '('):
            sum+=1
        if(sum < 0):
            return False
    return sum == 0

def evaluate(equasion):
    bracket_priority = 0
    parsed_equasion = list()
    is_minus = False
    op_count = 0
    i = 0
    while(i < len(equasion)):
        if(equasion[i].isdigit() or equasion[i] == '.'):
            t = get_number(equasion, i)
            if(is_minus):
                parsed_equasion.append((-t[0],0))
                is_minus = False
            else:
                parsed_equasion.append((t[0],0))
            i = t[1]
        elif(equasion[i].isalpha()):
            d = get_func(equasion, i)
            parsed_equasion.append((d[0], bracket_priority*6))
            op_count+=1
            i = d[1]
        elif (equasion[i] == '-'):
            if(len(parsed_equasion) == 0):
                is_minus = True
                i+=1
            elif (not (type(parsed_equasion[len(parsed_equasion)-1][0]) is float)):
                is_minus = True
                i+=1
            else:
                parsed_equasion.append((equasion[i], bracket_priority*6))
                op_count +=1
                i+=1
        elif(equasion[i] in ("+","*","/","^")):
            parsed_equasion.append((equasion[i], bracket_priority*6))
            op_count +=1
            i+=1
        elif (equasion[i] == ')'):
            bracket_priority-=1
            i+=1
        elif (equasion[i] == '('):
            bracket_priority+=1
            i+=1
        elif (equasion[i] == ',') :
            if(len(parsed_equasion) > 0):
                if(type(parsed_equasion[len(parsed_equasion)-1][0]) is float):
                    i+=1
                else:
                    print(parsed_equasion)
                    print(str(parsed_equasion[len(parsed_equasion)-1][0]))
                    return "invalid function arguments"
            else:
                return "invalid ',' position"
        else:
            return "unsopported symbol or operation"
    if(op_count>0):
        return evaluate_parsed_equasion(parsed_equasion)[0]
    else:
        if(is_minus or len(parsed_equasion) == 0):
            return 0
        else:
            return parsed_equasion[0][0]
        
    
def evaluate_parsed_equasion(equasion):
    while(len(equasion) != 1):
        j = 0
        max_priority = 0
        current_pos = 0
        operation = ''
        for i in equasion:
            if(priorities.get(i[0]) == None):
                pass
            elif(max_priority < priorities.get(i[0]) + i[1]):
                max_priority = priorities.get(i[0]) + i[1]
                operation = i[0]
                current_pos = j
            j+=1
        
        offset = offsets[operation]
        if(type(offset) is int):
            try:
                pos_list = list()
                pos_list.append(current_pos+offset)
                pos_list.append(current_pos)
                min_pos = min(pos_list)
                num1 = equasion[pos_list[0]][0]
                equasion[min_pos] = (avalible_funcs[operation](num1),0)
                equasion.pop(min_pos+1)
            except:
                return "invalid arguments"
            
        elif(len(offset) == 2):

            try:
                pos_list = list()
                pos_list.append(current_pos+offset[0])
                pos_list.append(current_pos+offset[1])
                pos_list.append(current_pos)

                
                min_pos = min(pos_list)
                num1 = equasion[pos_list[0]][0]
                num2 = equasion[pos_list[1]][0]

                equasion[min_pos] = (avalible_funcs[operation](num1, num2),0)
                equasion.pop(min_pos+2)
                equasion.pop(min_pos+1)
            except:
                return "invalid arguments"
    
    return equasion[0]

def get_number(equasion, position):
    value = ''
    while(True):
        if(not (position < len(equasion))):
            break
        if(equasion[position].isdigit() or equasion[position] == '.'):
            value+=equasion[position] 
            position+=1
        else:
            break
    return (float(value), position)

def get_func(equasion, position):
    value = ''
    while(True):
        if(position >= len(equasion)):
            break
        if(equasion[position].isalpha()):
            value+=equasion[position]
            position+=1
        else:
            break
    #if(avalible_funcs.get(value) != None):
    return (value, position)

for i in range(0, 7):
    main_window.columnconfigure(weight=1, index=i)
for j in range(0, 8):
    main_window.rowconfigure(index = j, weight=1)

lbl_equasion.grid(row=0, columnspan=7, sticky=tk.NSEW)
equasion_string_ent.grid(row=1, columnspan=7, sticky=tk.NSEW)

lbl_result.grid(row = 2, columnspan=7, sticky=tk.NSEW)
result_string_ent.grid(row = 3, columnspan=7, sticky=tk.NSEW)


add_button(main_window, "1", 4, 0, lambda: print_symbol(equasion_string_ent, "1"))
add_button(main_window, "2", 4, 1, lambda: print_symbol(equasion_string_ent, "2"))
add_button(main_window, "3", 4, 2, lambda: print_symbol(equasion_string_ent, "3"))
add_button(main_window, "4", 5, 0, lambda: print_symbol(equasion_string_ent, "4"))
add_button(main_window, "5", 5, 1, lambda: print_symbol(equasion_string_ent, "5"))
add_button(main_window, "6", 5, 2, lambda: print_symbol(equasion_string_ent, "6"))
add_button(main_window, "7", 6, 0, lambda: print_symbol(equasion_string_ent, "7"))
add_button(main_window, "8", 6, 1, lambda: print_symbol(equasion_string_ent, "8"))
add_button(main_window, "9", 6, 2, lambda: print_symbol(equasion_string_ent, "9"))
add_button(main_window, "0", 7, 1, lambda: print_symbol(equasion_string_ent, "0"))

add_button(main_window, "+", 4, 3, lambda: print_symbol(equasion_string_ent, "+"))
add_button(main_window, "-", 5, 3, lambda: print_symbol(equasion_string_ent, "-"))
add_button(main_window, "*", 6, 3, lambda: print_symbol(equasion_string_ent, "*"))
add_button(main_window, "/", 7, 3, lambda: print_symbol(equasion_string_ent, "/"))
add_button(main_window, "^", 4, 4, lambda: print_symbol(equasion_string_ent, "^"))
add_button(main_window, "\u221A", 5, 4, lambda: print_symbol(equasion_string_ent, "root("))
add_button(main_window, "log", 6, 4, lambda: print_symbol(equasion_string_ent, "log("))
add_button(main_window, "sin", 7, 4, lambda: print_symbol(equasion_string_ent, "sin("))
add_button(main_window, "cos", 4, 5, lambda: print_symbol(equasion_string_ent, "cos("))
add_button(main_window, "tg", 5, 5, lambda: print_symbol(equasion_string_ent, "tg("))
add_button(main_window, "ctg", 6, 5, lambda: print_symbol(equasion_string_ent, "ctg("))

add_button(main_window, "(", 4, 6, lambda: print_symbol(equasion_string_ent, "("))
add_button(main_window, ")", 5, 6, lambda: print_symbol(equasion_string_ent, ")"))
add_button(main_window, "\u232B", 7, 6, lambda: erase_one(equasion_string_ent))
add_button(main_window, "Clr", 7, 5, lambda: erase_all(equasion_string_ent))

add_button(main_window, ".", 7, 0, lambda: print_symbol(equasion_string_ent, "."))
add_button(main_window, ",", 7, 2, lambda: print_symbol(equasion_string_ent, ","))


main_window.mainloop()

