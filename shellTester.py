import sh
from subprocess import check_output
print('Ip:' + str(sh.hostname('-I')) + 'hi')
if check_output(['hostname','-I']) == '\n':
    print('Hello')
else:
    print('waiting')



    


