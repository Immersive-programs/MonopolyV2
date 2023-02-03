class char:
    def draw(buf,x,y,index,col):
        zero = x+8*index+1
        buf.line(zero,y,zero+1,y+1,col)
        buf.line(zero,y+1,zero+1,y+2,col)
        buf.line(zero+3,y,zero+3,y+6,col)
        buf.line(zero+5,y+1,zero+6,y,col)
        buf.line(zero+5,y+2,zero+6,y+1,col)
        buf.line(zero+2,y+2,zero+4,y+2,col)
        buf.line(zero+2,y+3,zero+4,y+3,col)
        buf.line(zero+2,y+4,zero+4,y+4,col)
        buf.line(zero,y+6,zero+1,y+5,col)
        buf.line(zero,y+5,zero+1,y+4,col)
        buf.line(zero+5,y+5,zero+6,y+6,col)
        buf.line(zero+5,y+4,zero+6,y+5,col)
