a = {'username': 'ash', 'password': 'wdsaasd'}
b = '=? AND '.join(a.keys()) + '=?'
c = tuple(a.values())



#if __name__ == "__main__":
