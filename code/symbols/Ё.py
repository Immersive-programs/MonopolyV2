class char:
    def draw(buf,x,y,index,col):
        zero = x+8*index+1
        buf.line(zero,y+2,zero,y+6,col)
        buf.line(zero+1,y+2,zero+1,y+6,col)
        buf.line(zero,y+2,zero+4,y+2,col)
        buf.line(zero,y+4,zero+3,y+4,col)
        buf.line(zero,y+6,zero+4,y+6,col)
        buf.pixel(zero+1,y,col)
        buf.pixel(zero+3,y,col)
        #buf.text('E', zero, y, col)
