class char:
    def draw(buf,x,y,index,col):
        zero = x+8*index+1
        buf.line(zero,y+6,zero+4,y+6,col)
        buf.line(zero,y,zero+4,y,col)
        buf.line(zero,y+3,zero+4,y+3,col)
        buf.line(zero+5,y+1,zero+5,y+2,col)
        buf.line(zero+4,y+1,zero+4,y+2,col)
        buf.line(zero+5,y+4,zero+5,y+5,col)
        buf.line(zero+4,y+4,zero+4,y+5,col)