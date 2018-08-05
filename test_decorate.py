
def my_decorator(func):

    def wrapper(y):
    
        print("Something is happening before some_function() is called.")

        g = func(y)
        
        print("Something is happening after some_function() is called.")


        return g
    return wrapper



@my_decorator
def func(x):
    print(x)
    return x+1
import logging
logging.basicConfig(filename = "mylog.log", filemode='w',level = logging.DEBUG)
logging.info('Started')
z = func(5)
logging.info("finished")
print(z)
