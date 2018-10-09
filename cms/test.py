from random import randint

def Insertsort(list):
    n = len(list)
    #总共排序n-1次
    for i in range(1,n):
        #初始化待插入下标
        k = i
        tmp = list[i]
        while i - 1 >=0 and tmp < list[i-1]:
            list[i] = list[i-1]
            #更新待插入下标
            k = i-1
            i = k
        list[k] = tmp



    return list

list1 = []
for i in range(20):
    list1.append(randint(1,1000))

print(list1)
list1 = Insertsort(list1)
print(list1)





