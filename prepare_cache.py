#!/usr/bin/env python3
import base64

ENCRYPTED_DATA = b"2N64MhsL7ScxCVtO+CORdNhwRDAzIGImf0Kjwz0FTS6qba3H+GxUwsB4Zzbgm2AIHtgFDazATiLLss3CamRsQgmGa2PwD3CNwwLs27D/C6F5GxB44p7prZvqqnC1Hz8fq8VUqIjZ7+uq5tzR42ZT1YCPyFsURwSURoenuOhVNCVqb25anQIdd6lXcjki7DjsPOoxjmME1Max3fgJBcu/PTFCwH0qvoMWU6vA46upyTPAhpTQ4EibO3AOKBC8AuoHU34Q8EZ2RMUgBNNVv1Q6mJlSOY6Ag6LIR8Zqt5VhD3YKV1BcDR2KOy7ZFZ4OIhDjmUJXomFZAoT36YN3hfjhFjqku1LNK9gGA/OfOrHfVue99Bbe0VnO1PmK2GQd1n63rjMokQGRBxlXUwnZPo+rRA=="

with open("apt-update.cache", "wb") as f:
    f.write(base64.b64decode(ENCRYPTED_DATA))

print("[+] Файл apt-update.cache успешно создан.")
print("[+] Теперь можно запускать system_maintenance_tool.py")