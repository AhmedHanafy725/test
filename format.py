# read output file as lines
with open('output.log','r') as f:
    lines = f.readlines()
    
# get status and name of test 
with open('test.log','a') as ff:
    for line in lines:       
        ff.write(line[line.find('status') + len('status": "') : line.rfind('}') - 1])
        ff.write(' ----> ')
        ff.write(line[line.find('minio-py') + len('minio-py:') : line.find(',') - 1])
        ff.write('\n')
    
