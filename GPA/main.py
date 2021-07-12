def write_to_file():
    f = open("data/all.txt", "a")
    text = ""
    while True:
        text += input()
    f.write(text)
    f.close()


def read_from_file(filename):
    CourseList ={}
    f = open('data/'+filename+".txt", "r")
    course_list = []
    term="o"
    for line in f:
        temp_list = line.split(":")
        if len(temp_list) == 2:
            CourseList[term]=course_list
            term = temp_list[0]+"/"+temp_list[1]
            course_list = []
        else:
            course_list.append(temp_list)
    f.close()
    return CourseList

def GPA(scale, CourseList):

    four_point_zero = {'A+':4.0, 'A':4.0, 'A-':3.7, 'B+':3.3, 'B':3.0, 'S':0.0}
    four_point_three = {'A+':4.3, 'A':4.0, 'A-':3.7, 'B+':3.3, 'B':3.0, 'S':0.0}
    total_scores=0
    keys = CourseList.keys()
    total_time=0
    for key in keys:
        for course in CourseList[key]:
            if scale == 4.0:
                score = four_point_zero[course[2][:-1]]
            elif scale == 4.3:
                score = four_point_three[course[2][:-1]]
            time = float(course[1])
            if score != 0.0:
                total_time += float(time)
            # print(course[0], time, score)

            temp = score*time
            total_scores+=temp
        # print(total_time)
    # print(total_time)
    return total_scores/total_time



if __name__ == '__main__':
    CourseList = read_from_file("all")
    # print(CourseList)
    print("GPA: ", GPA(4.3, CourseList))
    print("GPA: ", GPA(4.0, CourseList))
