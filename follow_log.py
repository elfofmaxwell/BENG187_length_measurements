import serial, time

def follow_log(path): 
    '''
    path: string of log file's path
    '''
    with open(path, 'r') as f: 
        lines = f.readlines()
        last_line = lines[-1].rstrip()
    
    return last_line

def ph_converter(ph_read, slope, intercept): 
    '''
    ph_read: int, from ph sensor pin analog read
    slope (k), intercept(b): float, ph = k * ph_signal +b
    '''
    ph_signal = ph_read/1023*5
    ph_value = ph_signal * slope + intercept

    return ph_value

def string_slicer(line): 
    '''
    line: string, readline result
    return: list of string
    '''
    sliced_string = (line.split())
    for i in range(len(sliced_string)): 
        sliced_string[i] = (sliced_string[i].strip())[:-1]
    
    return sliced_string




def output_serial(port, baudrate, timeout, path): 
    '''
    port: string, port name
    baudrate: int
    timeout: int
    path: string, path for the log file
    '''
    with open(path, 'w') as ser_output:
        #ser_output.write('Start at '+time.strftime('%a, %d %b %Y %H:%M:%S'))
        print('ready')
    with serial.Serial(port, baudrate, timeout=1) as ser: 
        while True: 
            try: 
                line = ser.readline()
                line = line.decode().strip()
                
                if line: 
                    sliced_line = string_slicer(line)
                    formated_temp = '%5.1f'%(float(sliced_line[0]))
                    ph_value = ph_converter(int(sliced_line[1]), -6.7001, 25.022)
                    formated_ph = '%5.1f'%ph_value
                    formatted_line = time.strftime('%H:%M:%S, ')+formated_temp+', '+formated_ph+',\n'
                    with open(path, 'a') as ser_output: 
                        ser_output.write(formatted_line)
            except KeyboardInterrupt: 
                break

