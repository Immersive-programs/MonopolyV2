class char:
    def draw(buf,x,y,index,col):
        zero = x+8*index+1
        buf.line(zero+3,y,zero+3,y+6,col)
        buf.line(zero+1,y+1,zero+5,y+1,col)
        buf.line(zero+1,y+2,zero+5,y+2,col)
        buf.line(zero+1,y+4,zero+5,y+4,col)
        buf.line(zero+1,y+5,zero+5,y+5,col)
        buf.line(zero,y+2,zero,y+4,col)
        buf.line(zero+6,y+2,zero+6,y+4,col)

