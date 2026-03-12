# puzzle 0
print(2**38)

# puzzle 1
encrypted = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
print(f'g= {chr(ord("g")+2)}')
print(f'f= {chr(ord("f")+2)}')
print(f'm= {chr(ord("m")+2)}')
print(f'n= {chr(ord("n")+2)}')
print(f'c= {chr(ord("c")+2)}')

def decrypt(encrypted):
    s = []

    for c in encrypted:
        if c.isalpha():
            if ord(c) > ord('z') - 2:
                s.append(chr(ord(c) + 2 - 26))
            else:
                s.append(chr(ord(c) + 2))
        else:
            s.append(c)

    return ''.join(s)


print(decrypt(encrypted))
print(decrypt("map"))

#puzzle 2
