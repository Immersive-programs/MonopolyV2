class char:
    def draw(buf,x,y,index,col):
        zero = x+8*index+1
        buf.line(zero,y,zero,y+6,col)
        buf.line(zero+6,y,zero+6,y+6,col)
        buf.line(zero+3,y,zero+3,y+6,col)
        buf.line(zero,y+6,zero+6,y+6,col)
        buf.line(zero+6,y+7,zero+6,y+6,col)