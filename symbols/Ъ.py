class char:
    def draw(buf,x,y,index,col):
        zero = x+8*index+3
        buf.line(zero,y,zero,y+6,col)
        buf.line(zero+1,y,zero+1,y+6,col)
        buf.line(zero,y+6,zero+2,y+6,col)
        buf.line(zero,y+3,zero+2,y+3,col)
        buf.line(zero+3,y+4,zero+3,y+5,col)
        buf.line(zero-2,y,zero,y,col)
        buf.line(zero-2,y+1,zero,y+1,col)