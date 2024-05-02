import socket
import subprocess
import time
import os
import datetime

buffersize = 1024

serverIP = '10.1.1.191'
severport = 5000

def write_log(log_message, *args, **kwargs):
  log_file = '/home/pi/info-logs.txt'
  if not os.path.exists(log_file):
    with open(log_file, 'w') as f:
        f.write('')
  with open(log_file, 'a') as f:
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f'{timestamp} - {log_message}: {kwargs}\n'
    f.write(log_line)
    print(log_line)

def execute_python_command(path):
  # Run command in shell
  return subprocess.run(['python3', path], capture_output=True, text=True)

def send_udp_response(message, socket, addr):
  # Encode message and send via socket UDP
  bytestosend = message.encode('utf-8')
  socket.sendto(bytestosend, addr)

def handle_script_result(result):
  if result.stdout:
    return result.stdout
  else:
    return result.stderr
  
def receive_udp_message_and_execute_python_command():
  try:
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to port 5000
    sock.bind((serverIP, severport))

    os.system('Listening...')
    write_log('Listening for UDP message.')

    while True:
      # Waiting for message
      data, addr = sock.recvfrom(buffersize)

      # Decode message 
      command = data.decode('utf-8')

      os.system(command)
      os.system(addr[0])
      write_log('Incoming Message: ', command=command, ip=addr[0])

      if command == 'hello': # Check if the socket is listening
        messageFromServer = 'Hello from server'
        send_udp_response(messageFromServer, sock, addr)
      elif command == 'take photo':
        result = execute_python_command('/home/pi/webcam/webcam.py')
        send_udp_response(handle_script_result(result), sock, addr)
      elif command == 'close':
        break

  except OSError as ex:
    if ex.errno == 99:  # Address already in use
      print(f"Address {serverIP}:{severport} already in use, retrying in 10 seconds...")
      time.sleep(10)
    else:
      error_message = f"An error has occurred while processing command: {str(ex)}"
      write_log(error_message)
      send_udp_response(error_message, sock, addr)
  except Exception as ex:
      error_message = f"An error has occurred while processing command: {str(ex)}"
      write_log(error_message)
      send_udp_response(error_message, sock, addr)
  finally:
    sock.close()

if __name__ == "__main__":
  receive_udp_message_and_execute_python_command()
