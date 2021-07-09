# pywarper
python function method warping around
example:

    def converter_1(value):
        return (value*value) + 1  
    
    def converter_2(value):
        return (value/2)*3.14
    
    register = {"z":converter_1,"y":converter_2}
    
    @warp(register)
    def function(x,y,z):
        return x+y+z
    
    function(2,4,8)
    
    register["x"] = lambda value : value
    
    function(2,4,8)
