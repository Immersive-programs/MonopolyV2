class char:
    def draw(buf,x,y,index,col):
        zero = x+8*index+1
        buf.pixel(zero,y+1,col)
        buf.pixel(zero,y+5,col)
        buf.line(zero+1,y,zero+4,y,col)
        buf.line(zero+1,y+6,zero+4,y+6,col)
        buf.line(zero+2,y+3,zero+5,y+3,col)
        buf.line(zero+5,y+1,zero+5,y+5,col)