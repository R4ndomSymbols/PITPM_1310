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
    "^": lambda a,b: a^b,
    "root": lambda a,b: math.pow(a, -b),
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
    "cos": 1,
    "sin": 1,
    "tan": 1,
    "ctg": 1
}


def add_button(master, displayed_text, grid_row, grid_colunm , command):
    btn = tk.Button(master)
    btn.configure(background=main_color)
    btn.configure(text=displayed_text)
    btn.grid(column=grid_colunm, row=grid_row, sticky=tk.NSEW)
    btn['command'] = command

def print_symbol(entry, symbol):
    current_txt = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_txt + symbol)
    

def evaluate_string(message, output):
    output.delete(0, tk.END)
    if(len(message.get()) == 0):
        output.insert(0, "void_input")
    elif(not validate_brakets(message.get())):
        output.insert(0, "invalid brakets")
    else:
        t = evaluate(message.get())
        output.insert(0, str(t))
    #output.insert(0, "invalid input")
    return True

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
    return True

def evaluate(equasion):
    bracket_priority = 0
    parsed_equasion = list()
    op_count = 0
    i = 0
    while(i < len(equasion)):
        if(equasion[i].isdigit() or equasion[i] == '.'):
            t = get_number(equasion, i)
            parsed_equasion.append((t[0],bracket_priority*6))
            i = t[1]
        elif(equasion[i].isalpha()):
            d = get_func(equasion, i)
            parsed_equasion.append((d[0], bracket_priority*6))
            op_count+=1
            i = d[1]
        elif (equasion[i] in ('+','-','/','*','^')):
            parsed_equasion.append((equasion[i], bracket_priority*6))
            op_count +=1
            i+=1
        elif (equasion[i] == ')'):
            bracket_priority-=1
            i+=1
        elif (equasion[i] == '('):
            bracket_priority+=1
            i+=1
        else:
            return "unsopported symbol or operation"
    if(op_count>0):
        return evaluate_parsed_equasion(parsed_equasion)
    else: 
        return parsed_equasion[0][0]
    


def evaluate_parsed_equasion(equasion):
    is_obsolete = False
    max_priority = 0
    operation = ''
    current_pos = 0
    
    while(len(equasion) != 1):
        j = 0
        max_priority = 0
        for i in equasion:
            if(priorities.get(i[0]) == None):
                j+=1
                continue
            if(max_priority < priorities.get(i[0]) + i[1]):
                max_priority = priorities.get(i[0]) + i[1]
                operation = i[0]
                current_pos = j
                j+=1
        
        offset = offsets[operation]
        if(len(offset) == 1):
            pass
        elif(len(offset) == 2):

            try:
                print("after")
                print(equasion)
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
                print("after")
                print(equasion)
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
    while(equasion[position].isalpha() and position < len(equasion)):
        value+=equasion[position]
        position+=1
    if(avalible_funcs.get(value) != None):
        return (avalible_funcs.get(value), position)
    else:
        raise Exception()


main_window = tk.Tk()
main_window.title("Калькулятор")
main_window.configure(background=background_color)

for i in range(0, 3):
    main_window.columnconfigure(weight=1, index=i)
for j in range(0, 8):
    main_window.rowconfigure(index = j, weight=1)

lbl_result = tk.Label(text="Строка результата")
result_string_ent = tk.Entry()
lbl_equasion = tk.Label(text="Текущая строка")
sv = tk.StringVar()
equasion_string_ent = tk.Entry(main_window, textvariable=sv, validate="all", validatecommand = lambda: evaluate_string(sv, result_string_ent))



lbl_equasion.grid(row=0, columnspan=3, sticky=tk.NSEW)
equasion_string_ent.grid(row=1, columnspan=3, sticky=tk.NSEW)

lbl_result.grid(row = 2, columnspan=3, sticky=tk.NSEW)
result_string_ent.grid(row = 3, columnspan=3, sticky=tk.NSEW)


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


main_window.mainloop()

