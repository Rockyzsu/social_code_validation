# -*-coding=utf-8-*-

# @Time : 2018/10/26 10:52
# @File : social_code_gen.py
# 生产社会统一码

# 统一社会信用代码中不使用I,O,Z,S,V
SOCIAL_CREDIT_CHECK_CODE_DICT = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22,
    'P': 23, 'Q': 24,
    'R': 25, 'T': 26, 'U': 27, 'W': 28, 'X': 29, 'Y': 30}

# GB11714-1997全国组织机构代码编制规则中代码字符集
ORGANIZATION_CHECK_CODE_DICT = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22,
    'N': 23, 'O': 24, 'P': 25, 'Q': 26,
    'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35}


class CreditIdentifier(object):
    def CreateC9(self, code):
        # 第i位置上的加权因子
        weighting_factor = [3, 7, 9, 10, 5, 8, 4, 2]
        # 第9~17位为主体标识码(组织机构代码)
        organization_code = code[8:17]
        # 本体代码
        ontology_code = organization_code[0:8]
        # 生成校验码
        tmp_check_code = self.gen_check_code(
            weighting_factor, ontology_code, 11, ORGANIZATION_CHECK_CODE_DICT)
        return code[:16] + tmp_check_code

    def getSocialCreditCode(self, code):
        code = self.CreateC9(code[:16])
        # 第i位置上的加权因子
        weighting_factor = [1, 3, 9, 27, 19, 26, 16,
                            17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
        # 本体代码
        ontology_code = code[0:17]
        # 计算校验码
        tmp_check_code = self.gen_check_code(
            weighting_factor, ontology_code, 31, SOCIAL_CREDIT_CHECK_CODE_DICT)
        return code[:17] + tmp_check_code

    # 只返回一个值 字符
    def gen_check_code(self, weighting_factor, ontology_code, modulus, check_code_dict):
        total = 0
        for i in range(len(ontology_code)):
            if ontology_code[i].isdigit():
                total += int(ontology_code[i]) * weighting_factor[i]
            else:
                total += check_code_dict[ontology_code[i]
                         ] * weighting_factor[i]
        C9 = modulus - total % modulus
        C9 = 0 if C9 == 31 else C9
        C9 = list(check_code_dict.keys())[
            list(check_code_dict.values()).index(C9)]
        return C9


if __name__ == '__main__':
    codeHelper = CreditIdentifier()
    input_code = '91430111MA4L41YT1U'
    ret=codeHelper.getSocialCreditCode(input_code)

    if ret == input_code:
        print("统一社会信用代码验证成功")
    else:
        print('统一社会信用代码验证失败')

