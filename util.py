def get_config(fname="sensor.config"):
    with open(fname, encoding="utf8") as fobj:
        lines = fobj.readlines()
    
    props = {}
    
    try:
        for l in lines:
            key, value = l.split('=')
            props[key] = value.rstrip('\n')
    except ValueError:
        print("Error al cargar configuracion del sensor.")
    
    return props

def rgb(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)

if __name__ == "__main__":
    print(get_config())

