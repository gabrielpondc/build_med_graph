import re
import UserDicNatureRecognition as UNR
def compare(kdzz,fdzz):
    # Create dictionaries to count occurrences in kdzz and fdzz
    kdzz_count = {}
    fdzz_count = {}

    # Initialize result lists
    kdzz_result = []
    fdzz_result = []

    # Count occurrences in kdzz
    for symptom in kdzz:
        if symptom in kdzz_count:
            kdzz_count[symptom] += 1
        else:
            kdzz_count[symptom] = 1

    # Count occurrences in fdzz
    for symptom in fdzz:
        if symptom in fdzz_count:
            fdzz_count[symptom] += 1
        else:
            fdzz_count[symptom] = 1

    # Iterate through kdzz and check occurrences
    for symptom in kdzz:
        if kdzz_count[symptom] > fdzz_count.get(symptom, 0):
            kdzz_result.append(symptom)

    # Iterate through fdzz and check occurrences
    for symptom in fdzz:
        if fdzz_count[symptom] >= kdzz_count.get(symptom, 0):
            fdzz_result.append(symptom)
    return kdzz_result,fdzz_result

def deny_check(text):
    text_list = re.split(r"[，。？！,?!;；]", str(text))
    map = {0: [], 1: []}
    fdzz = []
    kdzz = []
    for shorts in text_list:
         
        result,s=UNR.get_word_param(shorts)

        # if re.match(r".*(无|否认|不伴|排除|未|没有)#ab(.*#a)?([\u4e00-\u9fa5]{1,}(#dis|#sym){1})+(、#w[\u4e00-\u9fa5]{1,}(#dis|#sym){1})*.*", s):
            
        #     for t in result:
        
        #         if result[t] == "dis":
        #             fdzz.append(t)
        #         elif result[t] == "sym":
        #             fdzz.append(t)
        # elif re.match(r".未#ab[\u4e00-\u9fa5]+(#dis|#sym){1}", s):
        #     for t in result:
                
        #         if result[t] == "dis":
        #             fdzz.append(t)
        #         elif result[t] == "sym":
        #             fdzz.append(t)
        # elif re.match(r".*[\u4e00-\u9fa5]{1,}(#dis|#sym){1}阴性#ab.*", s):
        #     for t in result:
                
        #         if result[t] == "dis":
        #             fdzz.append(t)
        #         elif result[t] == "sym":
        #             fdzz.append(t)
        # else:
        #     for t in result:  
                
        #         if result[t] == "dis":
        #             kdzz.append(t)
        #         elif result[t] == "sym":
        #             kdzz.append(t)
        if re.match(r".*(无|否认|不伴|排除|未|没有)#ab(.*#a|.*#p|.*#b)?([\u4e00-\u9fa5]{1,}(#sym|#dis){1})+(、#w[\u4e00-\u9fa5]{1,}(#sym){1})*.*", s):
            for t in result:
                if result[t] == "sym":
                    fdzz.append(t)
        elif re.match(r".未#ab[\u4e00-\u9fa5]+(#sym){1}", s):
            for t in result:
                if result[t] == "sym":
                    fdzz.append(t)
        elif re.match(r".*[\u4e00-\u9fa5]{1,}(#sym){1}阴性#ab.*", s):
            for t in result:
                if result[t] == "sym":
                    fdzz.append(t)
        else:
            for t in result:  
                if result[t] == "sym":
                    kdzz.append(t)

        if re.match(r".*(无|否认|不伴|排除|未|没有)#ab(.*?)([\u4e00-\u9fa5]{1,}(#dis){1})+(、#w[\u4e00-\u9fa5]{1,}(#dis){1})*.*", s):
            for t in result:
                if result[t] == "dis":
                    fdzz.append(t)
        elif re.match(r".未#ab[\u4e00-\u9fa5]+(#dis){1}", s):
            for t in result:
                if result[t] == "dis":
                    fdzz.append(t)
        elif re.match(r".*[\u4e00-\u9fa5]{1,}(#dis){1}阴性#ab.*", s):
            for t in result:
                if result[t] == "dis":
                    fdzz.append(t)
        else:
            for t in result:  
                if result[t] == "dis":
                    kdzz.append(t)

        if re.match(r".*(无|否认|不伴|排除|未|没有)#ab(.*?)([\u4e00-\u9fa5]{1,}(#tra){1})+(、#w[\u4e00-\u9fa5]{1,}(#tra){1})*.*", s):
            for t in result:
                if result[t] == "tra":
                    fdzz.append(t)
        else:
            for t in result:   
                if result[t] == "tra":
                    kdzz.append(t)

    map[0] = fdzz
    map[1] = kdzz
    kdzz,fdzz=compare(kdzz,fdzz)
    # denylist = [v for v in map.values()]
    fdzz_str="、".join(list(set(fdzz)))
    kdzz_str = "、".join(list(set(kdzz)))
    
    return kdzz_str


