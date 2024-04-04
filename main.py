test_dir = "D:/python/test"       # 1) 파일의 내용을 관찰할 폴더
test_file = "E:/python/test.txt"   # 2) dir 수행결과를 지정하는 파일

result = {}
count = [0,0,0,0]   # 화면 가장 하단에 출력할 개수, 총 용량을 담을 공간을 리스트로 선언
# 좌측부터 순서대로 확장자의 수, 폴더의 수, 총 파일의 수, 총 용량

import os

# utf-8 기반의 한글이 출력되는 페이지 모드로 설정한다.
os.system('chcp 65001')

try :   # test_dir이 지정하는 폴더가 없을 경우를 대비해 예외 처리를 한다.
    # 변수가 지정하는 폴더를 검사하기 위해 폴더 경로를 옮긴다.
    os.chdir(test_dir)
    # 윈도우 cmd의 dir 기능으로 해당 폴더를 검사한 후 test_file 경로의 txt파일에 저장한다.
    os.system(f'dir > {test_file}')

except :    # test_dir이 지정하는 폴더가 없을 경우
    print('파일이 없습니다...')

else :      # test_dir이 지정하는 폴더가 있을 경우
    with open(test_file, 'rt', encoding='utf8') as fh:
        txt_lst = fh.readlines()    #리스트 형식으로 저장



    for i in range(len(txt_lst)-1,-1,-1):   # txt_lst의 마지막 자료부터 첫번째 자료까지
        try:                      # 유의미한 데이터는 모두 yyyy-mm-dd 형식으로 시작하는 것을 이용해 원하는 데이터만 선별
            int(txt_lst[i][0:4])
        except:
            txt_lst.pop(i)
        else:
            if (txt_lst[i].find('<DIR>') >= 0):     # yyyy-mm-dd 형식으로 시작하는 데이터 중 <DIR>이 있는 데이터는 삭제
                txt_lst.pop(i)
                count[1]+=1     # 폴더의 개수 저장

    count[2]=len(txt_lst)       # 파일의 개수 저장

    for i in range(len(txt_lst)):
        if(txt_lst[i].find('.') == -1) :    # 확장자가 있는지 찾고 확장자가 없는 파일이라면
            tmpa = txt_lst[i][22:].strip()[:txt_lst[i][22:].strip().find(' ')] # b에 파일명 / a에 파일 크기 저장
            tmpb = txt_lst[i][22:].strip()[txt_lst[i][22:].strip().find(' ') + 1:]

            result[tmpb]=[int(tmpa.replace(',',''))]          # 확장자가 없는 파일은 중복될 수 없으므로 바로 선언
        else :                                          # 확장자가 있는 파일은
            tmpa=txt_lst[i][22:].strip()[:txt_lst[i][22:].strip().find(' ')]
            tmpb=txt_lst[i][22:].strip()[txt_lst[i][22:].strip().find(' ')+1:]
            tmpb=tmpb[tmpb.rfind('.')+1:]

            if(result.get(tmpb,'no')=='no') :              # 키가 선언 되어 있지 않다면 새로 선언
                result[tmpb]=[int(tmpa.replace(',',''))]
            else :
                result[tmpb].append(int(tmpa.replace(',','')))    # 이미 선언되어 있는 키라면 append 메서드 사용


    count[0]=len(result)        # 확장자의 수 저장

    for i in result.keys() :
        for j in range(len(result[i])) :    # 총 용량 저장
            count[3]+=result[i][j]

    print(f"\n{'확장자명'.center(13)}{'갯수'.center(5)}{'파일용량'.center(15)}{'퍼센트'.ljust(7)}")
    if(count[0]!=0) :
        for i in sorted(result):
            a=0
            for j in range(len(result[i])) :
                a+=result[i][j]
            print(f'{i.ljust(15)}{str(len(result[i])).rjust(5)}{str(format(a,",d")).rjust(14)}{str(format((a/count[3])*100,".1f")+"%").rjust(10)}')
    else :
        print('파일이 없습니다...')

    print(f"\n확장자의 수={count[0] }, 폴더의 수={count[1]},", end='')
    print(f"총 파일의 수={count[2]}, 총 용량={count[3]}")
