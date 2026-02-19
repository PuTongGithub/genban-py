try:
    import msvcrt
except ModuleNotFoundError:
    _mswindows = False
else:
    _mswindows = True

def is_mswindows() -> bool:
    return _mswindows
