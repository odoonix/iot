from zk import ZK, const

try:
    _ip = input('Enter your ip:')
    _password = input('Enter your password:')
except EOFError as e:
    print(e)
    
conn = None
# create ZK instance
zk = ZK(str(_ip), port=4370, timeout=5, password=int(_password), force_udp=False, ommit_ping=False)
try:
    # connect to device
    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()
    # another commands will be here!
    # Example: Get All Users
    attendances = conn.get_attendance()
    print(attendances)
    
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
