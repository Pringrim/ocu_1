test_dir = "E:/py_test/test3_1"   
test_file = "E:/python/test.txt"   

result = {}       
count = [0,0,0,0]   # 화면 가장 하단에 출력할 개수, 총 용량을 담을 공간을 선언
# 좌측부터 순서대로 확장자의 수, 폴더의 수, 총 파일의 수, 총 용량

option = 0   #확장자가 없지만 파일의 이름이 기존에 존재하는 확장자인 경우의 처리를 결정함
            #예를 들어, 파일명 'txt'와 'test.txt' 파일의 처리를 어떻게 할지 결정함
            #option = 0 이라면 둘은 같은 확장자로 인식하고 파일의 용량이 더해짐
            #option = 1이라면 둘은 다른 확장자로 인식하고 파일명 'txt'의 확장자명이 '<txt>'로 표기됨
            #option != 0,1 이라면 모든 확장자가 없는 파일의 확장자명이 '<@>' 형식으로 표기됨

import os

# utf-8 기반의 한글이 출력되는 페이지 모드로 설정한다.
os.system('chcp 65001')

try :   # test_dir이 지정하는 폴더가 없을 경우를 대비해 예외 처리를 한다.
    # 변수가 지정하는 폴더를 검사하기 위해 폴더 경로를 옮긴다.
    os.chdir(test_dir)
    # 윈도우 cmd의 dir 기능으로 해당 폴더를 검사한 후 test_file 경로의 txt파일에 저장한다.
    os.system(f'dir > {test_file}')

except :    # test_dir이 지정하는 폴더가 없을 경우
    print('존재하지 않는 폴더입니다...')

else :      # test_dir이 지정하는 폴더가 있을 경우
    with open(test_file, 'rt', encoding='utf8') as fh:
        txt_lst = fh.readlines()    #리스트 형식으로 저장

    for i in range(len(txt_lst)-1,-1,-1):   # txt_lst의 마지막 자료부터 첫번째 자료까지
        try:                      # 유의미한 데이터는 모두 yyyy-mm-dd 형식으로 시작하는 것을 이용해 원하는 데이터만 선별
            int(txt_lst[i][0:4])
        except:                     #오류가 나면 유의미한 데이터가 아니므로 삭제
            txt_lst.pop(i)
        else:
            if (txt_lst[i].find('<DIR>') >= 0):     # yyyy-mm-dd 형식으로 시작하는 데이터 중 <DIR>이 있는 데이터는 삭제
                txt_lst.pop(i)                      # 폴더의 개수는 필요하므로 count[1]에 저장
                count[1]+=1     # 폴더의 개수 저장

    count[2]=len(txt_lst)       # 파일의 개수 저장


    for i in range(len(txt_lst)):
        if(txt_lst[i].find('.') == -1) :    # 확장자가 있는지 찾고 확장자가 없는 파일이라면
            tmpa = txt_lst[i][txt_lst[i].find(":")+3:].strip()[:txt_lst[i][txt_lst[i].find(":")+3:].strip().find(' ')] # b에 파일명 / a에 파일 크기 저장
            tmpb = txt_lst[i][txt_lst[i].find(":")+3:].strip()[txt_lst[i][txt_lst[i].find(":")+3:].strip().find(' ') + 1:]  # yyyy-mm-dd "D" AM/PM hh:mm 형식이 딱 22글자라는 점을 이용
                                                                                    # 공백 제거 후 파일의 크기와 이름 분리

            if(option==0) :         #만약 option이 0이라면
                if (result.get(tmpb, 'no') == 'no'):
                    result[tmpb] = [int(tmpa.replace(',', ''))]     # 키가 선언 되어 있지 않다면 새로 선언
                else:
                    result[tmpb].append(int(tmpa.replace(',', ''))) # 이미 선언되어 있는 키라면 append 메서드 사용
            else :
                result['<'+tmpb+'>'] = [int(tmpa.replace(',', ''))] # 사용자 설정에 따라 부등호 기호 삽입
        else :                                          # 확장자가 있는 파일은
            tmpa=txt_lst[i][txt_lst[i].find(":")+3:].strip()[:txt_lst[i][txt_lst[i].find(":")+3:].strip().find(' ')]
            tmpb=txt_lst[i][txt_lst[i].find(":")+3:].strip()[txt_lst[i][txt_lst[i].find(":")+3:].strip().find(' ')+1:]
            tmpb=tmpb[tmpb.rfind('.')+1:]

            if(result.get(tmpb,'no')=='no') :              # 키가 선언 되어 있지 않다면 새로 선언
                result[tmpb]=[int(tmpa.replace(',',''))]
            else :
                result[tmpb].append(int(tmpa.replace(',','')))    # 이미 선언되어 있는 키라면 append 메서드 사용


    count[0]=len(result)        # 확장자의 수 저장

    for i in result.keys() :
        for j in range(len(result[i])) :    # 총 용량 저장
            count[3]+=result[i][j]

    print(f"\n{'확장자명'.center(13)}{'개수'.center(5)}{'파일용량'.center(15)}{'퍼센트'.ljust(7)}")
    if(count[0]!=0) :
        for i in sorted(result):
            if(i.find('<')!=0) :
                a=0
                for j in range(len(result[i])) :
                    a+=result[i][j]

                try :
                    b=(a/count[3])*100
                except :
                    b=0

                print(f'{i.ljust(15)}{str(len(result[i])).rjust(5)}{str(format(a,",d")).rjust(14)}{str(format(b,".1f")+"%").rjust(10)}')
            else :
                a=0
                for j in range(len(result[i])) :
                    a+=result[i][j]

                try :
                    b=(a/count[3])*100
                except :
                    b=0
                con=0       #부등호 표시한 파일명이 이미 있는지를 알아보는 변수
                for z in result.keys():
                    if(i.replace("<","").replace(">","")==z):
                        con+=1      #부등호 표시한 파일명이 이미 있는 확장자라면 con은 0이 아님
                if(con==0 and option==1):   #만약 부등호 표시한 파일명이 기존에 존재하는 확장자명이 아니면서 option이 1인 경우 부등호를 표기하지 않음
                    print(f'{i.replace("<","").replace(">","").ljust(15)}{str(len(result[i])).rjust(5)}{str(format(a,",d")).rjust(14)}{str(format(b,".1f")+"%").rjust(10)}')
                else :
                    print(f'{i.ljust(15)}{str(len(result[i])).rjust(5)}{str(format(a, ",d")).rjust(14)}{str(format(b, ".1f") + "%").rjust(10)}')
    else :
        print('파일이 없습니다...')

    print(f"\n확장자의 수={format(count[0],',d')}, 폴더의 수={format(count[1],',d')}, ", end='')
    print(f"총 파일의 수={format(count[2],',d')}, 총 용량={format(count[3],',d')}")
