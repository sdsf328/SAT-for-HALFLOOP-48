import AES_BCT
import AES_DDT
# 刻画BCT SAT
# 1-7位:输入差分（upper trail） 8-14位：输出差分（lower trail） 15，16位：概率

# 把8位输入差分变成7位
def inp_7_var():
    inp_7_var_list=[]
    # j为7位变量
    j=0
    # i为8位变量
    i=1
    while(i<256):
        if(i==1):
            # print(bin(i)[2:].rjust(8, '0')+bin(j)[2:].rjust(7, '0'))
            inp_7_var_list.append(bin(j)[2:].rjust(7, '0'))
            i+=1
        else:
            # print(bin(i)[2:].rjust(8, '0')+bin(j)[2:].rjust(7, '0'))
            inp_7_var_list.append(bin(j)[2:].rjust(7, '0'))
            i+=1
            # print(bin(i)[2:].rjust(8, '0')+bin(j)[2:].rjust(7, '0'))
            inp_7_var_list.append(bin(j)[2:].rjust(7, '0'))
            i+=1
        j+=1
    return inp_7_var_list

def proba(pr):
    proba_list = ['01','10','11']
    if (pr == 2 ):
        return proba_list[0]
    elif (pr == 4 ):
        return proba_list[1]
    else:
        # 概率为6/256
        return proba_list[2]

# 把8位输出差分变成7位
# example:7bit输入差分0000001代表00000001和00000010，把两个8bit输入差分对应的输出差分概率相同的分成一组，概率不同的分为一组
def divide_group_pr(inp_diff_8):
    same_pr = []
    diff_pr = []
    for out_diff in range(1, 256):
        if(AES_BCT.AesResult[inp_diff_8][out_diff]==AES_BCT.AesResult[inp_diff_8+1][out_diff] and AES_BCT.AesResult[inp_diff_8][out_diff]!=0 and AES_BCT.AesResult[inp_diff_8+1][out_diff]!=0):
            # 相同输出差分值且概率相同,记录输出差分值时，概率要×2
            pr=2*AES_BCT.AesResult[inp_diff_8][out_diff]
            # 把输出差分从int型转为str型
            out_diff=bin(out_diff)[2:].rjust(8, '0')
            same_pr.append(out_diff+proba(pr))

        # 两个相同输出差分值，概率一个大（4/256），一个小（2/256），选择概率大的一者
        elif (AES_BCT.AesResult[inp_diff_8][out_diff] != AES_BCT.AesResult[inp_diff_8+1][out_diff] and AES_BCT.AesResult[inp_diff_8][out_diff] != 0 and AES_BCT.AesResult[inp_diff_8][
            out_diff] != 0):
            pr=AES_BCT.AesResult[inp_diff_8][out_diff]+AES_BCT.AesResult[inp_diff_8+1][out_diff]
            out_diff = bin(out_diff)[2:].rjust(8, '0')
            diff_pr.append(out_diff+proba(pr))

        elif(AES_BCT.AesResult[inp_diff_8][out_diff]!=0 and AES_BCT.AesResult[inp_diff_8+1][out_diff]==0):
            pr=AES_BCT.AesResult[inp_diff_8][out_diff]
            out_diff = bin(out_diff)[2:].rjust(8, '0')
            diff_pr.append(out_diff + proba(pr))

        elif(AES_BCT.AesResult[inp_diff_8][out_diff]==0 and AES_BCT.AesResult[inp_diff_8+1][out_diff]!=0):
            pr=AES_BCT.AesResult[inp_diff_8+1][out_diff]
            out_diff = bin(out_diff)[2:].rjust(8, '0')
            diff_pr.append(out_diff + proba(pr))
    # 7bit输出差分+2bit概率
    # print('diff_group:%s'%diff_pr)
    # print('same_group:%s'%same_pr)
    # 具有相同概率和不相同概率的输出差分加起来有191个
    # print('len_same:%s'%len(same_pr))
    # print('len_diff:%s' % len(diff_pr))
    return same_pr,diff_pr

# 把两个列表的值按升序排列，返回一个新列表
def sorted_list(inp_diff_8):

    same_pr, diff_pr = divide_group_pr(inp_diff_8)
    list=same_pr+diff_pr
    list.sort()
    # print('len_same+diff:%s'%len(list))
    return list

# 寻找相同概率组合和不相同概率组合里高位为0的输出差分,如果满足条件，输出差分最高位是0的8bit差分值分为一组G0 ;输出差分最高位是1的8bit差分值分为一组G1

# def sham_compare(word1, word2, word1_index, word2_index,delete_index_list):
#     same_list=[]
#     """
#     输入两个10位二进制字符串，第0位不同且1-7位相同则视为伪相同
#
#     :param word1: 二进制字符串1
#     :param word2: 二进制字符串2
#     :return:
#     """
#     #  8bit输出差分如何得到7bit差分原则：如果第一比特相同，如果后面7bit一定不完全相同，则去除第1bit（向左移1位）；第一bit不同，则
#     # 如果最高位相同 2-8位一定不全相同，返回列表
#     if word1[0] == word2[0]:
#         return list()
#     else:
#         # 如果最高位不同时，且2-8bit不全相同时，返回列表
#         if word1[1:8] != word2[1:8]:
#             return list()
#         # 如果最高位不同时，且2-8位全相同
#         else:
#             # 将8-9位较小的元素索引加入待删除列表
#             compare1 = int(word1[8:10],2)
#             compare2 = int(word2[8:10],2)
#             if compare1 < compare2:
#                 delete_index_list.append(word1_index)
#             elif compare1 > compare2:
#                 delete_index_list.append(word2_index)
#             else:
#                 # 如果两者概率相同，则把两者的索引都加入待删除的列表中，然后放入到same_list表中。因为相同概率的元素体量还是较大的，所以我们要保留概率相同的元素。
#                 same_list.append(word1)
#                 same_list.append(word2)
#                 delete_index_list.append(word1_index)
#                 delete_index_list.append(word2_index)
#
#     # print('same_list:%s'%same_list)
#     return delete_index_list, same_list

def sham_compare(word1, word2, word1_index, word2_index,delete_index_list):
    same_list=[]
    """
    输入两个10位二进制字符串，第0位不同且1-7位相同则视为伪相同

    :param word1: 二进制字符串1
    :param word2: 二进制字符串2
    :return:
    """
    #  8bit输出差分如何得到7bit差分原则：如果第一比特相同，如果后面7bit一定不完全相同，则去除第1bit（向左移1位）；第1bit不同，则
    # 如果最高位不同 2-8位全相同，且概率相同返回列表
    if word1[0]!= word2[0] and word1[1:8]== word2[1:8]:
        # compare1 = int(word1[8:10], 2)
        # compare2 = int(word2[8:10],2)
        # if word1[8:10] ==word2[8:10]:
            # 如果两者概率相同，则把两者的索引都加入待删除的列表中，然后放入到same_list表中。因为相同概率的元素体量还是较大的，所以我们要保留概率相同的元素。
            same_list.append(word1)
            # print(same_list)
            same_list.append(word2)
            # print(same_list)
            delete_index_list.append(word1_index)
            delete_index_list.append(word2_index)
    else:
        return list()
    # print('same_list:%s'%same_list)
    return delete_index_list, same_list

def delete_sham_num(delete_list,inp_diff_8):
    """
    根据索引删除伪重复元素：
    :return:
    """
    temps = sorted_list(inp_diff_8)
    result_list = []
    # print(delete_list,type(delete_list))
    for index in delete_list:
        # 遍历每一个待删除元素的索引
        temps[index] = "#"
        # 删除索引所指元素
    for i in range(len(temps)):
        if temps[i] == "#":
            continue
        result_list.append(temps[i])
    # result_list中存放着删除伪重复元素后的元素
    # print('result_list%s'%result_list)
    # print(len(result_list))
    return result_list


def BCT(inp_diff_8,inp_diff_7):
    same_list=[]
    list_all = sorted_list(inp_diff_8)
    # print('list_all:%s'%list_all)
    i = 0
    # 初始化delete_index_list
    delete_index_list = list()
    while i < len(list_all):
        j = i + 1
        while j < len(list_all):
            res = sham_compare(list_all[i], list_all[j], i, j, delete_index_list)
            # delete_index_list=res[0]
            if res != []:
                # same_list=res[1]
                same_list.append(res[1])
                # print('same_list:%s'%same_list)
            j += 1
        i += 1
        # print('same_list%s' % same_list)
    # 除第一位不同，其他位全部相同且概率相同的两元素
    same_list_0=[]
    same_list_1=[]
    for num in range (0,len(same_list)):
        if same_list[num]!=[]:
            same_list_0.append(bin(inp_diff_7)[2:].rjust(7,'0')+same_list[num][0][1:])
            same_list_1.append(bin(inp_diff_7)[2:].rjust(7, '0') + same_list[num][1][1:])
    # print('len_same_list:%s'%len(same_list_0))
    # print('same_list_0:%s'%same_list_0)
    # print('same_list_1%s'%same_list_1)

    result_list_0 = []
    result_list_1 = []
    if len(delete_index_list)>0:
        # print(delete_index_list)
    # 取每个元素（输出差分）的第2到8bit, 即将8bit输出差分变成7bit,并按照最高位值的不同进行分组
        result_list=delete_sham_num(delete_index_list,inp_diff_8)
        # print('len_result_list:%s'%len(result_list))
        for j in range(len(result_list)):
            # G0
            if (result_list[j][0]=='0'):
                result_list_0.append(bin(inp_diff_7)[2:].rjust(7,'0')+result_list[j][1:])
            # G1
            if(result_list[j][0]=='1'):
                result_list_1.append(bin(inp_diff_7)[2:].rjust(7,'0')+result_list[j][1:])
    G0=result_list_0+same_list_0
    G1=result_list_1+same_list_1
    # print('G0:%s'%G0)
    # print(len(G0))
    print('G1:%s'%G1)
    # print(len(G1))
    return result_list_0+same_list_0, result_list_1+same_list_1

if __name__ == '__main__' :
    inp_diff_8=1
    inp_diff_7 = 1
    # 254
    while inp_diff_8 <= 254:
        # 127
        while inp_diff_7 <= 127:
            BCT(inp_diff_8, inp_diff_7)
            inp_diff_8+=2
            inp_diff_7 += 1


#     8bit全1的差分，对应7bit全0的差分
for j in range(1,256):
    value = bin(j)[2:].rjust(8, '0')
    if AES_BCT.AesResult[255][j] == 2:
        if value[0]=='1':
            # G0
            print('0000000'+value[1:8]+'01,')
        # else:
            # G1
            # print('0000000' + value[1:8])
    elif AES_BCT.AesResult[255][j] == 4:
        if value[0]=='1':
            # G0
            print('0000000'+value[1:8]+'10,')
        # else:
            # G1
            # print('0000000' + value[1:8])
    else:
        if value[0]=='1':
            # G0
            print('0000000'+value[1:8]+'11,')
        # else:
            # G1
            # print('0000000' + value[1:8])






