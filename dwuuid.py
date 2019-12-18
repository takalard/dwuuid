#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = '283121442@qq.com'

import os,shutil
import os.path
import sys
import re


##################################### 参数初始化 - Begin ##########################

BASE64_KEYS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
BASE64_VALUES = [64]*128
# print 'BASE64_VALUES length = %d,%s'%(len(BASE64_VALUES),BASE64_VALUES)

for i in xrange(0,64):
    c = BASE64_KEYS[i]
    _idx_ = ord(c)
    BASE64_VALUES[_idx_] = i

HexChars = '0123456789abcdef'


UuidTemplate = ['']*36
UuidTemplate[8]='-'
UuidTemplate[13]='-'
UuidTemplate[18]='-'
UuidTemplate[23]='-'

print 'UuidTemplate length = %d,%s'%(len(UuidTemplate),UuidTemplate)

Indices = [0]*32
i = 0
for x in xrange(0,36):
    if x != 8 and x != 13 and x != 18 and x != 23:
        Indices[i]=x
        i = i + 1

print 'Indices length = %d,%s'%(len(Indices),Indices)

Reg_NormalizedUuid = r'^[0-9a-fA-F]{32}'

##################################### 参数初始化 - End #############################

################################# Uuid Function 相关 Begin #########################

#说明，_min_参数为True时，保留UUID的前两位，为False时，保留UUID的前5位
def compressUuid(_strUuid_,_isMin_):

    _strUuid_ = _strUuid_.replace('-', '')
    _searchObj_ = re.search(Reg_NormalizedUuid, _strUuid_, re.I)
    if _searchObj_:
        _strUuid_ = str(_searchObj_.group(0))
        _isReserved_ = 0
        if _isMin_ == True:
            _isReserved_ = 2
        else:
            _isReserved_ = 5

        return compressHex(_strUuid_, _isReserved_)
    else:
        return _strUuid_

def compressHex(_hexString_, _reservedHeadLength_):

    _hexStrLen_ = len(_hexString_)
    i = _reservedHeadLength_
    if _reservedHeadLength_ == 0:
        i = _hexStrLen_ % 3
    _strHead_ = _hexString_[0:i]

    _base64Chars_ = []
    while i < _hexStrLen_:
        _hexVal1_ = int(_hexString_[i],16)
        _hexVal2_ = int(_hexString_[i + 1],16)
        _hexVal3_ = int(_hexString_[i + 2],16)
        _idx1_ = (_hexVal1_ << 2) | (_hexVal2_ >> 2)
        _idx2_ = ((_hexVal2_ & 3) << 4) | _hexVal3_
        _base64Chars_.append(BASE64_KEYS[_idx1_])
        _base64Chars_.append(BASE64_KEYS[_idx2_])
        i += 3
    return _strHead_ + "".join(map(lambda x:str(x),_base64Chars_))

def decodeUuid(_strBase64_):
    _newUuid_ = decodeUuidBase(_strBase64_,BASE64_VALUES,UuidTemplate,HexChars,Indices)
    _strUuid_ = "".join(map(lambda x:str(x),_newUuid_))
    return _strUuid_

def decodeUuidBase(_strBase64_,_BASE64_VALUES_,_UuidTemplate_,_HexChars_,_Indices_):

    if len(_strBase64_) == 22:
        _UuidTemplate_[0] = _strBase64_[0]
        _UuidTemplate_[1] = _strBase64_[1]

        j = 2
        for i in xrange(2,22,2):
            c = _strBase64_[i]
            _idx_ = ord(c)        
            lhs = _BASE64_VALUES_[_idx_]

            c = _strBase64_[i+1]
            _idx_ = ord(c)        
            rhs = _BASE64_VALUES_[_idx_]

            _UuidTemplate_[_Indices_[j]] = _HexChars_[lhs >> 2]
            j = j+1
            _UuidTemplate_[_Indices_[j]] = _HexChars_[((lhs & 3) << 2) | rhs >> 4]
            j = j+1
            _UuidTemplate_[_Indices_[j]] = _HexChars_[rhs & 0xF]
            j = j+1

        return _UuidTemplate_
    elif len(_strBase64_) == 23:

        _UuidTemplate_[0] = _strBase64_[0]
        _UuidTemplate_[1] = _strBase64_[1]
        _UuidTemplate_[2] = _strBase64_[2]
        _UuidTemplate_[3] = _strBase64_[3]
        _UuidTemplate_[4] = _strBase64_[4]

        j = 5
        for i in xrange(5,23,2):
            c = _strBase64_[i]
            _idx_ = ord(c)        
            lhs = _BASE64_VALUES_[_idx_]

            c = _strBase64_[i+1]
            _idx_ = ord(c)        
            rhs = _BASE64_VALUES_[_idx_]

            _UuidTemplate_[_Indices_[j]] = _HexChars_[lhs >> 2]
            j = j+1
            _UuidTemplate_[_Indices_[j]] = _HexChars_[((lhs & 3) << 2) | rhs >> 4]
            j = j+1
            _UuidTemplate_[_Indices_[j]] = _HexChars_[rhs & 0xF]
            j = j+1

        return _UuidTemplate_

    else:
        return _strBase64_

################################# Uuid Function 相关 End #########################


def main():

    _base64key_ = "ecpdLyjvZBwrvm+cedCcQy"
    _strUuid_ = decodeUuid(_base64key_)
    print "base64 = %s,uuid = %s"%(_base64key_,_strUuid_)

    _newBase64key_ = compressUuid(_strUuid_,True)
    print "uuid = %s,base64 = %s"%(_strUuid_,_newBase64key_)

    
# for test
if __name__ == "__main__":
    main()