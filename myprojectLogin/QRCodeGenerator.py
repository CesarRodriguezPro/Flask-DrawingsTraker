

import qrcode 
import os

basedir = os.path.abspath(os.path.dirname(__file__))

def create_barcode(id_number, update_date):
    print(f'{id_number}   --  {update_date}')
    data = f'https://www.ibktech.info/ret/xcd{id_number}{update_date}'
    img = qrcode.make(data)
    img.save(os.path.join(basedir, f'static/{id_number}.jpg'))

def path_for_ScanID():
    return os.path.join(basedir, 'BarcodesID')

if __name__ == "__main__":
    input('')
