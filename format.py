# read output file as lines
with open('output.log','r') as f:
    lines = f.readlines()
    
# get status and name of test 
with open('test1.log','a') as ff:
    for line in lines:       
        ff.write(line[line.find('status') + len('status": "') : line.find('"', line.find('status') + len('status": "'))])
        ff.write(' ----> ')
        ff.write(line[line.find('name": "minio-py:') + len('name": "minio-py:') : line.find(',', line.find('name": "minio-py:')) - 1])
        ff.write('\n')
    