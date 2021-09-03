import hashlib

# 1. md5是不可逆的，不能解密
# 2. 所有语言生成的md5串都是一样的

# 3. 不论字符串多长，生成的md5是等长的

s='123456'
#变成bytes类型才能加密
encode_s=s.encode()
md5_str=hashlib.md5(encode_s)
print(md5_str.hexdigest())


# 加盐是在用户密码加密后，可以再加一个指定的字符串，再次加密，这样，用户密码被破解的概率极低