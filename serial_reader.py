import follow_log

ser_log_path = 'D:\\se_ds\\ref\\ser_log.txt'
port = 'COM6'
baudrate = 9600

follow_log.output_serial(port, baudrate, 1, ser_log_path)

