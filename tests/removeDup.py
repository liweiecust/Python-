"""
测试数据：50亿+的数据去重，200G+超大文件
此法不耗内存，但比上面千万级数据快速去重略慢
data此文件夹需先创建好
"""

from time import time
 
SPLIT_COUNT = 10
 
def write_data(t_file, value):
	t_file.write(value)

# hash方法：从大文件中取出每行数据X，并对数据进行hash(X)%N，N是需要hash到的文件数目，这就达到了对相同的数据映射到同一个文件的办法，而在分配的过程中根据计算机的内存来调整N的大小，这样做的目的就是为了让内存读入小文件进行set操作。
def calcu_hash(filename, handle_file):
	with open(filename, 'r') as f:
		for line in f:
			write_data(handle_file[hash(line)%SPLIT_COUNT], line)

#生成文件 
def generate_file(dir):
	handle_file, files = [], []
	for i in range(SPLIT_COUNT):
		path = dir+"split_"+str(i)
		files.append(path)
		f = open(path , 'w')						#此f不能关闭
		handle_file.append(f)
	return files, handle_file

#关闭文件 
def close_file(handle_file):
	for i in range(len(handle_file)):
		handle_file[i].close()

#数据去重 
def data_uniq(files, new_file):
	dataset = dict()
	n_file = open(new_file, 'w')
	i = 0
	for filename in files:
		f = open(filename, 'r')
		for line in f:
			dataset[line] = 1
		f.close()
		for key in dataset:					
			n_file.write(key)
			i += 1
		dataset = {}
	n_file.close()
	print('去重后总行数为%s行。' % i)
 
if __name__ == "__main__":
	filename = 'e:/Python/mypy/字典.txt'				#待去重的文件
	generate_dir = 'e:/Python/mypy/data/'			#data此文件夹需先创建好
	new_file = 'e:/Python/mypy/字典_new.txt'			#去重后的新文件
	print('开始去重...')
	start = time()
	files, handle_file = generate_file(generate_dir)
	calcu_hash(filename, handle_file)
	close_file(handle_file)
	data_uniq(files, new_file)
	end = time()
	shi = end - start
	print('去重完毕！')
	print('总耗时%s秒！' % shi)