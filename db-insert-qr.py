import getpass
import oracledb
import datetime
import pyotp
import qrcode
import sys
import platform

#k = pyotp.random_base32()

secret_key = "AAAAAAA"

def generate_qr(name, version=1):
    if platform.system() == "Windows":
        white_block = ''
        black_block = ''
        new_line = '\n'
    else:
        white_block = '\033[0;37;47m  '
        black_block = '\033[0;37;40m  '
        new_line = '\033[0m\n'
    
    totp_auth = pyotp.totp.TOTP(secret_key).provisioning_uri(name=name,issuer_name='issure name')

    qr = qrcode.QRCode(version)
    
    # Adding data to the instance 'qr'
    qr.add_data(totp_auth)
    
    qr.make(fit = True)
    output = white_block*(qr.modules_count+2) + new_line
    for mn in qr.modules:
        output += white_block
        for m in mn:
            if m:
                output += black_block
            else:
                output += white_block
        output += white_block + new_line
    output += white_block*(qr.modules_count+2) + new_line
    return output
    #img = qr.make_image(fill_color = 'yellow', back_color = 'black')
    #img.save('qr.png')

def insert_db():
    t = datetime.datetime.now()
    date = t.strftime('%m-%d-%Y-%H-%M')

    #pw = getpass.getpass("Enter password: ")

    connection = oracledb.connect(
        user="user",
        password="password",
        dsn="DATABASE_HOST:port/DATABASE_NAME")

    print("Successfully connected to Oracle Database")

    cur = connection.cursor()
    cur.execute("INSERT INTO [SIGNAL_SCHEMA_NAME].[SIGNAL_TABLE_NAME] (id, type, data) VALUES('ad-hoc-" + date + "', 'execute-snapshot', '{data-collections: [[SCHEMA_NAME].[TABLE_NAME]],type:incremental}')")
    connection.commit()

    print("success")
    print(date)
    
def verify_qr():
    totp_qr = pyotp.TOTP(secret_key)
    return totp_qr.verify(input(("Enter the Code : ")))
     
if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "--qr":
            while True:
                pw = getpass.getpass("Enter password: ")
                if pw == 'Password':
                    print(generate_qr(name="name", version=1))
                    exit(0)
        
    if verify_qr():
        insert_db()
    else:
        print("OTP incorrect")