
import codecs

# with codecs.open("C:/Users/Admin/Desktop/เทียบเฉลย/raw test/25kb 3889 test.txt","r") as f:
#     txt = f.read().replace(" ","").replace("\n","").replace("\t","")

# with codecs.open("text_sss.txt","w",encoding="utf-8") as f:
#         f.write(txt)


def genPatternSearch(text1,text2,stepLength,stepNext = 1,startIndex =0,stopIndex = 0):
    stepNext = stepLength - stepNext
    pattern=[]
    if(stepNext<stepLength):
        while(1):
            if(len(text1[startIndex:stopIndex+stepLength])==stepLength):
                print(">>>",text1[startIndex:stopIndex+stepLength])
                pattern.append("".join(text1[startIndex:stopIndex+stepLength]))
            if(stopIndex+stepLength>len(text1)):
                break
            startIndex+=stepLength-stepNext
            stopIndex+=stepLength-stepNext
        return pattern
    else:
        print("exception infinite loop")

if __name__ == "__main__":
    import tltk
    text1 ="""ออดิชั่นแอนด์"""
    text2 = "แอนด์"

    text1 = tltk.nlp.syl_segment(text1)
    text2 = tltk.nlp.syl_segment(text2)


    stepLength = 5
    stepNext = 1

    startIndex =0
    stopIndex = 0
    pattern = genPatternSearch(text1,text2,stepLength,stepNext,startIndex,stopIndex)
    print(pattern,text2 in pattern)

