import threading, time

def my_inline_function():
    for i in range(100):
        print(i)
        time.sleep(0.1)


t = threading.Thread(my_inline_function())
t.daemon = True
t.start()
time.sleep(1)
print('Holly shit, this works')