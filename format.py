# read output file as lines
with open('output.log','r') as f:
    lines = f.readlines()
    
# get status and name of test 
with open('test.log','a') as ff:
    for line in lines:       
        ff.write(line[line.find('status') + len('status": "') : 'status') + len('status": "') + 4])
        ff.write(' ----> ')
        ff.write(line[line.find('name": "minio-py:') + len('name": "minio-py:') : line.find(',', line.find('name": "minio-py:')) - 1])
        ff.write('\n')
    
