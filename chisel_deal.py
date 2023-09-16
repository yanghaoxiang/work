#! /usr/bin/python3

import os
import shutil

def deal_asert(outfile, tmpfile):
    fread = open(outfile,'r')
    ftmp = open(tmpfile,'w+')
    while(1):
        line = fread.readline()
        if not line:
            break
        elif(line.find('endmodule') != -1):
            ftmp.write(line)
            break
        elif(line.find('`ifndef SYNTHESIS') != -1):
            while(1):
                line = fread.readline()
                if(line.find('`endif // SYNTHESIS') != -1):
                    break
        else:
            ftmp.write(line)

    fread.close()
    ftmp.close()
    shutil.move(tmpfile, outfile)

def deal_comet(outfile, tmpfile):
    fread = open(outfile,'r')
    ftmp = open(tmpfile,'w+')
    while(1):
        line = fread.readline()
        if not line:
            break
        elif(line.find('endmodule') != -1):
            ftmp.write(line)
            break
        elif(line.find('// @') != -1):
            ftmp.write(line.split('//')[0]+'\r')
        else:
            ftmp.write(line)
    fread.close()
    ftmp.close()
    shutil.move(tmpfile, outfile)

def deal_init(outfile, tmpfile):
    fread = open(outfile,'r')
    ftmp = open(tmpfile,'w+')
    while(1):
        line = fread.readline()
        if not line:
            break
        elif(line.find('endmodule') != -1):
            ftmp.write(line)
            break
        elif(line.find('`ifdef RANDOMIZE_REG_INIT') != -1):
            while(1):
                line = fread.readline()
                if(line.find('`endif // RANDOMIZE_REG_INIT') != -1):
                    break
        elif(line.find('// Register and memory initialization') != -1):
            while(1):
                line = fread.readline()
                if(line.find('endmodule') != -1):
                    ftmp.write(line)
                    break
        else:
            ftmp.write(line)
    fread.close()
    ftmp.close()
    shutil.move(tmpfile, outfile)
            
def deal_rst(outfile, tmpfile):
    fread = open(outfile,'r')
    ftmp = open(tmpfile,'w+')
    while(1):
        line = fread.readline()
        if not line:
            break
        elif(line.find('endmodule') != -1):
            ftmp.write(line)
            break
        elif(line.find('always @(posedge clock or posedge reset)') != -1):
            ftmp.write('    always @(posedge clock or negedge reset) begin\r')
        elif(line.find('if (reset) begin') != -1):
            ftmp.write('      if (!reset) begin\r')
        else:
            ftmp.write(line)
    fread.close()
    ftmp.close()
    shutil.move(tmpfile, outfile)

def deal_file(infile, outfile, tmpfile):
    shutil.copyfile(infile,outfile)
    deal_rst(outfile,tmpfile)
    deal_init(outfile,tmpfile)
    deal_comet(outfile,tmpfile)
    deal_asert(outfile,tmpfile)

def main():
    in_path = r'D:\WORKSPACE\WORK_STC\src\main\verilog'
    out_path = r'D:\WORKSPACE\Python\chisel_deal\out'
    tmp_path = r'D:\WORKSPACE\Python\chisel_deal\tmp'
    f = os.listdir(in_path)
    for file in f:
        infile = in_path+'\\'+file
        outfile = out_path+'\\'+file
        tmpfile = tmp_path+'\\'+file
        if file.find('.v') != -1:
            print(file)
            deal_file(infile,outfile,tmpfile)

if __name__ == '__main__':
    main()