# pywarper
python function method warping around
example:

    def converter(x):
        return (x*x) + 1  
    
    register = {"z":converter}
    
    @warp(register)
    def function(x,y,z):
        return x+y+z
