def empty(arr):
    '''
    判断list中的所有元素是否都是空值
    :param arr:
    :return:  True：空， False：不为空
    '''
    if not isinstance(arr,list):
        return True

    for i in arr:
        if i:
            return False

    return True