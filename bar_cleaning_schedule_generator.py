import random
import numpy as np
import sys
from pandas import DataFrame

#DATA
Bar_staff_list = ["Savvas", "Ali", "Michael", "Mel", "Flo", "Jade",
"Damin", "Andre", "Yuval", "Sam", "Shaaroni", "Ayan",
"Frederik", "Sid", "Sarah", "Alex", "Anna-Marie", "Elsie", "Daniel", "Leanne", "Justin", "NONE"] # include NONE as last item in list

#UNAVAILABILITIES MAP
unavailabilities_dict = {
"Savvas":[10,11,12], "Ali":[], "Michael":[10,11,12], "Mel":[8,9,10,11,12], "Flo":[11,12,13], "Jade":[0,4,10,11,12],
"Damin":[2,3,10,11,12,13], "Andre":[8,9,10,11,12], "Yuval":[], "Sam":[0,6,8], "Shaaroni":[1,5,9,10,11,12,13], "Ayan":[0,3,7,10,11,12,13],
"Frederik":[10,11,12], "Sid":[], "Sarah":[8,9,10,11,12], "Alex":[10,11,12], "Anna-Marie":[3,4,10,11], "Elsie":[0,10,11,12], "Daniel":[2,10,11], "Leanne":[0,1,5,7,10,11],
"Justin":[1,3,8,9,10,11,12], "NONE":[]
}

list_size = len(Bar_staff_list)

#CHECK BEFORE CONTINUING THAT ALL BAR STAFF HAD THEIR UNAVAILABILITIES ENTERED IN DICTIONARY
if (list_size != len(unavailabilities_dict.keys())):
    sys.exit("Program exit: All bar staff need to have their unavailability entered in dictionary(include NONE in both).\n"
    "Bar_staff_list size = "+str(list_size)+"\n"
    "unavailabilities_dict size = "+str(len(unavailabilities_dict.keys())))

shift_count_1 = [0] * list_size

Sundays = 14
Sunday_dates = [
"13/10", #0
"20/10", #1
"27/10", #2
"03/11", #3
"10/11", #4
"17/11", #5
"24/11", #6
"01/12", #7
"08/12", #8
"15/12", #9
"22/12", #10
"29/12", #11
"05/01", #12
"12/01"] #13
per_Sunday = 3
print("Shifts per person from " + Sunday_dates[0] + " until " + Sunday_dates[-1] + ": " + str(Sundays*per_Sunday/list_size)+"\n")

#COMPUTATIONS
#DAY PRIORITY
day_priority = []
counting_unavailability = [0] * Sundays
for staff_name in unavailabilities_dict:
    for day_away in unavailabilities_dict[staff_name]:
        counting_unavailability[day_away] += 1

print("\nAvailability per day:")
for x in range(Sundays):
    print(Sunday_dates[x],list_size-counting_unavailability[x])

for x in range(Sundays):
    max_unavailability = max(counting_unavailability)
    index_unavailability = counting_unavailability.index(max_unavailability)
    day_priority.append(index_unavailability)
    counting_unavailability[index_unavailability] = -1

print("\nPriority list:")
for x in range(Sundays):
    print(Sunday_dates[day_priority[x]])

#SCHEDULE 1.0
schedule_dict_1 = {}
for x in range(Sundays):
    sunday_index = day_priority[x]
    day_list = []
    #print(Sunday_dates[sunday_index])
    for y in range(per_Sunday):
        i = random.randint(0,list_size-2)
        count = 1
        while ((Bar_staff_list[i] in day_list) or (sunday_index in unavailabilities_dict[Bar_staff_list[i]])):
            i = random.randint(0,list_size-2)
            count += 1
            if (count >= 1000):
                i = list_size-1 # NONE
                break # from the while loop
        day_list.append(Bar_staff_list[i])
        shift_count_1[i] += 1
    schedule_dict_1[Sunday_dates[sunday_index]] = day_list

#CHECK ALL GOOD WITH AVAILABILITY
for cleaning_day in schedule_dict_1:
    for staff_name in schedule_dict_1[cleaning_day]:
        cleaning_day_index = Sunday_dates.index(cleaning_day)
        if (cleaning_day_index in unavailabilities_dict[staff_name]):
            print("MISTAKE IN SCHEDULE")
            print("Day: "+cleaning_day)
            print("Staff: "+staff_name)
            print("Unavailability: "+unavailabilities_dict[staff_name])

print("\nSchedule 1.0:")
for x in range(Sundays):
    print(Sunday_dates[x],schedule_dict_1[Sunday_dates[x]])

print("\nShift count 1.0:")
for index in range(list_size):
    print(Bar_staff_list[index],shift_count_1[index])

# Now I will even out the shifts as much as possible
# First I will make copies of the previous lists/dictionaries
schedule_dict_2 = schedule_dict_1.copy()
shift_count_2 = shift_count_1.copy()

# defining a couple of useful functions
def get_shift_dates(staff_name):
    staff_shift_days = []
    for cleaning_day in schedule_dict_2:
        for name in schedule_dict_2[cleaning_day]:
            #print(name)
            if (staff_name == name):
                staff_shift_days.append(cleaning_day)
    return staff_shift_days

def get_names_with_shift_count(x):
    names_with_x_shifts = []
    for i in range(list_size-1):
        if (x == shift_count_2[i]):
            names_with_x_shifts.append(Bar_staff_list[i])
    return names_with_x_shifts

#SCHEDULE 2.0
print("\nShift changes to even out the number of shifts as much as possible")
keep_shifting = True
while (keep_shifting):
    keep_shifting = False
    max_shifts = max(shift_count_2)
    min_shifts = min(shift_count_2[0:(list_size-1)])
    diff_shifts = max_shifts - min_shifts
    if (diff_shifts > 1):
        max_names = get_names_with_shift_count(max_shifts)
        min_names = get_names_with_shift_count(min_shifts)
        swapped = False
        for min_name in min_names:
            for max_name in max_names:
                max_dates = get_shift_dates(max_name)
                min_dates = get_shift_dates(min_name)
                for date in max_dates:
                    date_index = Sunday_dates.index(date)
                    if (date not in min_dates) and (date_index not in unavailabilities_dict[min_name]):
                        schedule_dict_2[date].remove(max_name)
                        shift_count_2[shift_count_2.index(max_shifts)] -= 1
                        schedule_dict_2[date].append(min_name)
                        shift_count_2[shift_count_2.index(min_shifts)] += 1
                        keep_shifting = True
                        swapped = True
                        print("SWAPPED DATE: "+date+"\tMAX: "+max_name+"\tMIN: "+min_name)
                        #print("breaking once")
                        break
                if (swapped):
                    #print("breaking twice")
                    break
            if (swapped):
                #print("breaking thrice")
                break


#CHECK ALL GOOD WITH AVAILABILITY
for cleaning_day in schedule_dict_2:
    for staff_name in schedule_dict_2[cleaning_day]:
        cleaning_day_index = Sunday_dates.index(cleaning_day)
        if (cleaning_day_index in unavailabilities_dict[staff_name]):
            print("MISTAKE IN SCHEDULE")
            print("Day: "+cleaning_day)
            print("Staff: "+staff_name)
            print("Unavailability of staff: "+unavailabilities_dict[staff_name])

print("\nSchedule 2.0:")
for x in range(Sundays):
    print(Sunday_dates[x],schedule_dict_2[Sunday_dates[x]])

print("\nShift count 2.0:")
for index in range(list_size):
    print(Bar_staff_list[index],shift_count_2[index])

#OUTPUT TO EXCEL SHEET
#col_1: Sunday_dates
#col_2: Staff 1
#col_3: Staff 2
#col_4: Staff 3
def construct_staff_excel_columns(i):
    staff_column = []
    for date in Sunday_dates:
        staff_column.append((schedule_dict_2[date])[i])
    return staff_column

Staff_1 = construct_staff_excel_columns(0)
Staff_2 = construct_staff_excel_columns(1)
Staff_3 = construct_staff_excel_columns(2)
df = DataFrame({"Date":Sunday_dates, "Staff 1":Staff_1, "Staff 2":Staff_2, "Staff 3":Staff_3})
df.to_excel('.\\BarCleaningSchedule.xlsx', sheet_name='sheet1', index=False)
