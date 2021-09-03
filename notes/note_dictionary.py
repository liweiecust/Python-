###
#  dictionary
###

# create dictionary
#  method 1
my_dict={'a':'1','b':'2','c':'3'}
#  method 2
my_dict=dict(a='1',b='2',c='3')

print(type(my_dict))    # <class 'dict'>
print('keys:',my_dict.keys(),'values:',my_dict.values()) 

# -- keys
keys=my_dict.keys()
print('type of keys:',type(keys)) #type of keys: <class 'dict_keys'>
for key in keys:
    print(key)

# --iterate item in dictionary
for item in my_dict:
    print(item)     # item is actually the value of each item in dictionary. it's not key-value object
