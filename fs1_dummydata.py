import pandas as pd
from utils import load_from_mongodb
from Prototype1_final import ResourceRecommendation
import random
from random import randrange
import datetime 


def random_date(start,l):
   current = start
   while l >= 0:
    current = current + datetime.timedelta(minutes=random.choice([15,30]))
    yield current
    l-=1
def end_time(giventime):
    current = giventime
    current = current + datetime.timedelta(minutes = random.choice([30, 45, 60,90]))
    yield current
    

startDate = datetime.datetime(2021, 6, 11,8,00)
lesson_time = []

for x in reversed(list(random_date(startDate,150))):
    for y in list(end_time(x)):
        lesson_time.append((x.strftime("%d/%m/%y %H:%M"), y.strftime("%d/%m/%y %H:%M")))
print(lesson_time)

obj = ResourceRecommendation() 
list_of_names_and_kps = obj.load_KPs_for_FS1()
column_names = ['name', 'teacher', 'kp_covered', 'start_time', 'end_time', 'price', 'rating']
df = pd.DataFrame(columns = column_names)
teacher = ['Trần Thị Ánh', 'Nguyễn Văn Thuận', 'Trần Thị Phương', 'Đào Mai Anh', 'Nguyễn Văn Nam', 'Trần Duy Mạnh', 'Hoài Linh', 'Nguyễn Văn Thánh']
for i in range(150):
    tuple = random.choice(list_of_names_and_kps)
    time = random.choice(lesson_time)
    df = df.append({'name': tuple[0] , 'teacher': random.choice(teacher) , 'kp_covered': tuple[1], 'start_time': time[0], 'end_time': time[1], 'price': random.choice([0, 50000, 75000, 100000]) , 'rating': randrange(5)}, ignore_index = True)
df.to_csv(r'C:\Users\Admin\Desktop\Assignments\Work stuffs\FS1_resources.csv')