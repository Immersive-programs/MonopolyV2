class char:
    def draw(buf,x,y,index,col):
        zero = x+8*index+1
        buf.line(zero+5,y,zero+5,y+6,col)
        buf.line(zero+4,y,zero+4,y+6,col)
        
        buf.line(zero+1,y+6,zero+5,y+2,col)
        buf.line(zero,y+6,zero+4,y+2,col)
        
        buf.line(zero+1,y+3,zero+4,y+3,col)
        buf.line(zero+1,y,zero+4,y,col)
        buf.line(zero,y+1,zero,y+2,col)
