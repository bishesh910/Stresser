import socket
import time
from datetime import datetime
import threading

def send_log_to_syslog(log_message, syslog_server, port, count):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((syslog_server, port))
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for _ in range(count):
            s.sendall((f"{current_time} {log_message}\n").encode('utf-8'))
            time.sleep(1 / count)  # Adjust sleep duration for desired frequency

def send_logs_concurrently(log_message, syslog_server, port, count, num_threads):
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=send_log_to_syslog, args=(log_message, syslog_server, port, count // num_threads))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def run_infinite_loop(log_message, syslog_server, port, count, num_threads):
    try:
        while True:
            send_logs_concurrently(log_message, syslog_server, port, count, num_threads)
            time.sleep(1)  # Wait for 1 second before starting the next iteration

    except KeyboardInterrupt:
        print("Program terminated by user.")

if __name__ == "__main__":
    log_message = "May 31 20:42:26 f5.echo.saycure.io ASM:CEF:0|F5|ASM|16.1.3|Successful Request|Successful Request|2|dvchost=f5.echo.saycure.io dvc=172.26.10.3 cs1=/Common/WEBSITE-NEW-AWAF-POLICY cs1Label=policy_name cs2=/Common/WEBSITE-NEW-AWAF-POLICY cs2Label=http_class_name deviceCustomDate1=May 31 2023 20:14:14 deviceCustomDate1Label=policy_apply_date externalId=9648031521178177656 act=deny attack=HTTP_Parser_Attack cn1=403 cn1Label=response_code src=208.94.147.100 spt=30252 dst=172.25.10.44 dpt=443 requestMethod=GET app=HTTPS cs5=208.94.147.100 cs5Label=x_forwarded_for_header_value rt=May 31 2023 20:42:26 deviceExternalId=0 cs4=N/A cs4Label=attack_type cs6=US cs6Label=geo_location c6a1= c6a1Label=device_address c6a2= c6a2Label=source_address c6a3= c6a3Label=destination_address c6a4= c6a4Label=ip_address_intelligence msg=N/A suid=4b190ebfa6f220e9 suser=N/A cn2=0 cn2Label=violation_rating cn3=0 cn3Label=device_id microservice=N/A request=/admin/login cs3Label=full_request cs3=GET /admin/login HTTP/1.1\r\nHost: backend.echo.saycure.io\r\nConnection: Keep-Alive\r\nUser-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Q312461; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)\r\nX-Forwarded-For: 208.94.147.100\r\n\r\n"
    syslog_server = "192.168.108.67"
    port = 514
    count = 1500
    num_threads = 5  # Adjust the number of threads based on your needs

    run_infinite_loop(log_message, syslog_server, port, count, num_threads)
