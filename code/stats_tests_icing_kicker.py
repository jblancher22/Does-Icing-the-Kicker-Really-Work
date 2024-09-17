import pandas as pd
import cmh
import json
import matplotlib.pyplot as plt
import math

with open('fg_log_8.json','r') as file:
    data=file.readlines()


#group 1 = 18-23 yards
#group 2 = 24-29 yards
#group 3 = 30-35 yards
#group 4 = 36-41 yards
#group 5 = 42-47 yards
#group 6 = 48-53 yards
#group 7 = 54-59 yards
#group 8 = 60+ yards
#I chose 5 yard increments to stratify field goal distance
#so that there is enough sample size per distance while also not comparing a 18 to 60 yard field goal  

group1=[]
group2=[]
group3=[]
group4=[]
group5=[]
group6=[]
group7=[]
group8=[]


def stratify(distance):
    if 18<= distance <= 23:
        group1.append([iced,converted])
        return 'group 1'
    elif 24<=distance<=29:
        group2.append([iced,converted])
        return 'group 2'
    elif 30<=distance<=35:
        group3.append([iced,converted])
        return 'group 3'
    elif 36<= distance <= 41:
        group4.append([iced,converted])
        return 'group 4'
    elif 42<= distance <= 47:
        group5.append([iced,converted])
        return 'group 5'
    elif 48<= distance <= 53:
        group6.append([iced,converted])
        return 'group 6'
    elif 54<= distance <= 59:
        group7.append([iced,converted])
        return 'group 7'
    else:
        group8.append([iced,converted])
        return 'group 8'

def calculate_proportions(group):
    iced_attempts=0
    non_iced_attempts=0
    iced_successes=0
    non_iced_successes=0
    for item in group:
        if item[0]==0:
            non_iced_attempts+=1
            if item[1]==1:
                non_iced_successes+=1
        else:
            iced_attempts+=1
            if item[1]==1:
                iced_successes+=1
    iced_proportion=(iced_successes/iced_attempts)
    non_iced_proportion=(non_iced_successes/non_iced_attempts)
    error_i=0
    error_ni=0
    iced_failures=iced_attempts-iced_successes
    non_iced_failures=non_iced_attempts-non_iced_successes
    if iced_successes>=10 and iced_failures>=10: #only calculates error bar if there are more than 10 successes and failures
        error_i=math.sqrt((iced_proportion*(1-iced_proportion))/iced_attempts)
    else:
        error_i=0 #or show no error bar

    if non_iced_successes>=10 and non_iced_failures>=10: #only calculates error bar if there are more than 10 successes and failures
        error_ni=math.sqrt((non_iced_proportion*(1-non_iced_proportion))/non_iced_attempts)
    else:
        error_ni=0 #or show no error bar

    z_score=1.96 #assume 95% confidence interval
    
    return iced_proportion*100,non_iced_proportion*100,error_i*100*z_score,error_ni*100*z_score

            


cleaned=[]

for line in data:
    parsed_line = json.loads(line)
    distance=int(parsed_line['distance'])
    iced=parsed_line['Timeout by opposing team the play prior?']
    converted=parsed_line['Converted?']
    cleaned.append([stratify(distance),iced,converted])

all_groups=[group1,group2,group3,group4,group5,group6,group7,group8]


total_iced_attempts=0
total_non_iced_attempts=0
total_iced_conversions=0
total_non_iced_conversions=0
for group in all_groups:
    for item in group:
        if item[0]==0:
            total_non_iced_attempts+=1
            if item[1]==1:
                total_non_iced_conversions+=1
        else:
            total_iced_attempts+=1
            if item[1]==1:
                total_iced_conversions+=1
                
total_ip=(total_iced_conversions/total_iced_attempts) #calculates proportion of made kicks when iced for all strata 
total_nip=(total_non_iced_conversions/total_non_iced_attempts) #calculates proportion of made kicks when not iced for all strata


error_total_i=math.sqrt((total_ip*(1-total_ip))/total_iced_attempts)
error_total_ni=math.sqrt((total_nip*(1-total_nip))/total_non_iced_attempts)



#"ip" = iced proportion, "nip" = not iced proportion
ip1,nip1,error1_i,error1_ni=calculate_proportions(group1)
ip2,nip2,error2_i,error2_ni=calculate_proportions(group2)
ip3,nip3,error3_i,error3_ni=calculate_proportions(group3)
ip4,nip4,error4_i,error4_ni=calculate_proportions(group4)
ip5,nip5,error5_i,error5_ni=calculate_proportions(group5)
ip6,nip6,error6_i,error6_ni=calculate_proportions(group6)
ip7,nip7,error7_i,error7_ni=calculate_proportions(group7)
ip8,nip8,error8_i,error8_ni=calculate_proportions(group8)



x=[1,2,4,5,7,8,10,11,13,14,16,17,19,20,22,23,25,26]
y=[ip1,nip1,ip2,nip2,ip3,nip3,ip4,nip4,ip5,nip5,ip6,nip6,ip7,nip7,ip8,nip8,total_ip*100,total_nip*100]
colors=['b','r']*9
errors=[error1_i,error1_ni,error2_i,error2_ni,error3_i,error3_ni,error4_i,error4_ni,error5_i,error5_ni,error6_i,error6_ni,error7_i,error7_ni,error8_i,error8_ni,error_total_i*100,error_total_ni*100]

import matplotlib.patches as mplpatches

red_patch=mplpatches.Patch(color='blue',label='Iced')
blue_patch=mplpatches.Patch(color='red',label='Not-Iced')
plt.xlabel('Distance groups')
plt.ylabel('Percent of Converted Kicks')

custom_ticks = [1.5, 4.5, 7.5, 10.5, 13.5, 16.5, 19.5, 22.5,25.5] 
custom_labels = ['18-23', '24-29', '30-35', '36-41', '42-47', '48-53', '54-59', '60+','total'] 
plt.xticks(custom_ticks, custom_labels)

plt.bar(x,y,color=colors,yerr=errors)
plt.legend(handles=[red_patch,blue_patch])
plt.show()



df=pd.DataFrame(cleaned,columns=['distance groups','Iced','Converted'])   

result=cmh.CMH(df,"Iced","Converted",stratifier='distance groups')
print(result)

print('Since p is greater than .05, we fail to reject the null hypothesis and conclude that "icing" the kicker does not have a statistically significant impact on converting a kick')



